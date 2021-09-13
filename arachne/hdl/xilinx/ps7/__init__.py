# SPDX-License-Identifier: BSD-3-Clause

from typing       import List, Tuple, Union
from nmigen       import *
from nmigen.build import *

from ...amba4.axi import *
from .mio         import _PS7_MIO_MAPPING
from .resources   import *
from .adaptors    import *

__all__ = (
	'PS7', 'PS7CoreResource', 'PS7DDR3Resource'
)

class PS7(Elaboratable):
	"""Xilinx Zynq SoC PS Block

	"""
	def __init__(self, *, core, **kwargs):
		self._ps_resources = {
			'can0':  kwargs.get('can0', None),
			'can1':  kwargs.get('can1', None),
			'dma0':  kwargs.get('dma0', None),
			'dma1':  kwargs.get('dma1', None),
			'dma2':  kwargs.get('dma2', None),
			'dma3':  kwargs.get('dma3', None),
			'ddr':   kwargs.get('ddr', None),
			'eth0':  kwargs.get('eth0', None),
			'eth1':  kwargs.get('eth1', None),
			'i2c0':  kwargs.get('i2c0', None),
			'i2c1':  kwargs.get('i2c1', None),
			'jtag':  kwargs.get('jtag', None),
			'sdio0': kwargs.get('sdio0', None),
			'sdio1': kwargs.get('sdio1', None),
			'spi0':  kwargs.get('spi0', None),
			'spi1':  kwargs.get('spi1', None),
			'trace': kwargs.get('trace', None),
			'uart0': kwargs.get('uart0', None),
			'uart1': kwargs.get('uart1', None),
			'usb0':  kwargs.get('usb0', None),
			'usb1':  kwargs.get('usb1', None),
		}
		self._pl_resources = {
			'axi_gp0': (
				Interface(
					addr_width = 32, data_width = 32, id_width = 12,
					bus_type = AXIBusType.Full,
					interface_type = AXIInterfaceType.Manager,
					features = {'atomic', 'qos'},
					name = 'axi_m_gp0'
				),
				Interface(
					addr_width = 32, data_width = 32, id_width = 12,
					bus_type = AXIBusType.Full,
					interface_type = AXIInterfaceType.Subordinate,
					features = {'atomic', 'qos'},
					name = 'axi_s_gp0'
				),
			),
			'axi_gp1': (
				Interface(
					addr_width = 32, data_width = 32, id_width = 12,
					bus_type = AXIBusType.Full,
					interface_type = AXIInterfaceType.Manager,
					features = {'atomic', 'qos'},
					name = 'axi_m_gp1'
				),
				Interface(
					addr_width = 32, data_width = 32, id_width = 12,
					bus_type = AXIBusType.Full,
					interface_type = AXIInterfaceType.Subordinate,
					features = {'atomic', 'qos'},
					name = 'axi_s_gp1'
				),
			),
			'axi_hp0': Interface(
				addr_width = 32, data_width = 64, id_width = 6,
				bus_type = AXIBusType.Full,
				interface_type = AXIInterfaceType.Subordinate,
				features = {'atomic', 'qos'},
				name = 'axi_hp0'
			),
			'axi_hp1': Interface(
				addr_width = 32, data_width = 64, id_width = 6,
				bus_type = AXIBusType.Full,
				interface_type = AXIInterfaceType.Subordinate,
				features = {'atomic', 'qos'},
				name = 'axi_hp1'
			),
			'axi_hp2': Interface(
				addr_width = 32, data_width = 64, id_width = 6,
				bus_type = AXIBusType.Full,
				interface_type = AXIInterfaceType.Subordinate,
				features = {'atomic', 'qos'},
				name = 'axi_hp2'
			),
			'axi_hp3': Interface(
				addr_width = 32, data_width = 64, id_width = 6,
				bus_type = AXIBusType.Full,
				interface_type = AXIInterfaceType.Subordinate,
				features = {'atomic', 'qos'},
				name = 'axi_hp3'
			),
		}
		self._core = core

	def add_resource(self, *, name, resource) -> None:
		if name not in self._ps_resources:
			raise ValueError('Resource name not valid')
		elif self._ps_resources[name] is not None:
			raise ValueError('Resource already assigned, refusing to reassign to a new resource')
		self._ps_resources[name] = resource

	def get_resource(self, *, name) -> Record:
		if name not in self._pl_resources:
			raise ValueError('Resource name not valid')
		return self._pl_resources[name]

	def elaborate(self, platform) -> Module:
		m = Module()
		fixed_io = Signal(54, reset_less = True)

		ddr_map, ddr_adaptor = self._map_ddr()
		if ddr_adaptor is not None:
			m.submodules += ddr_adaptor

		m.submodules.ps7 = Instance(
			'PS7',
			# Core
			i_PSCLK = self._core.clk.i,
			i_PSPORB = self._core.por_n.i,
			i_PSSRSTB = self._core.srst_n.i,
			# MIO
			o_MIO = fixed_io,
			# AXI Bus'
			**self._map_axi_gp(num = 0),
			**self._map_axi_gp(num = 1),
			**self._map_axi_hp(num = 0),
			**self._map_axi_hp(num = 1),
			**self._map_axi_hp(num = 2),
			**self._map_axi_hp(num = 3),
			# CAN
			**self._map_can(m, platform = platform, mio = fixed_io, num = 0),
			**self._map_can(m, platform = platform, mio = fixed_io, num = 1),
			# DDR3 Memory
			**ddr_map,
			# Ethernet
			**self._map_eth(m, platform = platform, mio = fixed_io, num = 0),
			**self._map_eth(m, platform = platform, mio = fixed_io, num = 1),
			# I2C
			**self._map_i2c(m, platform = platform, mio = fixed_io, num = 0),
			**self._map_i2c(m, platform = platform, mio = fixed_io, num = 1),
			# JTAG
			**self._map_jtag(m, platform = platform, mio = fixed_io),
			# SDIO (SDCard interfaces)
			**self._map_sdio(m, platform = platform, mio = fixed_io, num = 0),
			**self._map_sdio(m, platform = platform, mio = fixed_io, num = 1),
			# SPI
			**self._map_spi(m, platform = platform, mio = fixed_io, num = 0),
			**self._map_spi(m, platform = platform, mio = fixed_io, num = 1),
			# UART
			**self._map_uart(m, platform = platform, mio = fixed_io, num = 0),
			**self._map_uart(m, platform = platform, mio = fixed_io, num = 1),
			# USB
			**self._map_usb(m, platform = platform, mio = fixed_io, num = 0),
			**self._map_usb(m, platform = platform, mio = fixed_io, num = 1),
		)

		# This is a pile of hacks. We tell nMigen that the MIO on the PS7 instance
		# "drives" fixed_io, and we tell it that the BIBUF's below are "driven"
		# by fixed_io, and this stops it from propergating the signal up through to
		# the outside world, which causes errors
		mio = Signal.like(fixed_io)
		for idx in range(len(mio)):
			m.submodules[f'mio_buf_{idx}'] = Instance(
				'BIBUF',
				io_PAD = mio[idx],
				i_IO = fixed_io[idx],
			)
		return m

	def _demap_resource(self, resource : Record) -> Tuple[str, int]:
		name, number = resource.name.rsplit('_', maxsplit = 1)
		return (name, int(number))

	def _find_subsignal(self, resource : Resource, name : str) -> Subsignal:
		for subsig in resource.ios:
			if subsig.name == name:
				return subsig
		raise KeyError('Subsignal not found')

	def _map_to_pad(self, *, resource : Resource, name : str) -> List[str]:
		subsignal = self._find_subsignal(resource, name)
		for part in subsignal.ios:
			if isinstance(part, Pins):
				return part.names

	def _mio_idx(self, *, mapping : List[tuple], pad : str) -> Union[int, None]:
		for idx, pad_name in mapping:
			if pad == pad_name:
				return idx
		return None

	def _mio_map_pads(self, m, mapping, mio, subsig, pads, dir):
		unmapped = False
		for i, pad in enumerate(pads):
			idx = self._mio_idx(mapping = mapping, pad = pad)
			if idx is None:
				unmapped = True
				continue
			if 'i' in dir:
				m.d.comb += mio[idx].eq(subsig.i[i])
			else:
				m.d.comb += subsig.o[i].eq(mio[idx])
		return unmapped

	def _map_mio(self, m, *, mapping, mio, resource, subsignal):
		unmapped = True
		for io in subsignal.ios:
			if isinstance(io, Pins):
				unmapped &= self._mio_map_pads(m, mapping, mio, getattr(resource, subsignal.name), io.names, io.dir)
			else:
				unmapped = False
		return unmapped

	def _map_axi_gp(self, *, num) -> dict:
		manager, subordinate = self._pl_resources[f'axi_gp{num}']
		return {
			**self._map_axi_manager(name = f'GP{num}', bus = manager),
			**self._map_axi_subordinate(name = f'GP{num}', bus = subordinate),
		}

	def _map_axi_hp(self, *, num) -> dict:
		bus = self._pl_resources[f'axi_hp{num}']
		return {
			f'o_SAXIHP{num}RACOUNT':       Signal(3),
			f'o_SAXIHP{num}RCOUNT':        Signal(8),
			f'i_SAXIHP{num}RDISSUECAP1EN': Signal(),
			f'o_SAXIHP{num}WACOUNT':       Signal(6),
			f'o_SAXIHP{num}WCOUNT':        Signal(8),
			f'i_SAXIHP{num}WRISSUECAP1EN': Signal(),
			**self._map_axi_subordinate(name = f'HP{num}', bus = bus)
		}

	def _map_axi_manager(self, *, name, bus) -> dict:
		return {
			f'i_MAXI{name}ACLK':    bus.clk,
			f'o_MAXI{name}ARESETN': bus.rst_n,

			# Read Address
			f'o_MAXI{name}ARVALID': bus.arvalid,
			f'i_MAXI{name}ARREADY': bus.arready,
			f'o_MAXI{name}ARADDR':  bus.araddr,
			f'o_MAXI{name}ARID':    bus.arid,
			f'o_MAXI{name}ARPROT':  bus.arprot,
			f'o_MAXI{name}ARLEN':   bus.arlen,
			f'o_MAXI{name}ARSIZE':  bus.arsize,
			f'o_MAXI{name}ARBURST': bus.arburst,
			f'o_MAXI{name}ARCACHE': bus.arcache,
			# Read Data
			f'i_MAXI{name}RVALID':  bus.rvalid,
			f'o_MAXI{name}RREADY':  bus.rready,
			f'i_MAXI{name}RDATA':   bus.rdata,
			f'i_MAXI{name}RRESP':   bus.rresp,
			f'i_MAXI{name}RID':     bus.rid,
			f'i_MAXI{name}RLAST':   bus.rlast,
			# Read Atomic
			f'o_MAXI{name}ARLOCK':  bus.arlock,
			# Read QoS
			f'o_MAXI{name}ARQOS':   bus.arqos,

			# Write Address
			f'o_MAXI{name}AWVALID': bus.awvalid,
			f'i_MAXI{name}AWREADY': bus.awready,
			f'o_MAXI{name}AWADDR':  bus.awaddr,
			f'o_MAXI{name}AWPROT':  bus.awprot,
			f'o_MAXI{name}AWID':    bus.awid,
			f'o_MAXI{name}AWLEN':   bus.awlen,
			f'o_MAXI{name}AWSIZE':  bus.awsize,
			f'o_MAXI{name}AWBURST': bus.awburst,
			f'o_MAXI{name}AWCACHE': bus.awcache,
			# Write Data
			f'o_MAXI{name}WVALID':  bus.wvalid,
			f'i_MAXI{name}WREADY':  bus.wready,
			f'o_MAXI{name}WDATA':   bus.wdata,
			f'o_MAXI{name}WSTRB':   bus.wstrobe,
			f'o_MAXI{name}WID':     bus.wid,
			f'o_MAXI{name}WLAST':   bus.wlast,
			# Write Response
			f'i_MAXI{name}BVALID':  bus.bvalid,
			f'o_MAXI{name}BREADY':  bus.bready,
			f'i_MAXI{name}BRESP':   bus.bresp,
			f'i_MAXI{name}BID':     bus.bid,
			# Write Atomic
			f'o_MAXI{name}AWLOCK':  bus.awlock,
			# Write QoS
			f'o_MAXI{name}AWQOS':   bus.awqos,
		}

	def _map_axi_subordinate(self, *, name, bus) -> dict:
		return {
			f'i_SAXI{name}ACLK':    bus.clk,
			f'o_SAXI{name}ARESETN': bus.rst_n,

			# Read Address
			f'i_SAXI{name}ARVALID': bus.arvalid,
			f'o_SAXI{name}ARREADY': bus.arready,
			f'i_SAXI{name}ARADDR':  bus.araddr,
			f'i_SAXI{name}ARID':    bus.arid,
			f'i_SAXI{name}ARPROT':  bus.arprot,
			f'i_SAXI{name}ARLEN':   bus.arlen,
			f'i_SAXI{name}ARSIZE':  bus.arsize,
			f'i_SAXI{name}ARBURST': bus.arburst,
			f'i_SAXI{name}ARCACHE': bus.arcache,
			# Read Data
			f'o_SAXI{name}RVALID':  bus.rvalid,
			f'i_SAXI{name}RREADY':  bus.rready,
			f'o_SAXI{name}RDATA':   bus.rdata,
			f'o_SAXI{name}RRESP':   bus.rresp,
			f'o_SAXI{name}RID':     bus.rid,
			f'o_SAXI{name}RLAST':   bus.rlast,
			# Read Atomic
			f'i_SAXI{name}ARLOCK':  bus.arlock,
			# Read QoS
			f'i_SAXI{name}ARQOS':   bus.arqos,

			# Write Address
			f'i_SAXI{name}AWVALID': bus.awvalid,
			f'o_SAXI{name}AWREADY': bus.awready,
			f'i_SAXI{name}AWADDR':  bus.awaddr,
			f'i_SAXI{name}AWPROT':  bus.awprot,
			f'i_SAXI{name}AWID':    bus.awid,
			f'i_SAXI{name}AWLEN':   bus.awlen,
			f'i_SAXI{name}AWSIZE':  bus.awsize,
			f'i_SAXI{name}AWBURST': bus.awburst,
			f'i_SAXI{name}AWCACHE': bus.awcache,
			# Write Data
			f'i_SAXI{name}WVALID':  bus.wvalid,
			f'o_SAXI{name}WREADY':  bus.wready,
			f'i_SAXI{name}WDATA':   bus.wdata,
			f'i_SAXI{name}WSTRB':   bus.wstrobe,
			f'i_SAXI{name}WID':     bus.wid,
			f'i_SAXI{name}WLAST':   bus.wlast,
			# Write Response
			f'o_SAXI{name}BVALID':  bus.bvalid,
			f'i_SAXI{name}BREADY':  bus.bready,
			f'o_SAXI{name}BRESP':   bus.bresp,
			f'o_SAXI{name}BID':     bus.bid,
			# Write Atomic
			f'i_SAXI{name}AWLOCK':  bus.awlock,
			# Write QoS
			f'i_SAXI{name}AWQOS':   bus.awqos,
		}

	def _map_can(self, m, *, platform, mio, num) -> dict:
		can = self._ps_resources[f'can{num}']
		if can is not None:
			mapping = _PS7_MIO_MAPPING[platform.device, platform.package]['mio']
			resource = platform.lookup(*self._demap_resource(can))

			unmapped = True
			for subsignal in resource.ios:
				unmapped &= self._map_mio(m, mapping = mapping, mio = mio, resource = can, subsignal = subsignal)

			if unmapped:
				return {
					f'i_EMIOCAN{num}PHYRX': can.rx.i,
					f'o_EMIOCAN{num}PHYTX': can.tx.o,
				}

		return {
			f'i_EMIOCAN{num}PHYRX': Signal(),
			f'o_EMIOCAN{num}PHYTX': Signal(),
		}

	def _map_ddr(self) -> Tuple[dict, Elaboratable]:
		if self._ps_resources['ddr'] is not None:
			ddr = DDR3Adaptor(bus = self._ps_resources['ddr'])
			return ({
				'o_DDRDRSTB': ddr.rst_n,
				'o_DDRCKP':   ddr.clk_p,
				'o_DDRCKN':   ddr.clk_n,
				'o_DDRCKE':   ddr.clk_en,
				'o_DDRCSB':   ddr.cs_n,
				'o_DDRWEB':   ddr.we_n,
				'o_DDRRASB':  ddr.ras_n,
				'o_DDRCASB':  ddr.cas_n,
				'o_DDRA':     ddr.address,
				'o_DDRBA':    ddr.bank_address,

				'io_DDRDQSP': ddr.data_strobe_p,
				'io_DDRDQSN': ddr.data_strobe_n,
				'io_DDRDQ':   ddr.data,
				'io_DDRDM':   ddr.data_mask,

				'io_DDRODT':  ddr.odt_en,
				'io_DDRVRP':  ddr.voltage_ref_p,
				'io_DDRVRN':  ddr.voltage_ref_n,
			}, ddr)
		else:
			return ({
				'o_DDRDRSTB': Signal(),
				'o_DDRCKP':   Signal(),
				'o_DDRCKN':   Signal(),
				'o_DDRCKE':   Signal(),
				'o_DDRCSB':   Signal(),
				'o_DDRWEB':   Signal(),
				'o_DDRRASB':  Signal(),
				'o_DDRCASB':  Signal(),
				'o_DDRA':     Signal(15),
				'o_DDRBA':    Signal(3),

				'io_DDRDQSP': Signal(4),
				'io_DDRDQSN': Signal(4),
				'io_DDRDQ':   Signal(32),
				'io_DDRDM':   Signal(4),

				'io_DDRODT':  Signal(),
				'io_DDRVRP':  Signal(),
				'io_DDRVRN':  Signal(),
			}, None)

	def _map_eth(self, m, *, platform, mio, num) -> dict:
		eth = self._ps_resources[f'eth{num}']
		if eth is not None:
			mapping = _PS7_MIO_MAPPING[platform.device, platform.package]['mio']
			resource = platform.lookup(*self._demap_resource(eth))

			unmapped = True
			for subsignal in resource.ios:
				unmapped &= self._map_mio(m, mapping = mapping, mio = mio, resource = eth, subsignal = subsignal)

			if unmapped:
				rx_domain = f'eth{num}_rx'
				tx_domain = f'eth{num}_tx'

				rx_clk = Signal()
				rx = Signal(8)
				rx_dv = Signal()
				rx_err = Signal()

				tx_clk = Signal()
				tx = Signal(8)
				tx_en = Signal()
				tx_err = Signal()
				col = Signal()
				crs = Signal()

				m.domains += ClockDomain(rx_domain)
				m.domains += ClockDomain(tx_domain)

				m.d.comb += [
					ClockSignal(rx_domain).eq(rx_clk),
					ClockSignal(tx_domain).eq(tx_clk),
				]

				# Apparently the Ethernet is miss-timed and requires a pipeline stage inserting.
				# RGMII
				if hasattr(eth, 'rx_ctl'):
					converter = GMIItoRGMII(rgmii = eth)
					m.submodules += converter

					m.d.comb += [
						rx_clk.eq(converter.rx_clk),
						converter.tx_clk.eq(tx_clk),
					]

					m.d[rx_domain] += [
						rx.eq(converter.rx),
						rx_dv.eq(converter.rx_dv),
						rx_err.eq(converter.rx_err),
					]

					m.d[tx_domain] += [
						converter.tx.eq(tx),
						converter.tx_en.eq(tx_en),
						converter.tx_err.eq(tx_err),
					]
				else:
				# GMII
					m.d.comb += [
						rx_clk.eq(eth.rx_clk.i),
						eth.tx_clk.o.eq(tx_clk),
					]

					m.d[rx_domain] += [
						rx.eq(eth.rx.i),
						rx_dv.eq(eth.rx_dv.i),
						rx_err.eq(eth.rx_err.i),
					]

					m.d[tx_domain] += [
						eth.tx.o.eq(tx),
						eth.tx_en.o.eq(tx_en),
						eth.tx_err.o.eq(tx_err),
					]
					if hasattr(eth, 'col'):
						m.d[tx_domain] += col.eq(eth.col.i)
					if hasattr(eth, 'crs'):
						m.d[tx_domain] == crs.eq(eth.crs.i)

				mdc = eth.mdc.o if hasattr(eth, 'mdc') else Signal()
				mdio_i = eth.mdio.i if hasattr(eth, 'mdio') else Signal()
				mdio_o = eth.mdio.o if hasattr(eth, 'mdio') else Signal()
				mdio_oe_n = Signal()

				if hasattr(eth, 'mdio'):
					m.d.comb += eth.mdio.oe.eq(~mdio_oe_n)

				return {
					f'i_EMIOENET{num}GMIIRXCLK': rx_clk,
					f'i_EMIOENET{num}GMIIRXD':   rx,
					f'i_EMIOENET{num}GMIIRXDV':  rx_dv,
					f'i_EMIOENET{num}GMIIRXER':  rx_err,

					f'o_EMIOENET{num}GMIITXCLK': tx_clk,
					f'o_EMIOENET{num}GMIITXD':   tx,
					f'o_EMIOENET{num}GMIITXEN':  tx_en,
					f'o_EMIOENET{num}GMIITXER':  tx_err,
					f'i_EMIOENET{num}GMIICOL':   col,
					f'i_EMIOENET{num}GMIICRS':   crs,

					f'o_EMIOENET{num}MDIOMDC':   mdc,
					f'i_EMIOENET{num}MDIOI':     mdio_i,
					f'o_EMIOENET{num}MDIOO':     mdio_o,
					f'o_EMIOENET{num}MDIOTN':    mdio_oe_n,
				}

		return {
			f'i_EMIOENET{num}GMIIRXCLK': Signal(),
			f'i_EMIOENET{num}GMIIRXD':   Signal(8),
			f'i_EMIOENET{num}GMIIRXDV':  Signal(),
			f'i_EMIOENET{num}GMIIRXER':  Signal(),

			f'o_EMIOENET{num}GMIITXCLK': Signal(),
			f'o_EMIOENET{num}GMIITXD':   Signal(8),
			f'o_EMIOENET{num}GMIITXEN':  Signal(),
			f'o_EMIOENET{num}GMIITXER':  Signal(),
			f'i_EMIOENET{num}GMIICOL':   Signal(),
			f'i_EMIOENET{num}GMIICRS':   Signal(),

			f'o_EMIOENET{num}MDIOMDC':   Signal(),
			f'i_EMIOENET{num}MDIOI':     Signal(),
			f'o_EMIOENET{num}MDIOO':     Signal(),
			f'o_EMIOENET{num}MDIOTN':    Signal(),
		}

	def _map_i2c(self, m, *, platform, mio, num) -> dict:
		i2c = self._ps_resources[f'i2c{num}']
		if i2c is not None:
			mapping = _PS7_MIO_MAPPING[platform.device, platform.package]['mio']
			resource = platform.lookup(*self._demap_resource(i2c))

			unmapped = True
			for subsignal in resource.ios:
				unmapped &= self._map_mio(m, mapping = mapping, mio = mio, resource = i2c, subsignal = subsignal)

			if unmapped:
				scl_oe_n = Signal()
				sda_oe_n = Signal()

				m.d.comb += [
					i2c.scl.oe.eq(~scl_oe_n),
					i2c.sda.oe.eq(~sda_oe_n),
				]

				return  {
					f'i_EMIOI2C{num}SCLI':  i2c.scl.i,
					f'o_EMIOI2C{num}SCLO':  i2c.scl.o,
					f'o_EMIOI2C{num}SCLTN': scl_oe_n,
					f'i_EMIOI2C{num}SDAI':  i2c.sda.i,
					f'o_EMIOI2C{num}SDAO':  i2c.sda.o,
					f'o_EMIOI2C{num}SDATN': sda_oe_n,
				}

		return {
			f'i_EMIOI2C{num}SCLI':  Signal(),
			f'o_EMIOI2C{num}SCLO':  Signal(),
			f'o_EMIOI2C{num}SCLTN': Signal(),
			f'i_EMIOI2C{num}SDAI':  Signal(),
			f'o_EMIOI2C{num}SDAO':  Signal(),
			f'o_EMIOI2C{num}SDATN': Signal(),
		}

	def _map_jtag(self, m, *, platform, mio) -> dict:
		jtag = self._ps_resources['jtag']
		if jtag is not None:
			mapping = _PS7_MIO_MAPPING[platform.device, platform.package]['mio']
			resource = platform.lookup(*self._demap_resource(jtag))

			unmapped = True
			for subsignal in resource.ios:
				unmapped &= self._map_mio(m, mapping = mapping, mio = mio, resource = jtag, subsignal = subsignal)

			if unmapped:
				tdo_oe_n = Signal()

				m.d.comb += jtag.tdo.oe.eq(~tdo_oe_n)

				return {
					'i_EMIOPJTAGTCK':  jtag.tck.i,
					'i_EMIOPJTAGTMS':  jtag.tms.i,
					'i_EMIOPJTAGTDI':  jtag.tdi.i,
					'o_EMIOPJTAGTDO':  jtag.tdo.o,
					'o_EMIOPJTAGTDTN': tdo_oe_n,
				}

		return {
			'i_EMIOPJTAGTCK':  Signal(),
			'i_EMIOPJTAGTMS':  Signal(),
			'i_EMIOPJTAGTDI':  Signal(),
			'o_EMIOPJTAGTDO':  Signal(),
			'o_EMIOPJTAGTDTN': Signal(),
		}

	def _map_sdio(self, m, *, platform, mio, num) -> dict:
		sdio = self._ps_resources[f'sdio{num}']
		if sdio is not None:
			mapping = _PS7_MIO_MAPPING[platform.device, platform.package]['mio']
			resource = platform.lookup(*self._demap_resource(sdio))

			unmapped = True
			for subsignal in resource.ios:
				unmapped &= self._map_mio(m, mapping = mapping, mio = mio, resource = sdio, subsignal = subsignal)

			if unmapped:
				data_oe_n = Signal()

				m.d.comb += sdio.dat.oe.eq(~data_oe_n)

				return {
					f'i_EMIOSDIO{num}CDN':    sdio.cd.i,
					f'o_EMIOSDIO{num}CLK':    sdio.clk.o,
					f'o_EMIOSDIO{num}CMDO':   sdio.cmd.o,
					f'i_EMIOSDIO{num}DATAI':  sdio.dat.i,
					f'o_EMIOSDIO{num}DATAO':  sdio.dat.o,
					f'o_EMIOSDIO{num}DATATN': data_oe_n,
				}

		return {
			f'i_EMIOSDIO{num}CDN':    Signal(),
			f'o_EMIOSDIO{num}CLK':    Signal(),
			f'o_EMIOSDIO{num}CMDO':   Signal(),
			f'i_EMIOSDIO{num}DATAI':  Signal(4),
			f'o_EMIOSDIO{num}DATAO':  Signal(4),
			f'o_EMIOSDIO{num}DATATN': Signal(4),
		}

	def _map_spi(self, m, *, platform, mio, num) -> dict:
		spi = self._ps_resources[f'spi{num}']
		if spi is not None:
			mapping = _PS7_MIO_MAPPING[platform.device, platform.package]['mio']
			resource = platform.lookup(*self._demap_resource(spi))

			unmapped = True
			for subsignal in resource.ios:
				unmapped &= self._map_mio(m, mapping = mapping, mio = mio, resource = spi, subsignal = subsignal)

			if unmapped:
				cs_i = Signal()
				cs_o = Signal(3)
				cs_oe = Signal()
				clk_i = Signal()
				clk_o = Signal()
				clk_oe = Signal()
				copi_i = Signal()
				copi_o = Signal()
				copi_oe = Signal()
				cipo_i = Signal()
				cipo_o = Signal()
				cipo_oe = Signal()

				# Controller mode
				if hasattr(spi.cs, 'o'):
					if len(spi.cs.o) > 3:
						raise AssertionError('Too many chip selects for PS SPI block - '
							f'have 3, requested {len(spi.cs.o)}')
					m.d.comb += [
						spi.cs.o.eq(cs_o[:len(spi.cs.o)]),
						spi.clk.o.eq(clk_o)
					]
					if hasattr(spi, 'copi'):
						m.d.comb += spi.copi.o.eq(copi_o)
					if hasattr(spi, 'cipo'):
						m.d.comb += cipo_i.eq(spi.cipo.i)
				# Peripheral mode
				else:
					m.d.comb += [
						cs_i.eq(spi.cs.i),
						clk_i.eq(spi.clk.i)
					]
					if hasattr(spi, 'copi'):
						m.d.comb += copi_i.eq(spi.copi.i)
					if hasattr(spi, 'cipo'):
						m.d.comb += [
							spi.cipo.o.eq(cipo_o),
							spi.cipo.oe.eq(cipo_oe),
						]

				return {
					f'i_EMIOSPI{num}SSIN':   cs_i,
					f'o_EMIOSPI{num}SSON':   cs_o,
					f'o_EMIOSPI{num}SSNTN':  cs_oe,
					f'i_EMIOSPI{num}SCLKI':  clk_i,
					f'o_EMIOSPI{num}SCLKO':  clk_o,
					f'o_EMIOSPI{num}SCLKTN': clk_oe,
					f'i_EMIOSPI{num}MI':     cipo_i,
					f'o_EMIOSPI{num}MO':     copi_o,
					f'o_EMIOSPI{num}MOTN':   copi_oe,
					f'i_EMIOSPI{num}SI':     copi_i,
					f'o_EMIOSPI{num}SO':     cipo_o,
					f'o_EMIOSPI{num}STN':    cipo_oe,
				}

		return {
			f'i_EMIOSPI{num}SSIN':   Signal(),
			f'o_EMIOSPI{num}SSON':   Signal(3),
			f'o_EMIOSPI{num}SSNTN':  Signal(),
			f'i_EMIOSPI{num}SCLKI':  Signal(),
			f'o_EMIOSPI{num}SCLKO':  Signal(),
			f'o_EMIOSPI{num}SCLKTN': Signal(),
			f'i_EMIOSPI{num}MI':     Signal(),
			f'o_EMIOSPI{num}MO':     Signal(),
			f'o_EMIOSPI{num}MOTN':   Signal(),
			f'i_EMIOSPI{num}SI':     Signal(),
			f'o_EMIOSPI{num}SO':     Signal(),
			f'o_EMIOSPI{num}STN':    Signal(),
		}

	def _map_uart(self, m, *, platform, mio, num) -> dict:
		uart = self._ps_resources[f'uart{num}']
		if uart is not None:
			mapping = _PS7_MIO_MAPPING[platform.device, platform.package]['mio']
			resource = platform.lookup(*self._demap_resource(uart))

			unmapped = True
			for subsignal in resource.ios:
				unmapped &= self._map_mio(m, mapping = mapping, mio = mio, resource = uart, subsignal = subsignal)

			if unmapped:
				rts_n = Signal()
				cts_n = Signal()
				dtr_n = Signal()
				dsr_n = Signal()
				dcd_n = Signal()
				ri_n = Signal()

				return {
					f'i_EMIOUART{num}RX':   uart.rx.i,
					f'o_EMIOUART{num}TX':   uart.tx.o,

					f'o_EMIOUART{num}RTSN': rts_n,
					f'i_EMIOUART{num}CTSN': cts_n,
					f'o_EMIOUART{num}DTRN': dtr_n,
					f'i_EMIOUART{num}DSRN': dsr_n,
					f'i_EMIOUART{num}DCDN': dcd_n,
					f'i_EMIOUART{num}RIN':  ri_n,
				}

		return {
			f'i_EMIOUART{num}RX':   Signal(),
			f'o_EMIOUART{num}TX':   Signal(),

			f'o_EMIOUART{num}RTSN': Signal(),
			f'i_EMIOUART{num}CTSN': Signal(),
			f'o_EMIOUART{num}DTRN': Signal(),
			f'i_EMIOUART{num}DSRN': Signal(),
			f'i_EMIOUART{num}DCDN': Signal(),
			f'i_EMIOUART{num}RIN':  Signal(),
		}

	def _map_usb(self, m, *, platform, mio, num) -> dict:
		usb = self._ps_resources[f'usb{num}']
		if usb is not None:
			mapping = _PS7_MIO_MAPPING[platform.device, platform.package]['mio']
			resource = platform.lookup(*self._demap_resource(usb))
			port_ind_ctrl = Signal(2)
			vbus_pwr_select = Signal()
			vbus_pwr_fault = Signal()

			for subsignal in resource.ios:
				if subsignal.name == 'ind_ctl':
					m.d.comb += usb.ind_ctl.eq(port_ind_ctrl)
				elif subsignal.name == 'vbus_select':
					m.d.comb += usb.vbus_select.eq(vbus_pwr_select)
				elif subsignal.name == 'vbus_fault':
					m.d.comb += vbus_pwr_fault.eq(usb.vbus_fault)
				else:
					self._map_mio(m, mapping = mapping, mio = mio, resource = usb, subsignal = subsignal)

			return {
				f'o_EMIOUSB{num}PORTINDCTL': port_ind_ctrl,
				f'o_EMIOUSB{num}VBUSPWRSELECT': vbus_pwr_select,
				f'i_EMIOUSB{num}VBUSPWRFAULT': vbus_pwr_fault,
			}
		else:
			return {
				f'o_EMIOUSB{num}PORTINDCTL': Signal(2),
				f'o_EMIOUSB{num}VBUSPWRSELECT': Signal(),
				f'i_EMIOUSB{num}VBUSPWRFAULT': Signal(),
			}

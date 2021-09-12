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
			'emac0': kwargs.get('emac0', None),
			'emac1': kwargs.get('emac1', None),
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
		mio = Signal(54, reset_less = True)

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
			io_MIO = mio,
			# AXI Bus'
			**self._map_axi_gp(num = 0),
			**self._map_axi_gp(num = 1),
			**self._map_axi_hp(num = 0),
			**self._map_axi_hp(num = 1),
			**self._map_axi_hp(num = 2),
			**self._map_axi_hp(num = 3),
			# DDR3 Memory
			**ddr_map,
			# JTAG
			**self._map_jtag(m, platform = platform, mio = mio),
			# SDIO (SDCard interfaces)
			**self._map_sdio(m, platform = platform, mio = mio, num = 0),
			**self._map_sdio(m, platform = platform, mio = mio, num = 1),
			# UART
			**self._map_uart(m, platform = platform, mio = mio, num = 0),
			**self._map_uart(m, platform = platform, mio = mio, num = 1),
			# USB
			**self._map_usb(m, platform = platform, mio = mio, num = 0),
			**self._map_usb(m, platform = platform, mio = mio, num = 1),
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
			f'o_SAXIHP{num}RACOUNT':       Signal(),
			f'o_SAXIHP{num}RCOUNT':        Signal(),
			f'i_SAXIHP{num}RDISSUECAP1EN': Signal(),
			f'o_SAXIHP{num}WACOUNT':       Signal(),
			f'o_SAXIHP{num}WCOUNT':        Signal(),
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

# SPDX-License-Identifier: BSD-3-Clause

from typing       import Tuple
from nmigen       import *

from ...amba4.axi import *
from .mio         import *
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

		mio = Signal(54)
		if platform.package.lower() == 'clg255':
			pass
		else:
			pass

		ddr_map, ddr_adaptor = self._map_ddr()
		if ddr_adaptor is not None:
			m.submodules += ddr_adaptor

		m.submodules += Instance(
			'PS7',
			# Core
			i_PSCLK = self._core.clk.i,
			i_PSPORB = self._core.por_n.i,
			i_PSSRSTB = self._core.srst_n.i,
			# AXI Bus'
			**self._map_axi_gp(num = 0),
			**self._map_axi_gp(num = 1),
			**self._map_axi_hp(num = 0),
			**self._map_axi_hp(num = 1),
			**self._map_axi_hp(num = 2),
			**self._map_axi_hp(num = 3),
			# DDR
			**ddr_map,
		)
		return m

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
			return ({}, None)

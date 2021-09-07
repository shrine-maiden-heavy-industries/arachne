# SPDX-License-Identifier: BSD-3-Clause

from nmigen import *

from ..amba4.axi import *
from .ps    import *

__all__ = (
	'PS7',
)

class PS7(Elaboratable):
	"""Xilinx Zynq SoC PS Block

	"""
	def __init__(self, *, clk : Signal, por_n : Signal, srst_n : Signal, **kwargs):
		self._ps_resources = {
			'can0':    kwargs.get('can0', None),
			'can1':    kwargs.get('can1', None),
			'dma0':    kwargs.get('dma0', None),
			'dma1':    kwargs.get('dma1', None),
			'dma2':    kwargs.get('dma2', None),
			'dma3':    kwargs.get('dma3', None),
			'ddr':     kwargs.get('ddr', None),
			'emac0':   kwargs.get('emac0', None),
			'emac1':   kwargs.get('emac1', None),
			'i2c0':    kwargs.get('i2c0', None),
			'i2c1':    kwargs.get('i2c1', None),
			'pjtag':   kwargs.get('pjtag', None),
			'sdio0':   kwargs.get('sdio0', None),
			'sdio1':   kwargs.get('sdio1', None),
			'spi0':    kwargs.get('spi0', None),
			'spi1':    kwargs.get('spi1', None),
			'trace':   kwargs.get('trace', None),
			'uart0':   kwargs.get('uart0', None),
			'uart1':   kwargs.get('uart1', None),
			'usb0':    kwargs.get('usb0', None),
			'usb1':    kwargs.get('usb1', None),
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
		}
		self._clk = clk
		self._por_n = por_n
		self._srst_n = srst_n

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

		perif_map = {}
		perif_map.update(self._map_axi_gp(0))
		perif_map.update(self._map_axi_gp(1))
		perif_map.update(self._map_ddr())

		Instance(
			'PS7',
			i_PSCLK = self._clk,
			i_PSPORB = self._por_n,
			i_PSSRSTB = self._srst_n,
			**perif_map,
		)
		return m

	def _map_axi_gp(self, *, num) -> dict:
		manager, subordinate = self._pl_resources[f'axi_gp{num}']
		return {}.update(
			self._map_axi_manager_gp(num = num, bus = manager),
			self._map_axi_subordinate_gp(num = num, bus = subordinate),
		)

	def _map_axi_manager_gp(self, *, num, bus) -> dict:
		return {
			f'i_MAXIGP{num}ACLK':    bus.clk,
			f'o_MAXIGP{num}ARESETN': bus.rst_n,

			# Read Address
			f'o_MAXIGP{num}ARVALID': bus.arvalid,
			f'i_MAXIGP{num}ARREADY': bus.arready,
			f'o_MAXIGP{num}ARADDR':  bus.araddr,
			f'o_MAXIGP{num}ARID':    bus.arid,
			f'o_MAXIGP{num}ARPROT':  bus.arprot,
			f'o_MAXIGP{num}ARLEN':   bus.arlen,
			f'o_MAXIGP{num}ARSIZE':  bus.arsize,
			f'o_MAXIGP{num}ARBURST': bus.arburst,
			f'o_MAXIGP{num}ARCACHE': bus.arcache,
			# Read Data
			f'i_MAXIGP{num}RVALID':  bus.rvalid,
			f'o_MAXIGP{num}RREADY':  bus.rready,
			f'i_MAXIGP{num}RDATA':   bus.rdata,
			f'i_MAXIGP{num}RRESP':   bus.rresp,
			f'i_MAXIGP{num}RID':     bus.rid,
			f'i_MAXIGP{num}RLAST':   bus.rlast,
			# Read Atomic
			f'o_MAXIGP{num}ARLOCK':  bus.arlock,
			# Read QoS
			f'o_MAXIGP{num}ARQOS':   bus.arqos,

			# Write Address
			f'o_MAXIGP{num}AWVALID': bus.awvalid,
			f'i_MAXIGP{num}AWREADY': bus.awready,
			f'o_MAXIGP{num}AWADDR':  bus.awaddr,
			f'o_MAXIGP{num}AWPROT':  bus.awprot,
			f'o_MAXIGP{num}AWID':    bus.awid,
			f'o_MAXIGP{num}AWLEN':   bus.awlen,
			f'o_MAXIGP{num}AWSIZE':  bus.awsize,
			f'o_MAXIGP{num}AWBURST': bus.awburst,
			f'o_MAXIGP{num}AWCACHE': bus.awcache,
			# Write Data
			f'o_MAXIGP{num}WVALID':  bus.wvalid,
			f'i_MAXIGP{num}WREADY':  bus.wready,
			f'o_MAXIGP{num}WDATA':   bus.wdata,
			f'o_MAXIGP{num}WSTRB':   bus.wstrobe,
			f'o_MAXIGP{num}WID':     bus.wid,
			f'o_MAXIGP{num}WLAST':   bus.wlast,
			# Write Response
			f'i_MAXIGP{num}BVALID':  bus.bvalid,
			f'o_MAXIGP{num}BREADY':  bus.bready,
			f'i_MAXIGP{num}BRESP':   bus.bresp,
			f'i_MAXIGP{num}BID':     bus.bid,
			# Write Atomic
			f'o_MAXIGP{num}AWLOCK':  bus.awlock,
			# Write QoS
			f'o_MAXIGP{num}AWQOS':   bus.awqos,
		}

	def _map_axi_subordinate_gp(self, *, num, bus) -> dict:
		return {
			f'i_SAXIGP{num}ACLK':    bus.clk,
			f'o_SAXIGP{num}ARESETN': bus.rst_n,

			# Read Address
			f'i_SAXIGP{num}ARVALID': bus.arvalid,
			f'o_SAXIGP{num}ARREADY': bus.arready,
			f'i_SAXIGP{num}ARADDR':  bus.araddr,
			f'i_SAXIGP{num}ARID':    bus.arid,
			f'i_SAXIGP{num}ARPROT':  bus.arprot,
			f'i_SAXIGP{num}ARLEN':   bus.arlen,
			f'i_SAXIGP{num}ARSIZE':  bus.arsize,
			f'i_SAXIGP{num}ARBURST': bus.arburst,
			f'i_SAXIGP{num}ARCACHE': bus.arcache,
			# Read Data
			f'o_SAXIGP{num}RVALID':  bus.rvalid,
			f'i_SAXIGP{num}RREADY':  bus.rready,
			f'o_SAXIGP{num}RDATA':   bus.rdata,
			f'o_SAXIGP{num}RRESP':   bus.rresp,
			f'o_SAXIGP{num}RID':     bus.rid,
			f'o_SAXIGP{num}RLAST':   bus.rlast,
			# Read Atomic
			f'i_SAXIGP{num}ARLOCK':  bus.arlock,
			# Read QoS
			f'i_SAXIGP{num}ARQOS':   bus.arqos,

			# Write Address
			f'i_SAXIGP{num}AWVALID': bus.awvalid,
			f'o_SAXIGP{num}AWREADY': bus.awready,
			f'i_SAXIGP{num}AWADDR':  bus.awaddr,
			f'i_SAXIGP{num}AWPROT':  bus.awprot,
			f'i_SAXIGP{num}AWID':    bus.awid,
			f'i_SAXIGP{num}AWLEN':   bus.awlen,
			f'i_SAXIGP{num}AWSIZE':  bus.awsize,
			f'i_SAXIGP{num}AWBURST': bus.awburst,
			f'i_SAXIGP{num}AWCACHE': bus.awcache,
			# Write Data
			f'i_SAXIGP{num}WVALID':  bus.wvalid,
			f'o_SAXIGP{num}WREADY':  bus.wready,
			f'i_SAXIGP{num}WDATA':   bus.wdata,
			f'i_SAXIGP{num}WSTRB':   bus.wstrobe,
			f'i_SAXIGP{num}WID':     bus.wid,
			f'i_SAXIGP{num}WLAST':   bus.wlast,
			# Write Response
			f'o_SAXIGP{num}BVALID':  bus.bvalid,
			f'i_SAXIGP{num}BREADY':  bus.bready,
			f'o_SAXIGP{num}BRESP':   bus.bresp,
			f'o_SAXIGP{num}BID':     bus.bid,
			# Write Atomic
			f'i_SAXIGP{num}AWLOCK':  bus.awlock,
			# Write QoS
			f'i_SAXIGP{num}AWQOS':   bus.awqos,
		}

	def _map_ddr(self) -> dict:
		if self._ps_resources['ddr']:
			ddr = self._ps_resources['ddr']
			return {
				'o_DDRCKP':   ddr.clk,
				'o_DDRCKN':   ddr.clk_n,
				'o_DDRCKE':   ddr.clk_en,
				'o_DDRDRSTB': ddr.rst_n,
				'o_DDRCSB':   ddr.cs_n,
				'o_DDRRASB':  ddr.ras_n,
				'o_DDRCASB':  ddr.cas_n,
				'o_DDRWEB':   ddr.we_n,
				'o_DDRA':     ddr.address,
				'o_DDRBA':    ddr.bank_address,

				'io_DDRDQ':   ddr.data,
				'io_DDRDM':   ddr.data_mask,
				'io_DDRDQSP': ddr.data_strobe,
				'io_DDRDQSN': ddr.data_strobe_n,

				'io_DDRODT':  ddr.odt_en,
				'io_DDRVRP':  ddr.voltage_ref,
				'io_DDRVRN':  ddr.voltage_ref_n,
			}
		else:
			return {}

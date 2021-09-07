# SPDX-License-Identifier: BSD-3-Clause

from nmigen import *

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
		perif_map.update(self._map_ddr())

		Instance(
			'PS7',
			i_PSCLK = self._clk,
			i_PSPORB = self._por_n,
			i_PSSRSTB = self._srst_n,
			**perif_map,
		)
		return m

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

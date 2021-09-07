# SPDX-License-Identifier: BSD-3-Clause

from nmigen import *

from .ps    import *

__all__ = (
	'PS7',
)

class PS7(Elaboratable):
	"""Xilinx Zynq SoC PS Block

	"""
	def __init__(self, *, **kwargs):
		self._resources = {
			'can0': kwargs.get('can0', None),
			'can1': kwargs.get('can1', None),
			'dma0': kwargs.get('dma0', None),
			'dma1': kwargs.get('dma1', None),
			'dma2': kwargs.get('dma2', None),
			'dma3': kwargs.get('dma3', None),
		}

	def add_resource(self, *, name, resource):
		if name not in self._resources:
			raise ValueError('Resource name not valid')
		elif self._resources[name] is not None:
			raise ValueError('Resource already assigned, refusing to reassign to a new resource')
		self._resources[name] = resource

	def elaborate(self, platform):
		m = Module()

		mio = Signal(54)
		if platform.package.lower() == 'clg255':
			pass
		else:
			pass

		#Instance(
		#	'PS7',
		#)
		return m

# SPDX-License-Identifier: BSD-3-Clause
from nmigen import *

from .ps    import *

__all__ = (
	'PS8',
)

class PS8(Elaboratable):
	"""Xilinx Zynq UltraScale+ MPSoC PS Block

	"""
	def __init__(self, *, **kwargs):
		self._resources = {

		}

	def add_resource(self, *, name, resource):
		if name not in self._resources:
			raise ValueError('Resource name not valid')
		elif self._resources[name] is not None:
			raise ValueError('Resource already assigned, refusing to reassign to a new resource')
		self._resources[name] = resource

	def elaborate(self, _):
		m = Module()

		return m

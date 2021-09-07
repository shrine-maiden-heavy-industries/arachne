# SPDX-License-Identifier: BSD-3-Clause
from nmigen import *

from .ps    import *

__all__ = (
	'PS8',
)

class PS8(Elaboratable):
	"""Xilinx Zynq UltraScale+ MPSoC PS Block

	"""
	def __init__(self, *, clk : Signal, por_n : Signal, srst_n : Signal, **kwargs):
		self._ps_resources = {

		}

		self._pl_resources = {

		}


		self._clk    = clk
		self._por_n  = por_n
		self._srst_n = srst_n

	def add_resource(self, *, name, resource):
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

		return m

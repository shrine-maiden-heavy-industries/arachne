# SPDX-License-Identifier: BSD-3-Clause

from nmigen      import *

from .mio        import *

__all__ = (
	'PS8',
)

class BUFG_PS(Elaboratable):
	"""Xilinx Zynq UltraScale+ MPSoC PS Global Buffer

	"""
	def __init__(self, *, i : Signal, o : Signal):
		self._i = i
		self._o = o

	def elaborate(self, platform) -> Module:
		m = Module()

		m.submodules.bufg_ps = Instance(
			'BUFG_PS',
			i_I = self._i,
			o_O = self._o,
		)

		return m

class PS8(Elaboratable):
	"""Xilinx Zynq UltraScale+ MPSoC PS Block

	"""
	def __init__(self, **kwargs):
		self._ps_resources = {

		}

		self._pl_resources = {

		}

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


		m.submodules.ps8 = Instance(
			'PS8',
		)

		return m

# SPDX-License-Identifier: BSD-3-Clause
from nmigen       import *
from nmigen.build import *

from ....util     import dbg

from .mio         import *
from .resources   import PS8Resource

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
	def __init__(self, *, resources = [], **kwargs):
		self._ps_resources = [ *resources ]

	def elaborate(self, platform) -> Module:
		# check to see if there is a `ps8resources` block for us
		if hasattr(platform, 'ps8resources'):
			self._ps_resources.append(*platform.ps8resources)

		self._validate_ps_resources()

		mappings = self._generate_mappings()

		m = Module()

		m.submodules.ps8 = Instance(
			'PS8',
			# unpack the generated mappings into the instance
			**mappings,
		)

		return m

	def _validate_ps_resources(self):
		if any(map(lambda r: not isinstance(r, PS8Resource), self._ps_resources)):
			raise ValueError('Non-PS8Resource found in ps resources block')

	def _generate_mappings(self):
		mappings = {}

		if len(self._ps_resources) > 0:
			for res in self._ps_resources:
				mappings.update(res.generate_mapping())

		return mappings


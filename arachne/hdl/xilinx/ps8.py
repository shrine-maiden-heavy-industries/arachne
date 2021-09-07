# SPDX-License-Identifier: BSD-3-Clause
from nmigen import *

from .ps    import *

__all__ = (
	'ps8',
)

class ps8(Elaboratable):
	"""Xilinx Zynq UltraScale+ MPSoC PS Block

	"""
	def __init__(self):
		pass

	def elaborate(self, _):
		m = Module()

		return m

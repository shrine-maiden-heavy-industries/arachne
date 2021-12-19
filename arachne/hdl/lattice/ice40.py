# SPDX-License-Identifier: BSD-3-Clause
from amaranth       import *
from amaranth.build import *

__all__ = ()



class ice40_warmboot(Elaboratable):
	def __init__(self):
		self.boot_sel    = Signal(2)
		self.triggr_boot = Signal()

	def elaborate(self, _):
		m = Module()

		m.submodules.warmboot = Instance(
			'SB_WARMBOOT',
			i_BOOT = self.triggr_boot,
			i_S0   = self.boot_sel[0],
			i_S1   = self.boot_sel[1]
		)

		return m

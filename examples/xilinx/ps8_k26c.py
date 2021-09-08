#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-3-Clause
from nmigen        import *
from nmigen.build  import *
from nmigen.hdl.ir import Elaboratable

from pathlib import Path
from sys     import path
path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from arachne.platforms.xilinx import KriaK26CSOMPlatform
from arachne.hdl.xilinx.ps8   import *

class System(Elaboratable):
	def elaborate(self, platform):
		m = Module()

		m.submodules.ps = PS8()


		return m

if __name__ == '__main__':
	platform = KriaK26CSOMPlatform()
	platform.build(System(), name = 'ps8_k26c')

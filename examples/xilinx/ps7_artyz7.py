#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-3-Clause
from nmigen import *
from nmigen.build import *
from nmigen.hdl.ir import Elaboratable
from nmigen_boards.arty_z7 import ArtyZ720Platform
from nmigen_boards.resources.memory import DDR3Resource, SDCardResources
from nmigen_boards.resources.interface import UARTResource, ULPIResource

from pathlib import Path
from sys import path
path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from arachne.resources.interface import JTAGResource
from arachne.resources.misc import DDR3VRefResource
from arachne.hdl.xilinx.ps7 import PS7, PS7CoreResource

class ArtyZ720PS7Platform(ArtyZ720Platform):
	resources = ArtyZ720Platform.resources + [
		PS7CoreResource(0,
			device = ArtyZ720Platform.device,
			package = ArtyZ720Platform.package,
			attrs = Attrs(IOSTANDARD = 'LVCMOS33')
		),

		JTAGResource(0,
			tck = 'F9', tms = 'J6', tdi = 'G6', tdo = 'F6',
			attrs = Attrs(IOSTANDARD = 'LVCMOS33')
		),

		DDR3Resource(0,
			rst_n =  'B4',
			clk_p =  'L2',
			clk_n =  'M2',
			clk_en = 'N3',
			cs_n =   'N1',
			we_n =   'M5',
			ras_n =  'P4',
			cas_n =  'P5',
			a =      'N2 K2 M3 K3 M4 L1 L4 K4 K1 J4 F5 G4 E4 D3 F4',
			ba =     'L5 R4 J5',
			dqs_p =  'C2 G2',
			dqs_n =  'B2 F2',
			dq =     'C3 B3 A2 A4 D3 D1 C1 E1 E2 E3 G3 H3 J3 H2 H1 J1',
			dm =     'A1 F1',
			odt =    'N5',
			diff_attrs = Attrs(IOSTANDARD = 'LVCMOS33'),
			attrs = Attrs(IOSTANDARD = 'LVCMOS33')
		),
		DDR3VRefResource(0,
			vref_p = 'H5',
			vref_n = 'G5',
			attrs = Attrs(IOSTANDARD = 'LVCMOS33')
		),

		UARTResource(0,
			rx = 'C5',
			tx = 'C8',
			attrs = Attrs(IOSTANDARD = 'LVCMOS33')
		),

		ULPIResource(0,
			data =    'A14 D15 A12 F12 C16 A10 E13 C18',
			clk =     'A11',
			clk_dir = 'i',
			dir =     'C13',
			nxt =     'E16',
			stp =     'C15',
			attrs = Attrs(IOSTANDARD = 'LVCMOS33')
		)
	]

class System(Elaboratable):
	def elaborate(self, platform):
		m = Module()
		m.submodules.ps7 = PS7(
			core = platform.request('ps7_core')
		)

		return m

if __name__ == '__main__':
	platform = ArtyZ720PS7Platform()
	platform.build(System(), name = 'ps7_artyz7')
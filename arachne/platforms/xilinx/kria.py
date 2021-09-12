# SPDX-License-Identifier: BSD-3-Clause

from nmigen       import *
from nmigen.build import *

from nmigen.vendor.xilinx_ultrascale  import XilinxUltraScalePlatform

from arachne.hdl.xilinx.ps8.resources import *

__all__ = (
	'KriaK26CSOMPlatform',
	'KriaK26ISOMPlatform',
	'KriaKV260Platform',
)

class _KriaK26SOMPlatform(XilinxUltraScalePlatform):
	"""Xilinx Kria KV26 system-on-module

	Datasheet
	---------
	`https://www.xilinx.com/content/dam/xilinx/support/documentation/data_sheets/ds987-k26-som.pdf <https://www.xilinx.com/content/dam/xilinx/support/documentation/data_sheets/ds987-k26-som.pdf>`_

	"""

	device       = 'xck26'
	package      = 'sfvc784'
	default_clk  = 'clk_pspl'
	speed_grade  = '2lv'

	resources    = [

	]

	ps8resources = [
	]

	connectors   = [
		Connector('som240_1', 0, {
			# Row A
			'som240_1_a3': 'A2',
			'som240_1_a4': 'A1',
			'som240_1_a6': 'C3',
			'som240_1_a7': 'C2',
			'som240_1_a9': 'G6',
			'som240_1_a10': 'F6',
			'som240_1_a12': 'G8',
			'som240_1_a13': 'F7',
			'som240_1_a15': 'F11',
			'som240_1_a16': 'J12',
			'som240_1_a17': 'H12',
			# Row B
			'som240_1_b1': 'C1',
			'som240_1_b2': 'B1',
			'som240_1_b4': 'E4',
			'som240_1_b5': 'E3',
			'som240_1_b7': 'B3',
			'som240_1_b8': 'A3',
			'som240_1_b10': 'E5',
			'som240_1_b11': 'D5',
			'som240_1_b16': 'J10',
			'som240_1_b17': 'K13',
			'som240_1_b18': 'K12',
			'som240_1_b20': 'B10',
			'som240_1_b21': 'E12',
			'som240_1_b22': 'D11',
			# Row C
			'som240_1_c3': 'G1',
			'som240_1_c4': 'F1',
			'som240_1_c6': 'G3',
			'som240_1_c7': 'F3',
			'som240_1_c9': 'B4',
			'som240_1_c10': 'A4',
			'som240_1_c12': 'D7',
			'som240_1_c13': 'D6',
			'som240_1_c18': 'H11',
			'som240_1_c19': 'G10',
			'som240_1_c20': 'F12',
			'som240_1_c22': 'B11',
			'som240_1_c23': 'A10',
			'som240_1_c24': 'A12',
			# Row D
			'som240_1_d4': 'F2',
			'som240_1_d5': 'E2',
			'som240_1_d7': 'E1',
			'som240_1_d8': 'D1',
			'som240_1_d10': 'D4',
			'som240_1_d11': 'C4',
			'som240_1_d13': 'F8',
			'som240_1_d14': 'E8',
			'som240_1_d16': 'G11',
			'som240_1_d17': 'F10',
			'som240_1_d18': 'J11',
			'som240_1_d20': 'E10',
			'som240_1_d21': 'D10',
			'som240_1_d22': 'C11',
		}),

		Connector('som240_2', 0, {
			# Row A
			'som240_2_a3': 'N4',
			'som240_2_a4': 'N3',
			'som240_2_a7': 'V6',
			'som240_2_a8': 'V5',
			'som240_2_a11': 'J5',
			'som240_2_a12': 'J4',
			'som240_2_a14': 'H4',
			'som240_2_a15': 'H3',
			'som240_2_a17': 'N7',
			'som240_2_a18': 'N6',
			'som240_2_a20': 'J1',
			'som240_2_a21': 'H1',
			'som240_2_a23': 'J7',
			'som240_2_a24': 'H7',
			'som240_2_a26': 'H9',
			'som240_2_a27': 'H8',
			'som240_2_a29': 'AG6',
			'som240_2_a30': 'AG5',
			'som240_2_a32': 'AH2',
			'som240_2_a33': 'AH1',
			'som240_2_a35': 'AB2',
			'som240_2_a36': 'AC2',
			'som240_2_a38': 'AG4',
			'som240_2_a39': 'AH4',
			'som240_2_a41': 'AD7',
			'som240_2_a42': 'AE7',
			'som240_2_a46': 'W10',
			'som240_2_a47': 'Y10',
			'som240_2_a48': 'Y9',
			'som240_2_a50': 'AA8',
			'som240_2_a51': 'AB10',
			'som240_2_a52': 'AB9',
			'som240_2_a54': 'Y14',
			'som240_2_a55': 'Y13',
			'som240_2_a56': 'W12',
			'som240_2_a58': 'W11',
			'som240_2_a59': 'Y12',
			'som240_2_a60': 'AA12',
			# Row B
			'som240_2_b1': 'T2',
			'som240_2_b2': 'T1',
			'som240_2_b5': 'R4',
			'som240_2_b6': 'R3',
			'som240_2_b9': 'Y2',
			'som240_2_b10': 'Y1',
			'som240_2_b12': 'L7',
			'som240_2_b13': 'L6',
			'som240_2_b15': 'K2',
			'som240_2_b16': 'J2',
			'som240_2_b18': 'L1',
			'som240_2_b19': 'K1',
			'som240_2_b21': 'M6',
			'som240_2_b22': 'L5',
			'som240_2_b24': 'R8',
			'som240_2_b25': 'T8',
			'som240_2_b27': 'AF8',
			'som240_2_b28': 'AG8',
			'som240_2_b30': 'AD2',
			'som240_2_b31': 'AD1',
			'som240_2_b33': 'AG3',
			'som240_2_b34': 'AH3',
			'som240_2_b36': 'AH8',
			'som240_2_b37': 'AH7',
			'som240_2_b39': 'AE2',
			'som240_2_b40': 'AF2',
			'som240_2_b44': 'AD11',
			'som240_2_b45': 'AD10',
			'som240_2_b46': 'AA11',
			'som240_2_b48': 'AA10',
			'som240_2_b49': 'AB11',
			'som240_2_b50': 'AC11',
			'som240_2_b52': 'AA13',
			'som240_2_b53': 'AB13',
			'som240_2_b54': 'W14',
			'som240_2_b56': 'W13',
			'som240_2_b57': 'AB15',
			'som240_2_b58': 'AB14',
			# Row C
			'som240_2_c3': 'Y6',
			'som240_2_c4': 'Y5',
			'som240_2_c7': 'U4',
			'som240_2_c8': 'U3',
			'som240_2_c11': 'K4',
			'som240_2_c12': 'K3',
			'som240_2_c14': 'N9',
			'som240_2_c15': 'N8',
			'som240_2_c17': 'U8',
			'som240_2_c18': 'V8',
			'som240_2_c20': 'P7',
			'som240_2_c21': 'P6',
			'som240_2_c23': 'K9',
			'som240_2_c24': 'J9',
			'som240_2_c26': 'AE3',
			'som240_2_c27': 'AF3',
			'som240_2_c29': 'AD5',
			'som240_2_c30': 'AD4',
			'som240_2_c32': 'AC4',
			'som240_2_c33': 'AC3',
			'som240_2_c35': 'AB4',
			'som240_2_c36': 'AB3',
			'som240_2_c38': 'AG9',
			'som240_2_c39': 'AH9',
			'som240_2_c41': 'AE5',
			'som240_2_c42': 'AF5',
			'som240_2_c46': 'AH12',
			'som240_2_c47': 'AH11',
			'som240_2_c48': 'AC12',
			'som240_2_c50': 'AD12',
			'som240_2_c51': 'AE10',
			'som240_2_c52': 'AF10',
			'som240_2_c54': 'AG13',
			'som240_2_c55': 'AH13',
			'som240_2_c56': 'AC14',
			'som240_2_c58': 'AC13',
			'som240_2_c59': 'AE13',
			'som240_2_c60': 'AF13',
			# Row D
			'som240_2_d1': 'V2',
			'som240_2_d2': 'V1',
			'som240_2_d5': 'P2',
			'som240_2_d6': 'P1',
			'som240_2_d9': 'W4',
			'som240_2_d10': 'W3',
			'som240_2_d12': 'U9',
			'som240_2_d13': 'V9',
			'som240_2_d15': 'W8',
			'som240_2_d16': 'Y8',
			'som240_2_d18': 'L3',
			'som240_2_d19': 'L2',
			'som240_2_d21': 'R7',
			'som240_2_d22': 'T7',
			'som240_2_d24': 'K8',
			'som240_2_d25': 'K7',
			'som240_2_d27': 'AF7',
			'som240_2_d28': 'AF6',
			'som240_2_d30': 'AE9',
			'som240_2_d31': 'AE8',
			'som240_2_d33': 'AC9',
			'som240_2_d34': 'AD9',
			'som240_2_d36': 'AB8',
			'som240_2_d37': 'AC8',
			'som240_2_d39': 'AB7',
			'som240_2_d40': 'AC7',
			'som240_2_d44': 'AE12',
			'som240_2_d45': 'AF12',
			'som240_2_d46': 'AG10',
			'som240_2_d48': 'AH10',
			'som240_2_d49': 'AF11',
			'som240_2_d50': 'AG11',
			'som240_2_d52': 'AD15',
			'som240_2_d53': 'AD14',
			'som240_2_d54': 'AE15',
			'som240_2_d56': 'AE14',
			'som240_2_d57': 'AG14',
			'som240_2_d58': 'AH14',
		}),
	]

class KriaK26ISOMPlatform(_KriaK26SOMPlatform):
	"""Xilinx Kria KV26 system-on-module Industrial

	Datasheet
	---------
	`https://www.xilinx.com/content/dam/xilinx/support/documentation/data_sheets/ds987-k26-som.pdf <https://www.xilinx.com/content/dam/xilinx/support/documentation/data_sheets/ds987-k26-som.pdf>`_

	"""

	speed = f'{_KriaK26SOMPlatform.speed_grade}-i'


class KriaK26CSOMPlatform(_KriaK26SOMPlatform):
	"""Xilinx Kria KV26 system-on-module Commercial

	Datasheet
	---------
	`https://www.xilinx.com/content/dam/xilinx/support/documentation/data_sheets/ds987-k26-som.pdf <https://www.xilinx.com/content/dam/xilinx/support/documentation/data_sheets/ds987-k26-som.pdf>`_

	"""
	speed = f'{_KriaK26SOMPlatform.speed_grade}-c'


class KriaKV260Platform(XilinxUltraScalePlatform):
	"""Xilinx Kria KV260 Vision AI Starter Kit

	Datasheet
	---------
	`https://www.xilinx.com/content/dam/xilinx/support/documentation/data_sheets/ds986-kv260-starter-kit.pdf <https://www.xilinx.com/content/dam/xilinx/support/documentation/data_sheets/ds986-kv260-starter-kit.pdf>`_

	"""

	device      = 'xck26'
	package     = 'sfvc784'
	speed       = '2lv-c'
	default_clk = 'clk_pspl'

	resources   = [

	]

	connectors = []

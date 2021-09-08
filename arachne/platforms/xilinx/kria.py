# SPDX-License-Identifier: BSD-3-Clause

from nmigen import *
from nmigen.build import *

from nmigen.vendor.xilinx_ultrascale import XilinxUltraScalePlatform

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

	device      = 'xck26'
	package     = 'sfvc784'
	default_clk = 'clk_pspl'
	speed_grade = '2lv'


	resources   = [

	]

	connectors = [
		Connector('SOM240_1', 0, {

		}),

		Connector('SOM240_2', 0, {

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

	connectors = [

	]

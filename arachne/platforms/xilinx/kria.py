# SPDX-License-Identifier: BSD-3-Clause

from nmigen import *
from nmigen.build import *

from nmigen.vendor.xilinx_ultrascale import XilinxUltraScalePlatform

__all__ = (
	'KriaK26CSOMPlatform',
	'KriaK26ISOMPlatform',
	'KriaKV260Platform',
)


class KriaK26ISOMPlatform(XilinxUltraScalePlatform):
	"""Xilinx Kria KV26 system-on-module Industrial

	Datasheet
	---------
	`https://www.xilinx.com/content/dam/xilinx/support/documentation/data_sheets/ds987-k26-som.pdf <https://www.xilinx.com/content/dam/xilinx/support/documentation/data_sheets/ds987-k26-som.pdf>`_

	"""

	device      = 'xck26'
	package     = 'sfvc784'
	speed       = '2LV-i'
	default_clk = 'clk_pspl'

	resources   = [

	]

	connectors = [
		Connector('SOM240_1', 0, {

		}),

		Connector('SOM240_2', 0, {

		}),
	]

class KriaK26CSOMPlatform(XilinxUltraScalePlatform):
	"""Xilinx Kria KV26 system-on-module Commercial

	Datasheet
	---------
	`https://www.xilinx.com/content/dam/xilinx/support/documentation/data_sheets/ds987-k26-som.pdf <https://www.xilinx.com/content/dam/xilinx/support/documentation/data_sheets/ds987-k26-som.pdf>`_

	"""

	device      = 'xck26'
	package     = 'sfvc784'
	speed       = '2LV-c'
	default_clk = 'clk_pspl'

	resources   = [

	]

	connectors = [
		Connector('SOM240_1', 0, {

		}),

		Connector('SOM240_2', 0, {

		}),
	]

class KriaKV260Platform(XilinxUltraScalePlatform):
	"""Xilinx Kria KV260 Vision AI Starter Kit

	Datasheet
	---------
	`https://www.xilinx.com/content/dam/xilinx/support/documentation/data_sheets/ds986-kv260-starter-kit.pdf <https://www.xilinx.com/content/dam/xilinx/support/documentation/data_sheets/ds986-kv260-starter-kit.pdf>`_

	"""

	device      = 'xck26'
	package     = 'sfvc784'
	speed       = '2LV-c'
	default_clk = 'clk_pspl'

	resources   = [

	]

	connectors = [

	]

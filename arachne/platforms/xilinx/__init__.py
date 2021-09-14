# SPDX-License-Identifier: BSD-3-Clause
from .unified  import XilinxPlatform

from .kria     import KriaK26CSOMPlatform, KriaK26ISOMPlatform
from .zynq7000 import XilinxZynq7000Platform

__all__ = (
	'XilinxPlatform',

	'KriaK26CSOMPlatform',
	'KriaK26ISOMPlatform',
	'KriaKV260Platform',
	'XilinxZynq7000Platform',
)

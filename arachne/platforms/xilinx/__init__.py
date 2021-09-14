# SPDX-License-Identifier: BSD-3-Clause

from .kria     import KriaK26CSOMPlatform, KriaK26ISOMPlatform
from .zynq7000 import XilinxZynq7000Platform

__all__ = (
	'KriaK26CSOMPlatform',
	'KriaK26ISOMPlatform',
	'KriaKV260Platform',
	'XilinxZynq7000Platform',
)

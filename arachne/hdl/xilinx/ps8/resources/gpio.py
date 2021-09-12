# SPDX-License-Identifier: BSD-3-Clause
from nmigen       import *
from nmigen.build import *

from .common      import PS8Resource

__all__ = (
	'GPIOResource',
)

def GPIOResource():
	io = []

	return PS8Resource('pmu', 0, *io, Attrs(IOSTANDARD="LVCMOS33"))

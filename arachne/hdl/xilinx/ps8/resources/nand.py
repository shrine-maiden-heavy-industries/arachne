# SPDX-License-Identifier: BSD-3-Clause
from nmigen       import *
from nmigen.build import *

from .common      import PS8Resource

__all__ = (
	'NANDResource',
)

def NANDResource():
	io = []

	return PS8Resource('nand', 0, *io, Attrs(IOSTANDARD="LVCMOS33"))

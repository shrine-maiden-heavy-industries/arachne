# SPDX-License-Identifier: BSD-3-Clause
from nmigen       import *
from nmigen.build import *

from .common      import PS8Resource

__all__ = (
	'DPResource',
)

def DPResource():
	io = []

	return PS8Resource('dp', 0, *io, Attrs(IOSTANDARD="LVCMOS33"))

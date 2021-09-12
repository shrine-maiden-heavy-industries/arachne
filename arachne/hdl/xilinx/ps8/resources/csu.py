# SPDX-License-Identifier: BSD-3-Clause
from nmigen       import *
from nmigen.build import *

from .common      import PS8Resource

__all__ = (
	'CSUResource',
)

def CSUResource():
	io = []

	return PS8Resource('csu', 0, *io, Attrs(IOSTANDARD="LVCMOS33"))

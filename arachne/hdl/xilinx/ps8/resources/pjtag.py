# SPDX-License-Identifier: BSD-3-Clause
from nmigen       import *
from nmigen.build import *

from .common      import PS8Resource

__all__ = (
	'PJTAGResource',
)


def PJTAGResource():
	io = []

	return PS8Resource('pjtag', 0, *io, Attrs(IOSTANDARD="LVCMOS33"))

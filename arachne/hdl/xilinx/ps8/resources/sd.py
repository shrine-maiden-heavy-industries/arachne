# SPDX-License-Identifier: BSD-3-Clause
from nmigen       import *
from nmigen.build import *

from .common      import PS8Resource

__all__ = (
	'SDResource',
)

def SDResource(num):
	if num > 1:
		raise ValueError(f'PS8 Only has sd0..1, not {num}')

	io = []

	return PS8Resource('sd', num, *io, Attrs(IOSTANDARD="LVCMOS33"))

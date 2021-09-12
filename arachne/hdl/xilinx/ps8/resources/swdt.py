# SPDX-License-Identifier: BSD-3-Clause
from nmigen       import *
from nmigen.build import *

from .common      import PS8Resource

__all__ = (
	'SWDTResource',
)

def SWDTResource(num):
	if num > 1:
		raise ValueError(f'PS8 Only has swdt0..1, not {num}')

	io = []

	return PS8Resource('swdt', num, *io, Attrs(IOSTANDARD="LVCMOS33"))

# SPDX-License-Identifier: BSD-3-Clause
from nmigen       import *
from nmigen.build import *

from .common      import PS8Resource

__all__ = (
	'GEMResource',
)

def GEMResource(num):
	if num > 3:
		raise ValueError(f'PS8 Only has gem0..3, not {num}')

	io = []

	return PS8Resource('gem', num, *io, Attrs(IOSTANDARD="LVCMOS33"))

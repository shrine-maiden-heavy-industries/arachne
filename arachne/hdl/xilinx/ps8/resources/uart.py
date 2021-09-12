# SPDX-License-Identifier: BSD-3-Clause
from nmigen       import *
from nmigen.build import *

from .common      import PS8Resource

__all__ = (
	'UARTResource',
)

def UARTResource(num):
	if num > 1:
		raise ValueError(f'PS8 Only has uart0..1, not {num}')

	io = []

	return PS8Resource('uart', num, *io, Attrs(IOSTANDARD="LVCMOS33"))

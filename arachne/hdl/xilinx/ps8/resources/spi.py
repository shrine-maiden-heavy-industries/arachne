# SPDX-License-Identifier: BSD-3-Clause
from nmigen       import *
from nmigen.build import *

from .common      import PS8Resource

__all__ = (
	'SPIResource',
)

def SPIResource(num):
	if num > 1:
		raise ValueError(f'PS8 Only has spi0..1, not {num}')

	io = []

	return PS8Resource('spi', num, *io, Attrs(IOSTANDARD="LVCMOS33"))

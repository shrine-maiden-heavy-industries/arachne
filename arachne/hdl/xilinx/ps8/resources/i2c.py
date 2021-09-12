# SPDX-License-Identifier: BSD-3-Clause
from nmigen       import *
from nmigen.build import *

from .common      import PS8Resource

__all__ = (
	'I2CResource',
)

def I2CResource(num):
	if num > 1:
		raise ValueError(f'PS8 Only has i2c0..1, not {num}')

	io = []

	return PS8Resource('i2c', num, *io, Attrs(IOSTANDARD="LVCMOS33"))

# SPDX-License-Identifier: BSD-3-Clause
from nmigen       import *
from nmigen.build import *

from .common      import PS8Resource

__all__ = (
	'USBResource',
)

def USBResource(num):
	if num > 1:
		raise ValueError(f'PS8 Only has usb0..1, not {num}')

	io = []

	return PS8Resource('usb', num, *io, Attrs(IOSTANDARD="LVCMOS33"))

# SPDX-License-Identifier: BSD-3-Clause
from nmigen       import *
from nmigen.build import *

from .common      import PS8Resource

__all__ = (
	'QSPIResource',
)

def QSPIResource():
	io = []

	return PS8Resource('qspi', 0, *io, Attrs(IOSTANDARD="LVCMOS33"))

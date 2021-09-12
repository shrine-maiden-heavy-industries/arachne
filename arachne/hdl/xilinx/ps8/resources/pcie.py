# SPDX-License-Identifier: BSD-3-Clause
import enum

from nmigen       import *
from nmigen.build import *

from .common      import PS8Resource

__all__ = (
	'PCIEResource',
	'PCIEPortType',
	'PCIELaneWidth',
)

@enum.unique
class PCIEPortType(enum.Enum):
	Endpoint = enum.auto()
	RootPort = enum.auto()

@enum.unique
class PCIELaneWidth(enum.Enum):
	x1 = enum.auto()
	x2 = enum.auto()
	x4 = enum.auto()

def PCIEResource(*, rst, ):
	io = []

	return PS8Resource('pcie', 0, *io, Attrs(IOSTANDARD="LVCMOS33"))

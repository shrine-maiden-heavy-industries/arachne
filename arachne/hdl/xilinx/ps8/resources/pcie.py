# SPDX-License-Identifier: BSD-3-Clause
import enum

from amaranth       import *
from amaranth.build import *

from .common        import PS8Resource, MIOSet

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

class PCIEResource(PS8Resource):
	name = 'pcie'
	claimable_mio = [ ]

	def __init__(self, *, width):
		super().__init__(0, 0, None, False)

	def used_mio(self, **kwargs):
		raise NotImplementedError # :nocov:

	def generate_mapping(self, **kwargs):
		raise NotImplementedError # :nocov:

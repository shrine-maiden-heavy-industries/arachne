# SPDX-License-Identifier: BSD-3-Clause
import enum

from amaranth       import *
from amaranth.build import *

from .common        import PS8Resource, MIOSet

__all__ = (
	'DPResource',
)

@enum.unique
class DPLanes(enum.Enum):
	NONE         = enum.auto()
	SingleLower  = enum.auto()
	SingleHigher = enum.auto()
	DualLower    = enum.auto()
	DualHigher   = enum.auto()

class DPResource(PS8Resource):
	name = 'dp'
	claimable_mio = [
		(27, 30), (34, 37)
	]

	def __init__(self, *, mio_set, lanes):
		super().__init__(0, 0, mio_set, True)

	def used_mio(self, **kwargs):
		raise NotImplementedError # :nocov:

	def generate_mapping(self, **kwargs):
		raise NotImplementedError # :nocov:

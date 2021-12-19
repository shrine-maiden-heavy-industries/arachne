# SPDX-License-Identifier: BSD-3-Clause
from amaranth       import *
from amaranth.build import *

from .common        import PS8Resource, MIOSet

__all__ = (
	'TraceResource',
)

def _validate_width(mio_set, width):
	if mio_set is None or width is None:
		raise ValueError('mio_set and width must not be None')

	if width not in (2, 4, 8, 16, 32):
		raise ValueError(f'trace width must be one of 2, 4, 8, 16, or 32, not {width}')

	if mio_set != MIOSet.EMIO and width == 32:
		raise ValueError(f'trace width can only be 32 in EMIO mode')



class TraceResource(PS8Resource):
	name = 'trace'
	claimable_mio = [
		(0, 17), (26, 43), (52, 69)
	]

	def __init__(self, *, mio_set, width):
		super().__init__(0, 0, mio_set, True)

		_validate_width(mio_set, width)

		self._width = width

	def used_mio(self, **kwargs):
		raise NotImplementedError # :nocov:

	def generate_mapping(self, **kwargs):
		raise NotImplementedError # :nocov:

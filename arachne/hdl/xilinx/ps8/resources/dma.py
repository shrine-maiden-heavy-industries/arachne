# SPDX-License-Identifier: BSD-3-Clause
from amaranth       import *
from amaranth.build import *

from .common        import PS8Resource

__all__ = (
	'DMAResource',
)

class DMAResource(PS8Resource):
	name = 'dma'
	claimable_mio = [ ]

	def __init__(self):
		super().__init__(0, 0, None, False)

	def used_mio(self, **kwargs):
		raise NotImplementedError # :nocov:

	def generate_mapping(self, **kwargs):
		raise NotImplementedError # :nocov:

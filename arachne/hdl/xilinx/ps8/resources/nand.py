# SPDX-License-Identifier: BSD-3-Clause
from amaranth       import *
from amaranth.build import *

from .common        import PS8Resource, MIOSet

__all__ = (
	'NANDResource',
)

class NANDResource(PS8Resource):
	name = 'nand'
	claimable_mio = [
		(9, 27), 32
	]

	def __init__(self, ):
		super().__init__(0, 0, mio_set, False)

	def used_mio(self, **kwargs):
		raise NotImplementedError # :nocov:

	def generate_mapping(self, **kwargs):
		raise NotImplementedError # :nocov:

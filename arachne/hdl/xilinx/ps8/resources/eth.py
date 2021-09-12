# SPDX-License-Identifier: BSD-3-Clause
from nmigen       import *
from nmigen.build import *

from .common      import PS8Resource, MIOSet

__all__ = (
	'ETHResource',
)

class ETHResource(PS8Resource):
	name = 'eth'
	claimable_mio = [ ]

	def __init__(self, num, mio_set):
		super().__init__(num, 3, mio_set, True)

	def used_mio(self, **kwargs):
		raise NotImplementedError # :nocov:

	def generate_mapping(self, **kwargs):
		raise NotImplementedError # :nocov:

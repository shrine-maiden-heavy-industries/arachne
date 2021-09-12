# SPDX-License-Identifier: BSD-3-Clause
from nmigen       import *
from nmigen.build import *

from .common      import PS8Resource

__all__ = (
	'ETHResource',
)

class ETHResource(PS8Resource):
	name = 'eth'
	claimable_mio = [ ]

	def __init__(self, num):
		super().__init__(num, 3)

	def used_mio(self, **kwargs):
		raise NotImplementedError # :nocov:

	def generate_mapping(self, **kwargs):
		raise NotImplementedError # :nocov:

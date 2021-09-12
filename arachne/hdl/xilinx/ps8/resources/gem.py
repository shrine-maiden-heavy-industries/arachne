# SPDX-License-Identifier: BSD-3-Clause
from nmigen       import *
from nmigen.build import *

from .common      import PS8Resource

__all__ = (
	'GEMResource',
)

class GEMResource(PS8Resource):
	name = 'gem'

	def __init__(self, num):
		if num > 3:
			raise ValueError(f'PS8 Only has gem0..3, not {num}')

	def used_mio(self, **kwargs):
		raise NotImplementedError # :nocov:

	def generate_mapping(self, **kwargs):
		raise NotImplementedError # :nocov:

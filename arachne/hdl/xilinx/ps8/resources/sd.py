# SPDX-License-Identifier: BSD-3-Clause
from nmigen       import *
from nmigen.build import *

from .common      import PS8Resource

__all__ = (
	'SDResource',
)

class SDResource(PS8Resource):
	name = 'sd'

	def __init__(self, num):
		if num > 1:
			raise ValueError(f'PS8 Only has sd0..1, not {num}')

	def used_mio(self, **kwargs):
		raise NotImplementedError # :nocov:

	def generate_mapping(self, **kwargs):
		raise NotImplementedError # :nocov:

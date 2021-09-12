# SPDX-License-Identifier: BSD-3-Clause
from nmigen       import *
from nmigen.build import *

from .common      import PS8Resource

__all__ = (
	'UARTResource',
)

class UARTResource(PS8Resource):
	name = 'uart'

	def __init__(self, num):
		if num > 1:
			raise ValueError(f'PS8 Only has uart0..1, not {num}')

	def used_mio(self, **kwargs):
		raise NotImplementedError # :nocov:

	def generate_mapping(self, **kwargs):
		raise NotImplementedError # :nocov:


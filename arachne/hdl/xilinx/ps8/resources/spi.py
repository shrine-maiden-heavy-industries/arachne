# SPDX-License-Identifier: BSD-3-Clause
from nmigen       import *
from nmigen.build import *

from .common      import PS8Resource

__all__ = (
	'SPIResource',
)

class SPIResource(PS8Resource):
	def __init__(self, num):
		if num > 1:
			raise ValueError(f'PS8 Only has spi0..1, not {num}')

	def generate_mapping(self, **kwargs):
		raise NotImplementedError # :nocov:

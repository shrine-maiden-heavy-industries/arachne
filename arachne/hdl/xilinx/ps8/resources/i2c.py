# SPDX-License-Identifier: BSD-3-Clause
from nmigen       import *
from nmigen.build import *

from .common      import PS8Resource

__all__ = (
	'I2CResource',
)

class I2CResource(PS8Resource):
	name = 'i2c'
	claimable_mio = [ ]

	def __init__(self, num):
		super().__init__(num, 1)

	def used_mio(self, **kwargs):
		raise NotImplementedError # :nocov:

	def generate_mapping(self, **kwargs):
		raise NotImplementedError # :nocov:
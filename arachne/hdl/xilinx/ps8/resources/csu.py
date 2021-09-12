# SPDX-License-Identifier: BSD-3-Clause
from nmigen       import *
from nmigen.build import *

from .common      import PS8Resource, MIOSet

__all__ = (
	'CSUResource',
)

class CSUResource(PS8Resource):
	name = 'csu'
	claimable_mio = [
		18, 19, 20, 21, 22, 23, 24, 25, 26, 31, 32, 33
	]

	def __init__(self, mio_set):
		super().__init__(0, 0, mio_set, False)

	def used_mio(self, **kwargs):
		raise NotImplementedError # :nocov:

	def generate_mapping(self, **kwargs):
		raise NotImplementedError # :nocov:

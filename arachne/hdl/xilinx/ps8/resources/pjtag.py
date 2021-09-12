# SPDX-License-Identifier: BSD-3-Clause
from nmigen       import *
from nmigen.build import *

from .common      import PS8Resource, MIOSet

__all__ = (
	'PJTAGResource',
)


class PJTAGResource(PS8Resource):
	name = 'pjtag'
	claimable_mio = [ ]

	def __init__(self):
		super().__init__(0, 0, mio_set, False)

	def used_mio(self, **kwargs):
		raise NotImplementedError # :nocov:

	def generate_mapping(self, **kwargs):
		raise NotImplementedError # :nocov:

# SPDX-License-Identifier: BSD-3-Clause
from nmigen       import *
from nmigen.build import *

from .common      import PS8Resource

__all__ = (
	'PMUResource',
)

class PMUResource(PS8Resource):
	name = 'pmu'
	claimable_mio = [ ]

	def __init__(self):
		super().__init__(0, 0)

	def used_mio(self, **kwargs):
		raise NotImplementedError # :nocov:

	def generate_mapping(self, **kwargs):
		raise NotImplementedError # :nocov:
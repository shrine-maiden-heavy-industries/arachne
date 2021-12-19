# SPDX-License-Identifier: BSD-3-Clause
from amaranth       import *
from amaranth.build import *

from .common        import PS8Resource, MIOSet

__all__ = (
	'USBResource',
)

class USBResource(PS8Resource):
	name = 'usb'
	claimable_mio = [ ]

	def __init__(self, num, mio_set):
		super().__init__(num, 1, mio_set, False)

	def used_mio(self, **kwargs):
		raise NotImplementedError # :nocov:

	def generate_mapping(self, **kwargs):
		raise NotImplementedError # :nocov:

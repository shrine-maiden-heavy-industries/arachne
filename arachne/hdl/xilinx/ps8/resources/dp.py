# SPDX-License-Identifier: BSD-3-Clause
from nmigen       import *
from nmigen.build import *

from .common      import PS8Resource

__all__ = (
	'DPResource',
)

class DPResource(PS8Resource):
	def __init__(self):
		pass

	def generate_mapping(self, **kwargs):
		raise NotImplementedError # :nocov:

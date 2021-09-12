# SPDX-License-Identifier: BSD-3-Clause
from abc          import ABCMeta, abstractmethod, abstractproperty

from nmigen       import *
from nmigen.build import *

from ..mio        import _PS8_MIO_MAPPING

__all__ = (
	'PS8Resource',
)

class PS8Resource(Subsignal, metaclass = ABCMeta):
	name = abstractproperty()

	def __init__(self, *args):
		pass

	@abstractmethod
	def used_mio(self, **kwargs):
		raise NotImplementedError # :nocov:

	@abstractmethod
	def generate_mapping(self, **kwargs):
		raise NotImplementedError # :nocov:

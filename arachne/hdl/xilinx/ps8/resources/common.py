# SPDX-License-Identifier: BSD-3-Clause
from abc          import ABCMeta, abstractmethod, abstractproperty

from nmigen       import *
from nmigen.build import *

from ..mio        import _PS8_MIO_MAPPING

__all__ = (
	'PS8Resource',
)

class PS8Resource(Subsignal, metaclass = ABCMeta):
	name          = abstractproperty()
	claimable_mio = abstractproperty()

	def __init__(self, num, rnum_max, *args):
		if num > rnum_max:
			raise ValueError(f'PS8 Only has {self.name}0..{rnum_max}, not {num}')


	@abstractmethod
	def used_mio(self, **kwargs):
		raise NotImplementedError # :nocov:

	@abstractmethod
	def generate_mapping(self, **kwargs):
		raise NotImplementedError # :nocov:

# SPDX-License-Identifier: BSD-3-Clause
from typing import List
from abc    import ABCMeta, abstractproperty, abstractmethod
import enum
from nmigen import *

from ..mio  import _PS7_MIO_MAPPING

__all__ = (
	'PS7Resource',
	'MIOSet'
)

@enum.unique
class MIOSet(enum.Enum):
	EMIO  = -1
	MIO00 =  0
	MIO01 =  1
	MIO02 =  2
	MIO03 =  3
	MIO04 =  4
	MIO05 =  5
	MIO06 =  6
	MIO07 =  7
	MIO08 =  8
	MIO09 =  9
	MIO10 = 10
	MIO11 = 11
	MIO12 = 12
	MIO13 = 13
	MIO14 = 14
	MIO15 = 15
	MIO16 = 16
	MIO17 = 17
	MIO18 = 18
	MIO19 = 19
	MIO20 = 20
	MIO21 = 21
	MIO22 = 22
	MIO23 = 23
	MIO24 = 24
	MIO25 = 25
	MIO26 = 26
	MIO27 = 27
	MIO28 = 28
	MIO29 = 29
	MIO30 = 30
	MIO31 = 31
	MIO32 = 32
	MIO33 = 33
	MIO34 = 34
	MIO35 = 35
	MIO36 = 36
	MIO37 = 37
	MIO38 = 38
	MIO39 = 39
	MIO40 = 40
	MIO41 = 41
	MIO42 = 42
	MIO43 = 43
	MIO44 = 44
	MIO45 = 45
	MIO46 = 46
	MIO47 = 47
	MIO48 = 48
	MIO49 = 49
	MIO50 = 50
	MIO51 = 51
	MIO52 = 52
	MIO53 = 53

def _expand_mio_set(mios) -> List[MIOSet]:
	result = []
	if isinstance(mios, (tuple, list)):
		if len(mios) == 2:
			begin, end = mios
			if isinstance(begin, MIOSet) and isinstance(end, MIOSet):
				result.extend((MIOSet(mio) for mio in range(begin, end + 1)))
			else:
				if isinstance(begin, MIOSet):
					result.append(begin)
				else:
					result.extend(_expand_mio_set(begin))
				if isinstance(end, MIOSet):
					result.append(end)
				else:
					result.extend(_expand_mio_set(end))
		else:
			for mio in mios:
				if isinstance(mio, MIOSet):
					result.append(mio)
				else:
					result.extend(_expand_mio_set(mio))
	else:
		result.append(mios)
	return result

class PS7Resource(Record, metaclass = ABCMeta):
	name          = abstractproperty()
	claimable_mio = abstractproperty()
	signals       = abstractproperty()

	def __init__(self, *, num, rnum_max, layout, mio_set = (), allow_emio = False):
		if num > rnum_max:
			raise AssertionError(f'PS7 only has {self.name}0..{rnum_max}, not {num}')
		elif mio_set is None:
			raise AssertionError('Resource MIO pinout is not allowed to be None')
		elif mio_set == MIOSet.EMIO and not allow_emio:
			raise AssertionError(f'EMIO is not allowed for {self.name}{num}')

		self._mios = mio_set
		self.number = num

		super().__init__(layout, name = self.name)

	def used_mio(self) -> List[MIOSet]:
		if self._mios == MIOSet.EMIO:
			return []
		else:
			return _expand_mio_set(self._mios)

	@abstractmethod
	def generate_mapping(self, **kwargs) -> dict:
		raise NotImplementedError # :nocov:

	def __repr__(self):
		return "(ps7_resource {} {} {})".format(self.name, self.number, self._content_repr())

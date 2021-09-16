# SPDX-License-Identifier: BSD-3-Clause
from abc          import ABCMeta, abstractmethod, abstractproperty
import enum

from nmigen       import *
from nmigen.build import *

from ..mio        import _PS8_MIO_MAPPING

__all__ = (
	'PS8Resource',
	'MIOSet'
)

@enum.unique
class MIOSet(enum.Enum):
	GT00  = -5
	GT01  = -4
	GT02  = -3
	GT03  = -2
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
	MIO54 = 54
	MIO55 = 55
	MIO56 = 56
	MIO57 = 57
	MIO58 = 58
	MIO59 = 59
	MIO60 = 60
	MIO61 = 61
	MIO62 = 62
	MIO63 = 63
	MIO64 = 64
	MIO65 = 65
	MIO66 = 66
	MIO67 = 67
	MIO68 = 68
	MIO69 = 69
	MIO70 = 70
	MIO71 = 71
	MIO72 = 72
	MIO73 = 73
	MIO74 = 74
	MIO75 = 75
	MIO76 = 76
	MIO77 = 77

class PS8Resource(Subsignal, metaclass = ABCMeta):
	name          = abstractproperty()
	claimable_mio = abstractproperty()

	def __init__(self, num, rnum_max, mio_set, allow_emio, *args):
		if num > rnum_max:
			raise ValueError(f'PS8 Only has {self.name}0..{rnum_max}, not {num}')

		if mio_set is not None:
			if mio_set == MIOSet.EMIO and not allow_emio:
				raise ValueError(f'EMIO is not allowed for {self.name}')

			if int(mio_set) > len(self.claimable_mio):
				raise ValueError(f'mio set is out of range of {self.name}')

		self.num = num

	@abstractmethod
	def used_mio(self, **kwargs):
		raise NotImplementedError # :nocov:

	@abstractmethod
	def generate_mapping(self, **kwargs):
		raise NotImplementedError # :nocov:

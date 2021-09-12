# SPDX-License-Identifier: BSD-3-Clause
import enum

from nmigen       import *
from nmigen.build import *

from .common      import PS8Resource

__all__ = (
	'DDRResource',
	'DDRType',
	'DDRModuleType',
)

@enum.unique
class DDRType(enum.Enum):
	LPDDR3 = enum.auto()
	DDR3   = enum.auto()
	DDR3LV = enum.auto()
	DDR4   = enum.auto()
	LPDDR4 = enum.auto()

@enum.unique
class DDRModuleType(enum.Enum):
	Discrete = enum.auto()
	UDIMM    = enum.auto()
	RDIMM    = enum.auto()

def _validate_freq(ddr_type, frq):
	if ddr_type is None or frq is None:
		raise ValueError('ddr_type and frq must not be None')

	if ddr_type == DDRType.LPDDR3:
		if frq < 100 or frq > 800:
			raise ValueError(f'Frequency for LPDDR3 must be between 100 and 800 MHz, not {frq}')

	if ddr_type == DDRType.DDR3 or ddr_type == DDRType.DDR3LV:
		if frq < 100 or frq > 400:
			raise ValueError(f'Frequency for DDR3 or DDR3LV must be between 100 and 400 MHz, not {frq}')

	if ddr_type == DDRType.DDR4:
		if frq < 100 or frq > 1200:
			raise ValueError(f'Frequency for DDR4 must be between 100 and 1200 MHz, not {frq}')

	if ddr_type == DDRType.LPDDR4:
		if frq < 100 or frq > 534:
			raise ValueError(f'Frequency for LPDDR3 must be between 100 and 534 MHz, not {frq}')

def _validate_module(ddr_type, module_type):
	if ddr_type is None or module_type is None:
		raise ValueError('ddr_type and module_type must not be None')

	if ddr_type == DDRType.LPDDR3 or ddr_type == DDRType.LPDDR4:
		if module_type != DDRModuleType.Discrete:
			raise ValueError(f'Only Discrete DDR modules are supported for LPDDR3 and LPDDR4, not {module_type}')

def _validate_width(ddr_type, width):
	if ddr_type is None or width is None:
		raise ValueError('ddr_type and width must not be None')

	if width not in (16, 32, 64):
		raise ValueError(f'width must be one of 16, 32, 64, not {width}')

	if ddr_type == DDRType.LPDDR3 or ddr_type == DDRType.DDR3 or ddr_type == DDRType.DDR3LV:
		if width == 16:
			raise ValueError(f'width must be 32 or 64, when using DDR3 not {width}')

	if ddr_type == DDRType.LPDDR4:
		if width != 32:
			raise ValueError(f'width must be 32 for LPDDR4, not {width}')

def _validate_ecc(ddr_type, ecc):
	if ddr_type is None or ecc is None:
		raise ValueError('ddr_type and ecc must not be None')

	if ddr_type == DDRType.LPDDR3 and ecc:
		raise ValueError('ECC is not supported for LPDDR3')



class DDRResource(PS8Resource):
	name = 'ddr'

	def __init__(self, *, frq, ddr_type, module_type, width, ecc):
		_validate_freq(ddr_type, frq)
		_validate_module(ddr_type, module_type)
		_validate_width(ddr_type, width)
		_validate_ecc(ddr_type, ecc)

	def used_mio(self, **kwargs):
		raise NotImplementedError # :nocov:

	def generate_mapping(self, **kwargs):
		raise NotImplementedError # :nocov:

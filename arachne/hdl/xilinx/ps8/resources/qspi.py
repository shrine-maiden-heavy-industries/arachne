# SPDX-License-Identifier: BSD-3-Clause
import enum

from nmigen       import *
from nmigen.build import *

from .common      import PS8Resource

__all__ = (
	'QSPIResource',
	'QSPIMode',
	'QSPIDataMode',
)

@enum.unique
class QSPIMode(enum.Enum):
	Single       = enum.auto()
	DualStacked  = enum.auto()
	DualParallel = enum.auto()

@enum.unique
class QSPIDataMode(enum.Enum):
	x1 = enum.auto()
	x2 = enum.auto()
	x4 = enum.auto()

def _validate_data_mode(mode, data_mode):
	if mode == QSPIMode.DualParallel and data_mode != QSPIDataMode.x4:
		raise ValueError(f'For QSPI in Dual Parallel mode the data mode must be x4 not {data_mode}')


class QSPIResource(PS8Resource):
	name = 'qspi'
	claimable_mio = [
		(0, 12)
	]

	def __init__(self, *, mode, data_mode, feedback_clk = False):
		super().__init__(0, 0)

		_validate_data_mode(mode, data_mode)

		self.mode         = mode
		self.data_mode    = data_mode
		self.feedback_clk = feedback_clk

	def used_mio(self, **kwargs):
		raise NotImplementedError # :nocov:

	def generate_mapping(self, **kwargs):
		raise NotImplementedError # :nocov:

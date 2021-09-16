# SPDX-License-Identifier: BSD-3-Clause
from nmigen               import *
from nmigen.build         import *

from .....resources.enums import *
from .common              import PS8Resource, MIOSet

__all__ = (
	'QSPIResource',
	'QSPIMode',
	'QSPIDataMode',
)

def _validate_data_mode(mode : QSPIMode, data_mode : QSPIDataMode):
	if mode == QSPIMode.DualParallel and data_mode != QSPIDataMode.x4:
		raise ValueError(f'For QSPI in Dual Parallel mode the data mode must be x4 not {data_mode}')


class QSPIResource(PS8Resource):
	name = 'qspi'
	claimable_mio = [
		(0, 12)
	]

	def __init__(self, *, mode : QSPIMode, data_mode : QSPIDataMode, feedback_clk = False):
		super().__init__(0, 0, None, False)

		_validate_data_mode(mode, data_mode)

		self.mode         = mode
		self.data_mode    = data_mode
		self.feedback_clk = feedback_clk

	def used_mio(self, **kwargs):
		raise NotImplementedError # :nocov:

	def generate_mapping(self, **kwargs):
		return {}

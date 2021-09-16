# SPDX-License-Identifier: BSD-3-Clause
import enum

__all__ = (
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
	x8 = enum.auto()

# SPDX-License-Identifier: BSD-3-Clause
from amaranth.build import *
from .enums         import *

__all__ = (
	'QSPIFlashResource'
)

def QSPIFlashResource(*args, cs_n, clk, mode : QSPIMode, data_mode : QSPIDataMode,
		dq = None, dq_a = None, dq_b = None, clk_fb = None, conn = None, attrs = None):
	if not isinstance(mode, QSPIMode) or not isinstance(data_mode, QSPIDataMode):
		raise AssertionError('mode must be a QSPIMode and data_mode a QSPIDataMode')
	elif mode == QSPIMode.Single and data_mode == QSPIDataMode.x8:
		raise AssertionError('Cannot use x8 data mode in QSPI single mode')
	elif mode == QSPIMode.DualStacked and data_mode == QSPIDataMode.x8:
		raise AssertionError('Cannot use x8 data mode in QSPI dual stacked mode')
	elif mode == QSPIMode.DualParallel and data_mode != QSPIDataMode.x8:
		raise AssertionError('Must use x8 data mode in QSPI dual parallel mode')

	clk_count = 2 if mode == QSPIMode.DualParallel else 1
	cs_count = 1 if mode == QSPIMode.Single else 2

	ios = [
		Subsignal('cs', PinsN(cs_n, dir = 'o', conn = conn, assert_width = cs_count)),
		Subsignal('clk', Pins(clk, dir = 'o', conn = conn, assert_width = clk_count)),
	]

	if mode == QSPIMode.DualParallel:
		assert dq is None and dq_a is not None and dq_b is not None
		ios.append('dq_a', Pins(dq_a, dir = 'io', conn = conn, assert_width = 4))
		ios.append('dq_b', Pins(dq_b, dir = 'io', conn = conn, assert_width = 4))
	else:
		assert dq is not None and dq_a is None and dq_b is None
		if data_mode == QSPIDataMode.x1:
			dq = dq.split(' ')
			assert len(dq) == 3
			ios.append('copi', Pins(dq[0], dir = 'o', conn = conn))
			ios.append('cipo', Pins(dq[1], dir = 'i', conn = conn))
			ios.append('hold', PinsN(dq[2], dir = 'io', conn = conn))
		elif data_mode == QSPIDataMode.x2:
			dq = dq.split(' ')
			assert len(dq) == 3
			ios.append('dq', Pins(f'{dq[0]} {dq[1]}', dir = 'io', conn = conn))
			ios.append('hold', PinsN(dq[2], dir = 'io', conn = conn))
		elif data_mode == QSPIDataMode.x4:
			ios.append('dq', Pins(dq, dir = 'io', conn = conn, assert_width = 4))

	if clk_fb is not None:
		ios.append(Subsignal('clk_fb', Pins(clk_fb, dir = 'i', conn = conn, assert_width = 1)))
	if attrs is not None:
		ios.append(attrs)
	return Resource.family(*args, ios = ios)

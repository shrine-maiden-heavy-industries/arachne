# SPDX-License-Identifier: BSD-3-Clause
from nmigen.build import *

__all__ = (
	'DDR3VRefResource',
)

def DDR3VRefResource(*args, vref_p, vref_n, conn = None, attrs = None):
	ios = [
		Subsignal('vref', DiffPairs(vref_p, vref_n, dir = 'i', conn = conn)),
	]
	if attrs is not None:
		ios.append(attrs)
	return Resource.family(*args, default_name = 'ddr3_vref', ios = ios)

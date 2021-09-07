# SPDX-License-Identifier: BSD-3-Clause
from nmigen.build import *
from .mio import _PS7_MIO_MAPPING

__all__ = (
	'PS7CoreResource', 'PS7DDR3Resource'
)

def PS7CoreResource(*args, device, package, conn = None, attrs = None):
	mapping = _PS7_MIO_MAPPING[(device, package)]['core']
	ios = [
		Subsignal('clk', Pins(mapping['clk'], dir = 'i', conn = conn)),
		Subsignal('por_n', Pins(mapping['por_n'], dir = 'i', conn = conn)),
		Subsignal('srst_n', Pins(mapping['srst_n'], dir = 'i', conn = conn)),
	]
	if attrs is not None:
		ios.append(attrs)
	return Resource.family(*args, default_name = 'ps7_core', ios = ios)

def PS7DDR3Resource(*args, device, package, ddr3 : Resource, conn = None):
	mapping = _PS7_MIO_MAPPING[(device, package)]['ddr']
	#
	ios = [
		*ddr3.ios,
		Subsignal('vref', DiffPairs(mapping['vrp'], mapping['vrn'], dir = 'i', conn = conn, assert_width=1)),
		ddr3.attrs
	]
	return Resource.family(*args, default_name = 'ps7_ddr3', ios = ios)

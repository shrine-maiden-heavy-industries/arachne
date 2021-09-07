# SPDX-License-Identifier: BSD-3-Clause
from nmigen.build import *

__all__ = (
	'JTAGResource',
)

def JTAGResource(*args, tck, tms, tdi, tdo, conn = None, attrs = None):
	ios = [
		Subsignal("tck", Pins(tck, dir = 'i', conn = conn)),
		Subsignal("tms", Pins(tms, dir = 'i', conn = conn)),
		Subsignal("tdi", Pins(tdi, dir = 'i', conn = conn)),
		Subsignal("tdo", Pins(tdo, dir = 'o', conn = conn)),
	]
	if attrs is not None:
		ios.append(attrs)
	return Resource.family(*args, default_name = 'jtag', ios = ios)

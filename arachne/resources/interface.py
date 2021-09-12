# SPDX-License-Identifier: BSD-3-Clause
from nmigen.build import *

from .            import assert_width

__all__ = (
	'JTAGResource', 'EthernetResource'
)

def JTAGResource(*args, tck, tms, tdi, tdo, conn = None, attrs = None):
	ios = [
		Subsignal('tck', Pins(tck, dir = 'i', conn = conn, assert_width = 1)),
		Subsignal('tms', Pins(tms, dir = 'i', conn = conn, assert_width = 1)),
		Subsignal('tdi', Pins(tdi, dir = 'i', conn = conn, assert_width = 1)),
		Subsignal('tdo', Pins(tdo, dir = 'oe', conn = conn, assert_width = 1)),
	]
	if attrs is not None:
		ios.append(attrs)
	return Resource.family(*args, default_name = 'jtag', ios = ios)

def EthernetResource(*args, rxck, rxd, txck, txd, mdc = None, mdio = None,
					 conn = None, attrs = None, mdio_attrs = None):
	assert_width(rxd, (4, 8))
	assert_width(txd, (4, 8))
	ios = [
		Subsignal('rx_clk', Pins(rxck, dir = 'i', conn = conn, assert_width = 1)),
		Subsignal('rx_dat', Pins(rxd, dir = 'i', conn = conn)),
		Subsignal('tx_clk', Pins(txck, dir = 'i', conn = conn, assert_width = 1)),
		Subsignal('tx_dat', Pins(txd, dir = 'o', conn = conn)),
	]
	if mdc is not None and mdio is not None:
		ios.append(Subsignal('mdc', Pins(mdc, dir = 'o', conn = conn, assert_width = 1), mdio_attrs))
		ios.append(Subsignal('mdio', Pins(mdio, dir = 'io', conn = conn, assert_width = 1), mdio_attrs))
	if attrs is not None:
		ios.append(attrs)
	return Resource.family(*args, default_name = 'eth', ios = ios)

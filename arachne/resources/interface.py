# SPDX-License-Identifier: BSD-3-Clause
from nmigen.build import *

from .            import assert_width

__all__ = (
	'JTAGResource',
	'EthernetResource',
	'CANResource',
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

def EthernetResource(*args, rxck, rxd, txck, txd, rx_dv = None, rx_err = None, rx_ctl = None,
					 tx_en = None, tx_err = None, tx_ctl = None, col = None, crs = None,
					 mdc = None, mdio = None, conn = None, attrs = None, mdio_attrs = None):
	assert_width(rxd, (4, 8))
	assert_width(txd, (4, 8))
	ios = [
		Subsignal('rx_clk', Pins(rxck, dir = 'i', conn = conn, assert_width = 1)),
		Subsignal('rx_dat', Pins(rxd, dir = 'i', conn = conn)),
		Subsignal('tx_clk', Pins(txck, dir = 'o', conn = conn, assert_width = 1)),
		Subsignal('tx_dat', Pins(txd, dir = 'o', conn = conn)),
	]

	if rx_dv is not None and rx_err is not None:
		assert rx_ctl is None
		ios.append(Subsignal('rx_dv', Pins(rx_dv, dir = 'i', conn = conn, assert_width = 1)))
		ios.append(Subsignal('rx_err', Pins(rx_err, dir = 'i', conn = conn, assert_width = 1)))
	elif rx_ctl is not None:
		ios.append(Subsignal('rx_ctl', Pins(rx_ctl, dir = 'i', conn = conn, assert_width = 1)))
	else:
		raise AssertionError('Must specify either MII RXDV + RXER pins or RGMII RXCTL')

	if tx_en is not None and tx_err is not None:
		assert tx_ctl is None
		ios.append(Subsignal('tx_en', Pins(tx_en, dir = 'o', conn = conn, assert_width = 1)))
		ios.append(Subsignal('tx_err', Pins(tx_err, dir = 'o', conn = conn, assert_width = 1)))
	elif tx_ctl is not None:
		ios.append(Subsignal('tx_ctl', Pins(tx_ctl, dir = 'o', conn = conn, assert_width = 1)))
	else:
		raise AssertionError('Must specify either MII TXDV + TXER pins or RGMII TXCTL')

	assert (rx_dv is not None and rx_err is not None) == (tx_en is not None and tx_err is not None)
	assert (rx_ctl is not None) == (tx_ctl is not None)

	if mdc is not None and mdio is not None:
		ios.append(Subsignal('mdc', Pins(mdc, dir = 'o', conn = conn, assert_width = 1), mdio_attrs))
		ios.append(Subsignal('mdio', Pins(mdio, dir = 'io', conn = conn, assert_width = 1), mdio_attrs))
	if attrs is not None:
		ios.append(attrs)
	return Resource.family(*args, default_name = 'eth', ios = ios)

def CANResource(*args, rx, tx, conn = None, attrs = None):
	ios = [
		Subsignal('rx', Pins(rx, dir = 'o', conn = conn)),
		Subsignal('tx', Pins(tx, dir = 'o', conn = conn)),
	]
	if attrs is not None:
		ios.append(attrs)
	return Resource.family(*args, default_name = 'can', ios = ios)

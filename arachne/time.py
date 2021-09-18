# SPDX-License-Identifier: BSD-3-Clause

__all__(
	'ps_to_s',
	'ns_to_s',
	'us_to_s',
	'ms_to_s',
)

ps = 1e-12
ns = 1e-9
us = 1e-6
ms = 1e-3

def ps_to_s(val):
	return val * ps

def ns_to_s(val):
	return val * ns

def us_to_s(val):
	return val * us

def ms_to_s(val):
	return val * ms

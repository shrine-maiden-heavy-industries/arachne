# SPDX-License-Identifier: BSD-3-Clause
from nmigen.build import *

from ..mio        import _PS7_MIO_MAPPING
from .ethernet    import EthernetResource
from .i2c         import I2CResource

__all__ = (
	'PS7CoreResource',
	'PS7DDR3Resource',
	'EthernetResource',
	'I2CResource',
)

_ddr3_name_map = {
	'rst': 'drst_n',
	'clk_p': 'ckp',
	'clk_n': 'ckn',
	'clk_en': 'cke',
	'cs': 'cs_n',
	'we': 'we_n',
	'ras': 'ras_n',
	'cas': 'cas_n',
	'a': 'a',
	'ba': 'na',
	'dqs_p': 'dqs_p',
	'dqs_n': 'dqs_n',
	'dq': 'dq',
	'dm': 'dm',
	'odt': 'odt',
}

def PS7CoreResource(*args, device, package, clk_freq, conn = None):
	mapping = _PS7_MIO_MAPPING[(device, package)]['core']
	ios = [
		Subsignal('clk', Pins(mapping['clk'], dir = 'i', conn = conn), Clock(clk_freq), Attrs(IOSTANDARD = 'LVCMOS33')),
		Subsignal('por_n', Pins(mapping['por_n'], dir = 'i', conn = conn), Attrs(IOSTANDARD = 'LVCMOS33')),
		Subsignal('srst_n', Pins(mapping['srst_n'], dir = 'i', conn = conn), Attrs(IOSTANDARD = 'LVCMOS18')),
	]
	return Resource.family(*args, default_name = 'ps7_core', ios = ios)

def PS7DDR3Resource(*args, device, package, ddr3 : Resource, conn = None):
	mapping = _PS7_MIO_MAPPING[(device, package)]['ddr']

	def validate(name, xilinx_name, pins):
		if len(pins) > 1:
			for i, pin in enumerate(pins):
				ps7_pin = mapping[f'{xilinx_name}{i}']
				if ps7_pin != pin:
					raise ValueError(f'Pin {name}{i} is incorrectly mapped to {pin}, should be {ps7_pin}')
		else:
			ps7_pin = mapping[xilinx_name]
			if ps7_pin != pins[0]:
				raise ValueError(f'Pin {name} is incorrectly mapped to {pins[0]}, should be {ps7_pin}')

	for subsignal in ddr3.ios:
		if not isinstance(subsignal, Subsignal):
			continue
		elif subsignal.name == 'clk':
			clk = subsignal
		elif subsignal.name == 'dqs':
			dqs = subsignal

		pin = subsignal.ios[0]
		if isinstance(pin, Pins):
			name = subsignal.name
			validate(name, _ddr3_name_map[name], pin.names)
		elif isinstance(pin, DiffPairs):
			name = f'{subsignal.name}_p'
			validate(name, _ddr3_name_map[name], pin.p.names)
			name = f'{subsignal.name}_n'
			validate(name, _ddr3_name_map[name], pin.n.names)

	ddr3.ios.remove(clk)
	ddr3.ios.remove(dqs)

	ios = [
		*ddr3.ios,
		Subsignal('clk_p', clk.ios[0].p),
		Subsignal('clk_n', clk.ios[0].n),
		Subsignal('dqs_p', dqs.ios[0].p),
		Subsignal('dqs_n', dqs.ios[0].n),
		Subsignal('vref_p', Pins(mapping['vrp'], dir = 'i', conn = conn, assert_width=1)),
		Subsignal('vref_n', Pins(mapping['vrn'], dir = 'i', conn = conn, assert_width=1)),
		ddr3.attrs
	]
	return Resource.family(*args, default_name = 'ps7_ddr3', ios = ios)

#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-3-Clause
from typing import List, Tuple
from nmigen import *
from nmigen.build import *
from nmigen.hdl.ir import Elaboratable
from nmigen_boards.arty_z7 import ArtyZ720Platform
from nmigen_boards.resources.memory import DDR3Resource, SDCardResources
from nmigen_boards.resources.interface import UARTResource, ULPIResource

from pathlib import Path
from sys import path
path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from arachne.resources.interface import JTAGResource
from arachne.hdl.xilinx.ps7 import *

class ArtyZ720PS7Platform(ArtyZ720Platform):
	resources = ArtyZ720Platform.resources + [
		PS7CoreResource(0,
			device = ArtyZ720Platform.device,
			package = ArtyZ720Platform.package,
			clk_freq = 50e6
		),

		JTAGResource(0,
			tck = 'F9', tms = 'J6', tdi = 'G6', tdo = 'F6',
			attrs = Attrs(IOSTANDARD = 'LVCMOS33')
		),

		PS7DDR3Resource(0,
			device = ArtyZ720Platform.device,
			package = ArtyZ720Platform.package,
			ddr3 = DDR3Resource(0,
				rst_n =  'B4',
				clk_p =  'L2',
				clk_n =  'M2',
				clk_en = 'N3',
				cs_n =   'N1',
				we_n =   'M5',
				ras_n =  'P4',
				cas_n =  'P5',
				a =      'N2 K2 M3 K3 M4 L1 L4 K4 K1 J4 F5 G4 E4 D4 F4',
				ba =     'L5 R4 J5',
				dqs_p =  'C2 G2',
				dqs_n =  'B2 F2',
				dq =     'C3 B3 A2 A4 D3 D1 C1 E1 E2 E3 G3 H3 J3 H2 H1 J1',
				dm =     'A1 F1',
				odt =    'N5',
				diff_attrs = Attrs(IOSTANDARD = 'SSTL15'),
				attrs = Attrs(IOSTANDARD = 'SSTL15')
			),
		),

		UARTResource(0,
			rx =    'C5',
			tx =    'C8',
			attrs = Attrs(IOSTANDARD = 'LVCMOS33')
		),

		ULPIResource(0,
			data =    'A14 D15 A12 F12 C16 A10 E13 C18',
			clk =     'A11',
			clk_dir = 'i',
			dir =     'C13',
			nxt =     'E16',
			stp =     'C15',
			attrs =   Attrs(IOSTANDARD = 'LVCMOS18')
		),

		*SDCardResources(0,
			clk =   'D14',
			cmd =   'C17',
			dat0 =  'E12',
			dat1 =  'A9',
			dat2 =  'F13',
			dat3 =  'B15',
			cd =    'B14',
			attrs = Attrs(IOSTANDARD = 'LVCMOS18')
		),
	]

	def __init__(self, *args, **kwargs):
		from arachne.hdl.xilinx.ps7.mio import _PS7_MIO_MAPPING
		self._mapping = self._flatten_mapping(_PS7_MIO_MAPPING[self.device, self.package])
		super().__init__(*args, *kwargs)

	@staticmethod
	def _flatten_mapping(mapping : dict) -> list:
		flat_map = {'mio': [], 'other': []}
		for pinset in mapping.values():
			if isinstance(pinset, dict):
				flat_map['other'].extend(pinset.values())
			elif isinstance(pinset, list):
				for _, pad in pinset:
					flat_map['mio'].append(pad)
		return flat_map

	def _demap_pin(self, pin : Record) -> Tuple[str, int, str]:
		parts = pin.name.split('__', maxsplit = 1)
		name, number = parts[0].rsplit('_', maxsplit = 1)
		return (name, int(number), parts[1])

	def _find_subsignal(self, resource : Resource, name : str) -> Subsignal:
		for subsig in resource.ios:
			if subsig.name == name:
				return subsig
		raise KeyError('Subsignal not found')

	def _map_pin_to_pad(self, pin : Record) -> str:
		name, number, subsignal = self._demap_pin(pin)
		resource = self.lookup(name, number)
		subsignal = self._find_subsignal(resource, subsignal)
		for part in subsignal.ios:
			if isinstance(part, Pins):
				return part.names[0]
		raise ValueError('Failed to map pin to pad')

	def get_input(self, pin, port, attrs, invert):
		pad = self._map_pin_to_pad(pin)
		if pad not in self._mapping['mio'] and pad not in self._mapping['other']:
			return super().get_input(pin, port, attrs, invert)
		print(f'Bidi-mapping pin {pin} ({pad})')
		self._check_feature("single-ended input", pin, attrs,
							valid_xdrs=self._get_valid_xdrs(), valid_attrs=True)
		m = Module()
		if pad in self._mapping['other']:
			i = Signal(pin.width)
			m.d.comb += pin.i.eq(self._invert_if(invert, i))
			for bit in range(pin.width):
				m.submodules["{}_{}".format(pin.name, bit)] = Instance(
					'BIBUF',
					io_PAD = port.io[bit],
					o_IO = i[bit]
				)
		return m

	def get_output(self, pin, port, attrs, invert):
		pad = self._map_pin_to_pad(pin)
		if pad not in self._mapping['mio'] and pad not in self._mapping['other']:
			return super().get_output(pin, port, attrs, invert)
		print(f'Bidi-mapping pin {pin} ({pad})')
		self._check_feature("single-ended output", pin, attrs,
							valid_xdrs=self._get_valid_xdrs(), valid_attrs=True)
		m = Module()
		# o = Signal(pin.width)
		# o = self._invert_if(invert, pin.o)
		# i, o, t = self._get_xdr_buffer(m, pin, attrs.get("IOSTANDARD"), i_invert=invert)
		# for bit in range(pin.width):
		# 	m.submodules["{}_{}".format(pin.name, bit)] = Instance(
		# 		'BIBUF',
		# 		io_PAD = port.io[bit],
		# 		i_IO = o[bit]
		# 	)
		return m

	def get_input_output(self, pin, port, attrs, invert):
		pad = self._map_pin_to_pad(pin)
		if pad not in self._mapping['mio'] and pad not in self._mapping['other']:
			return super().get_input_output(pin, port, attrs, invert)
		print(f'Bidi-mapping pin {pin} ({pad})')
		self._check_feature("single-ended input/output", pin, attrs,
							valid_xdrs=self._get_valid_xdrs(), valid_attrs=True)
		m = Module()
		if pad in self._mapping['other']:
			assert invert == False, "Cannot invert an inout pin"
			for bit in range(pin.width):
				m.submodules["{}_{}".format(pin.name, bit)] = Instance(
					'BIBUF',
					io_PAD = port.io[bit],
					io_IO = pin.i[bit]
				)
		return m

	def _mio_translate(self, pad) -> str:
		from arachne.hdl.xilinx.ps7.mio import _PS7_MIO_MAPPING
		mapping = _PS7_MIO_MAPPING[self.device, self.package]['mio']
		for bit, pad_name in mapping:
			if pad == pad_name:
				return f'mio[{bit}]'

	def iter_port_constraints_bits(self):
		from arachne.hdl.xilinx.ps7.mio import _PS7_MIO_MAPPING
		mio_attrs = {}

		for port_name, pin_names, attrs in self.iter_port_constraints():
			if len(pin_names) == 1:
				if pin_names[0] in self._mapping['mio']:
					mio_attrs[pin_names[0]] = attrs
				else:
					yield port_name, pin_names[0], attrs
			else:
				for bit, pin_name in enumerate(pin_names):
					if pin_name in self._mapping['mio']:
						mio_attrs[pin_name] = attrs
					else:
						yield f'{port_name}[{bit}]', pin_name, attrs

		mapping = _PS7_MIO_MAPPING[self.device, self.package]['mio']
		for bit, pin_name in mapping:
			yield f'mio[{bit}]', pin_name, mio_attrs.get(pin_name, {}) # TODO: IO directions and voltages..?

class System(Elaboratable):
	def elaborate(self, platform):
		m = Module()
		m.submodules.ps7 = ps7 = PS7(core = platform.request('ps7_core'))

		#ps7.add_resource(name = 'ddr', resource = platform.request('ps7_ddr3'))
		#ps7.add_resource(name = 'jtag', resource = platform.request('jtag'))
		ps7.add_resource(name = 'usb0', resource = platform.request('usb'))
		ps7.add_resource(name = 'sdio0', resource = platform.request('sd_card_4bit'))

		return m

if __name__ == '__main__':
	platform = ArtyZ720PS7Platform()
	platform.build(System(), name = 'ps7_artyz7')

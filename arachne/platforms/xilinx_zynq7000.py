# SPDX-License-Identifier: BSD-3-Clause
from typing                       import Tuple
from nmigen                       import *
from nmigen.build                 import *
from nmigen.vendor.xilinx_7series import *

from ..hdl.xilinx.ps7.mio import _PS7_MIO_MAPPING

__all__ = ('XilinxZynq7000Platform',)

class XilinxZynq7000Platform(Xilinx7SeriesPlatform):
	def __init__(self, *args, **kwargs):
		self._mapping = self._flatten_mapping(_PS7_MIO_MAPPING[self.device, self.package])
		super().__init__(*args, *kwargs)

	@staticmethod
	def _flatten_mapping(mapping : dict) -> list:
		flat_map = {'mio': [], 'other': []}
		for key, pinset in mapping.items():
			if key == 'mio_banks':
				continue
			if isinstance(pinset, dict):
				flat_map['other'].extend(pinset.values())
			elif isinstance(pinset, list):
				for _, pad in pinset:
					flat_map['mio'].append(pad)
		return flat_map

	def _demap_pin(self, pin : Record) -> Tuple[str, int, str]:
		parts = pin.name.split('__', maxsplit = 1)
		name, number = parts[0].rsplit('_', maxsplit = 1)
		if len(parts) == 1:
			return (name, int(number), name)
		return (name, int(number), parts[1])

	def _find_subsignal(self, resource : Resource, name : str) -> Subsignal:
		if resource.name == name:
			return resource
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

	# Support both the current upstream behaviour and MWK's unified Xilinx patch
	# (https://github.com/nmigen/nmigen/pull/563)
	def _get_valid_xdrs(self):
		if hasattr(super(), '_get_valid_xdrs'):
			return super()._get_valid_xdrs()
		return (0, 1, 2)

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
		mapping = _PS7_MIO_MAPPING[self.device, self.package]['mio']
		for bit, pad_name in mapping:
			if pad == pad_name:
				return f'mio[{bit}]'

	def iter_port_constraints_bits(self):
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

		banks = _PS7_MIO_MAPPING[self.device, self.package]['mio_banks']
		mapping = _PS7_MIO_MAPPING[self.device, self.package]['mio']

		for bank in banks.values():
			attrs = []
			for mio in bank['mios']:
				_, pin = mapping[mio]
				if pin in mio_attrs:
					attrs.append(mio_attrs[pin])

			io_standards = set()
			for attr in attrs:
				for key, value in attr.items():
					if key != 'IOSTANDARD':
						continue
					io_standards.add(value)

			assert len(io_standards) <= 1, f'Cannot mix IO standards on a bank, have {io_standards}'
			if len(io_standards) == 1:
				io_standard = io_standards.pop()
			else:
				io_standard = bank['default_standard']

			for mio in bank['mios']:
				_, pin = mapping[mio]
				mio_attrs.setdefault(pin, Attrs(IOSTANDARD=io_standard))

		for bit, pin_name in mapping:
			yield f'mio[{bit}]', pin_name, mio_attrs.get(pin_name) # TODO: IO directions..?

# SPDX-License-Identifier: BSD-3-Clause
import enum

__all__ = (
	'AXIBusType',
	'AXIChannelType',
	'AXIInterfaceType',
)

@enum.unique
class AXIChannelType(enum.Enum):
	Read  = enum.auto()
	Write = enum.auto()

@enum.unique
class AXIInterfaceType(enum.Enum):
	Manager     = enum.auto()
	Subordinate = enum.auto()

@enum.unique
class AXIBusType(enum.Enum):
	Lite = enum.auto()
	Full = enum.auto()

	def __str__(self):
		return self.name

	@staticmethod
	def from_str(s):
		try:
			return AXIBusType[s]
		except KeyError:
			raise ValueError(f'Unknown AXI bus type value {s}')

def _check_id_width(*, id_width, bus_type):
	if not isinstance(id_width, int) or id_width < 0:
		raise ValueError(f'id_width must be a non negative integer, not {id_width}')

def _check_addr_width(*, addr_width):
	if not isinstance(addr_width, int) or addr_width not in (
		8, 16, 32, 64, 128, 256, 512, 1024
	):
		raise ValueError(f'addr_width must be either 8, 16, 32, 64, 128, 256, 512, 1024, not {addr_width}')

def _check_data_width(*, data_width, bus_type):
	if bus_type == AXIBusType.Full:
		if not isinstance(data_width, int) or data_width not in (
			8, 16, 32, 64, 128, 256, 512, 1024
		):
			raise ValueError(f'data_width must be either 8, 16, 32, 64, 128, 256, 512, 1024, not {addr_width}')
	else:
		if not isinstance(data_width, int) or data_width not in (
			32, 64
		):
			raise ValueError(f'data_width must be either 32 or 64, for AXI Lite not {addr_width}')

def _check_widths(*, addr_width, data_width, id_width, bus_type):
	_check_addr_width(addr_width = addr_width)
	_check_data_width(data_width = data_width, bus_type = bus_type)
	_check_id_width(id_width = id_width, bus_type = bus_type)


def _check_features(*, features):
	unknown = set(features) - {
		'atomic', 'qos', 'region'
	}

	if unknown:
		raise ValueError(f'Optional feature(s) {", ".join(map(repr, unknown))} are not supported')

def _check_interface(*,
	addr_width, data_width, id_width,
	bus_type, interface_type,
	features
):
	_check_widths(
		addr_width = addr_width, data_width = data_width,
		id_width = id_width, bus_type = bus_type
	)

	if not isinstance(bus_type, AXIBusType):
		raise ValueError(f'bus_type must be of type AXIBusType and not {type(interface_type)}')

	if not isinstance(interface_type, AXIInterfaceType):
		raise ValueError(f'interface_type must be of type InterfaceType and not {type(interface_type)}')

	_check_features(features = features)

def _check_channel(*,
	addr_width, data_width, id_width,
	bus_type, interface_type, channel_type,
	features
):
	_check_interface(
		addr_width = addr_width, data_width = data_width, id_width = id_width,
		bus_type = bus_type, interface_type = interface_type,
		features = features
	)

	if not isinstance(channel_type, AXIChannelType):
		raise ValueError(f'channel_type must be of type ChannelType not {type(channel_type)}')

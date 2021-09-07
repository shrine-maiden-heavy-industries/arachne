# SPDX-License-Identifier: BSD-3-Clause
from nmigen   import *

from .common  import *
from .common  import _check_interface

from .channel import *

__all__ = (
	'Interface',
)

# NOTE: Records are planned to be deprecated from nMigen in the future
class Interface(Record):
	"""AMBA4 AXI Interface

	See the `AMBA AXI and ACE Protocol Specification <https://developer.arm.com/documentation/ihi0022/e/?lang=en>`_ for a full description of all of the
	signals.

	This record defines the full interface to the AXI bus based on the AXI version.

	Parameters
	----------
	addr_width : int
		The width of the AXI address bus. (either 8, 16, 32, 64, 128, 256, 512, or 1024 unless bypass_width_check is set)

	data_width : int
		The width of the AXI data bus. (either 8, 16, 32, 64, 128, 256, 512, or 1024 unless bypass_width_check is set)

	id_width : int
		The width of the AXI address bus. (must be a positive non-zero value unless bypass_width_check is set)

	bus_type : AXIBusType
		The type of AXI bus the interface describes.

	interface_type : AXIInterfaceType
		The type of interface, either a Manager or Subordinate.

	features : iter(str)
		The collection of optional features enabled for this interface.
		 * 'atomic' - Atomic transactions
		 * 'qos' - Quality Of Service
		 * 'region' - Region signaling

	name : str
		The name of this interface


	Attributes
	----------
	clk : Signal
		The AXI bus clock

	rst_n : Signal
		The AXI bus reset line


	Additional attributes are added depending on  the ``bus_type``, for each channel type.
	see the documentation for ``Channel`` for a list of and in which case these
	additional attributes will be added.

	"""
	def __init__(self, *,
		addr_width, data_width, id_width,
		bus_type, interface_type,
		features = frozenset(),
		name = None
	):
		_check_interface(
			addr_width = addr_width, data_width = data_width, id_width = id_width,
			bus_type = bus_type, interface_type = interface_type,
			features = features
		)

		self.addr_width = addr_width
		self.data_width = data_width
		self.id_width   = id_width

		self.bus_type       = bus_type
		self.interface_type = interface_type

		self.features       = features

		self.read_channel = Channel(
			addr_width = self.addr_width, data_width = self.data_width, id_width = self.id_width,
			bus_type = self.bus_type, interface_type = self.interface_type, channel_type = AXIChannelType.Read,
			features = self.features,
			name = f'{name}_read_channel'
		)

		self.write_channel = Channel(
			addr_width = self.addr_width, data_width = self.data_width, id_width = self.id_width,
			bus_type = self.bus_type, interface_type = self.interface_type, channel_type = AXIChannelType.Write,
			features = self.features,
			name = f'{name}_read_channel'
		)

		layout = [
			('clk',   1),
			('rst_n', 1)
		] + list(self.read_channel.layout) + list(self.write_channel.layout)

		super().__init__(layout, name = name, src_loc_at = 1)

# SPDX-License-Identifier: BSD-3-Clause
from amaranth         import *
from amaranth.hdl.rec import Direction

from .common          import *
from .common          import _check_channel

__all__ = (
	'Channel',
)

# NOTE: Records are planned to be deprecated from nMigen in the future
class Channel(Record):
	"""AMBA4 AXI Channel

	See the `AMBA AXI and ACE Protocol Specification <https://developer.arm.com/documentation/ihi0022/e/?lang=en>`_ for a full description of all of the
	signals.

	This record defines the signals and their direction based on ``chanel_type`` and ``interface_type``.

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

	channel_type : AXIChannelType
		The type of channel this record represents, either Read or Write

	features : iter(str)
		The collection of optional features enabled for this interface.
		 * 'atomic' - Atomic transactions
		 * 'qos' - Quality Of Service
		 * 'region' - Region signaling

	name : str
		The name of this interface

	Attributes
	----------
	When ``channel_type`` is ``AXIChannelType.Read`` and ``bus_type`` is ``AXIBusType.Lite`` the following signals are present

	arvalid : Signal(1)
		Indicates if channel address signals are valid

	arready : Signal(1)
		Indicates that a transfer on the channel is ready

	araddy : Signal(addr_width)
		Channel address

	arid : Signal(id_width)
		AXI ID tag for this channel

	rvalid : Signal(1)
		Indicates if the channel data is valid

	rready : Signal(1)
		Indicates if the channel data is ready

	rdata : Signal(data_width)
		Channel data

	rrsesp : Signal(2)
		Read response

	When ``channel_type`` is ``AXIChannelType.Read`` and ``bus_type`` is ``AXIBusType.full`` the following additional signals are present

	arprot : Signal(3)
		Protection type

	arlen : Signal(8)
		Read length

	arsize : Signal(3)
		Read size

	arburst : Signal(2)
		Read burst indicator

	arcache : Signal(4)
		Read cache control

	rid : Signal(id_width)
		Read data id

	rlast : Signal(1)
		Last read data indicator

	When ``channel_type`` is ``AXIChannelType.Read`` and ``bus_type`` is ``AXIBusType.full`` and the ``atomic` feature is enabled,
	the following additional signals are present

	arlock : Signal(1)
		If channel is locked

	When ``channel_type`` is ``AXIChannelType.Read`` and ``bus_type`` is ``AXIBusType.full`` and the ``qos` feature is enabled,
	the following additional signals are present

	arqos : Signal(4)
		Quality Of Service tag

	When ``channel_type`` is ``AXIChannelType.Read`` and ``bus_type`` is ``AXIBusType.full`` and the ``region` feature is enabled,
	the following additional signals are present

	arregion : Signal(4)
		Region address

	When ``channel_type`` is ``AXIChannelType.Write`` and ``bus_type`` is ``AXIBusType.Lite`` the following signals are present

	awvalid : Signal(1)
		Write channel address is valid

	awready : Signal(1)
		Write channel address is ready

	awaddr : Signal(addr_width)
		Write address

	awprot : Signal(3)
		Protection type

	wvalid : Signal(1)
		Write data is valid

	wready : Signal(1)
		Write data is ready

	wdata : Signal(data_width)
		Data to write

	wstrobe : Signal(data_width // 8)
		Data strobes per byte for valid data

	bvalid : Signal(1)
		Response is valid

	bready : Signal(1)
		Response is ready

	bresp : Signal(2)
		Write response


	When ``channel_type`` is ``AXIChannelType.Write`` and ``bus_type`` is ``AXIBusType.full`` the following additional signals are present

	awid : Signal(id_width)
		Write address ID

	awlen : Signal(8)
		Write address length

	awburst : Signal(2)
		Write address burst

	awcache : Signal(4)
		Write address cache control

	wid : Signal(id_width)
		Write data ID

	wlast : Signal(1)
		Last write indicator

	bid : Signal(id_width)
		Write response ID

	When ``channel_type`` is ``AXIChannelType.Write`` and ``bus_type`` is ``AXIBusType.full`` and the ``atomic` feature is enabled,
	the following additional signals are present

	awlock : Signal(1)
		If channel is locked

	When ``channel_type`` is ``AXIChannelType.Write`` and ``bus_type`` is ``AXIBusType.full`` and the ``qos` feature is enabled,
	the following additional signals are present

	awqos : Signal(4)
		Quality Of Service tag

	When ``channel_type`` is ``AXIChannelType.Write`` and ``bus_type`` is ``AXIBusType.full`` and the ``region` feature is enabled,
	the following additional signals are present

	awregion : Signal(4)
		Region address

	"""
	def __init__(self, *,
		addr_width, data_width, id_width,
		bus_type, interface_type, channel_type,
		features = frozenset(), name = None,
	):
		_check_channel(
			addr_width = addr_width, data_width = data_width, id_width = id_width,
			bus_type = bus_type, interface_type = interface_type, channel_type = channel_type,
			features = features
		)

		self.addr_width = addr_width
		self.data_width = data_width
		self.id_width   = id_width

		self.bus_type       = bus_type
		self.interface_type = interface_type
		self.channel_type   = channel_type

		self.features = set(features)

		layout = []

		if channel_type == AXIChannelType.Read:
			layout += self._assemble_read_channel(
				addr_width = self.addr_width, data_width = self.data_width, id_width = self.id_width,
				bus_type = self.bus_type, interface_type = self.interface_type,
				features = self.features
			)
		elif channel_type == AXIChannelType.Write:
			layout += self._assemble_write_channel(
				addr_width = self.addr_width, data_width = self.data_width, id_width = self.id_width,
				bus_type = self.bus_type, interface_type = self.interface_type,
				features = self.features
			)
		else:
			raise ValueError(f'channel_type is unknown value {str(channel_type)}, how did this even happen?')

		super().__init__(layout, name = name, src_loc_at = 1)

	def _fanout_if_manager(self, *,interface_type):
		if interface_type == AXIInterfaceType.Manager:
			return Direction.FANOUT
		else:
			return Direction.FANIN

	def _fanin_if_manager(self, *, interface_type):
		if interface_type == AXIInterfaceType.Manager:
			return Direction.FANIN
		else:
			return Direction.FANOUT

	def _assemble_read_channel(self, *,
		addr_width, data_width, id_width,
		bus_type, interface_type,
		features
	):
		manager_fanin  = self._fanin_if_manager(interface_type = interface_type)
		manager_fanout = self._fanout_if_manager(interface_type = interface_type)

		# Common AXI Lite and AXI Full Signals
		layout = [
			# Address
			('arvalid' , 1         , manager_fanout),
			('arready' , 1         , manager_fanin ),
			('araddr'  , addr_width, manager_fanout),
			('arid'    , id_width  , manager_fanout),
			# Data
			('rvalid'  , 1         , manager_fanin ),
			('rready'  , 1         , manager_fanout),
			('rdata'   , data_width, manager_fanin ),
			('rresp'   , 2         , manager_fanin ),
		]
		# Additional/bus type only Signals
		if bus_type == AXIBusType.Full:
			layout += [
				# Address
				('arprot'  , 3         , manager_fanout),
				('arlen'   , 8         , manager_fanout),
				('arsize'  , 3         , manager_fanout),
				('arburst' , 2         , manager_fanout),
				('arcache' , 4         , manager_fanout),
				# Data
				('rid'     , id_width  , manager_fanin ),
				('rlast'   , 1         , manager_fanin ),
			]

			if 'atomic' in self.features:
				layout += [
					('arlock'  , 1         , manager_fanout)
				]

			if 'qos' in self.features:
				layout += [
					('arqos'   , 4         , manager_fanout)
				]

			if 'region' in self.features:
				layout += [
					('arregion', 4         , manager_fanout)
				]


		elif bus_type == AXIBusType.Lite:
			layout += [
				# No known AXI lite only signals for the read channel
			]
		else:
			raise ValueError(f'bus_type is unknown value {str(bus_type)}, how did this even happen')

		return layout

	def _assemble_write_channel(self, *,
		addr_width, data_width, id_width,
		bus_type, interface_type,
		features
	):
		manager_fanin  = self._fanin_if_manager(interface_type = interface_type)
		manager_fanout = self._fanout_if_manager(interface_type = interface_type)

		# Common AXI Lite and AXI Full Signals
		layout = [
			# Address
			('awvalid', 1              , manager_fanout),
			('awready', 1              , manager_fanin ),
			('awaddr' , addr_width     , manager_fanout),
			('awprot' , 3              , manager_fanout),
			# Data
			('wvalid' , 1              , manager_fanout),
			('wready' , 1              , manager_fanin ),
			('wdata'  , data_width     , manager_fanout),
			('wstrobe', data_width // 8, manager_fanout),
			# Response
			('bvalid' , 1               , manager_fanin ),
			('bready' , 1               , manager_fanout),
			('bresp'  , 2               , manager_fanin ),

		]
		# Additional/bus type only Signals
		if bus_type == AXIBusType.Full:
			layout += [
				# Address
				('awid'    , id_width, manager_fanout),
				('awlen'   , 8       , manager_fanout),
				('awsize'  , 3       , manager_fanout),
				('awburst' , 2       , manager_fanout),
				('awcache' , 4       , manager_fanout),
				# Data
				('wid'     , id_width, manager_fanout),
				('wlast'   , 1       , manager_fanout),
				# Response
				('bid'     , id_width, manager_fanin ),
			]

			if 'atomic' in self.features:
				layout += [
					('awlock'  , 1       , manager_fanout)
				]

			if 'qos' in self.features:
				layout += [
					('awqos'   , 4       , manager_fanout)
				]

			if 'region' in self.features:
				layout += [
					('awregion', 4       , manager_fanout)
				]

		elif bus_type == AXIBusType.Lite:
			layout += [
				# No known AXI lite only signals for the write channel
			]
		else:
			raise ValueError(f'bus_type is unknown value {str(bus_type)}, how did this even happen')

		return layout

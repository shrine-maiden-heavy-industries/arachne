# SPDX-License-Identifier: BSD-3-Clause
from nmigen       import *
from nmigen.build import *


from .mio         import _PS8_MIO_MAPPING

__all__ = (
	'PS8Resource',

	'QSPIResource'
)

'''

'''

class PS8Resource(Subsignal):
	def __init__(self, name, number, *args):
		super().__init__(name, *args)

		self.number = number


def QSPIResource():
	io = []

	return PS8Resource('qspi', 0, *io, Attrs(IOSTANDARD="LVCMOS33"))

def NANDResource():
	io = []

	return PS8Resource('nand', 0, *io, Attrs(IOSTANDARD="LVCMOS33"))

def SDResource(num):
	if num > 1:
		raise ValueError(f'PS8 Only has sd0..1, not {num}')

	io = []

	return PS8Resource('sd', num, *io, Attrs(IOSTANDARD="LVCMOS33"))


def CANResource(num):
	if num > 1:
		raise ValueError(f'PS8 Only has can0..1, not {num}')

	io = []

	return PS8Resource('can', num, *io, Attrs(IOSTANDARD="LVCMOS33"))

def I2CResource(num):
	if num > 1:
		raise ValueError(f'PS8 Only has i2c0..1, not {num}')

	io = []

	return PS8Resource('i2c', num, *io, Attrs(IOSTANDARD="LVCMOS33"))

def PJTAGResource():
	io = []

	return PS8Resource('pjtag', 0, *io, Attrs(IOSTANDARD="LVCMOS33"))

def PMUResource():
	io = []

	return PS8Resource('pmu', 0, *io, Attrs(IOSTANDARD="LVCMOS33"))

def CSUResource():
	io = []

	return PS8Resource('csu', 0, *io, Attrs(IOSTANDARD="LVCMOS33"))

def I2CResource(num):
	if num > 1:
		raise ValueError(f'PS8 Only has spi0..1, not {num}')

	io = []

	return PS8Resource('spi', num, *io, Attrs(IOSTANDARD="LVCMOS33"))

def UARTResource(num):
	if num > 1:
		raise ValueError(f'PS8 Only has uart0..1, not {num}')

	io = []

	return PS8Resource('uart', num, *io, Attrs(IOSTANDARD="LVCMOS33"))

def SWDTResource(num):
	if num > 1:
		raise ValueError(f'PS8 Only has swdt0..1, not {num}')

	io = []

	return PS8Resource('swdt', num, *io, Attrs(IOSTANDARD="LVCMOS33"))

def TraceResource():
	io = []

	return PS8Resource('trace', 0, *io, Attrs(IOSTANDARD="LVCMOS33"))

def TCCResource(num):
	if num > 3:
		raise ValueError(f'PS8 Only has tcc0..3, not {num}')

	io = []

	return PS8Resource('tcc', num, *io, Attrs(IOSTANDARD="LVCMOS33"))

def GEMResource(num):
	if num > 3:
		raise ValueError(f'PS8 Only has gem0..3, not {num}')

	io = []

	return PS8Resource('gem', num, *io, Attrs(IOSTANDARD="LVCMOS33"))

def USBResource(num):
	if num > 1:
		raise ValueError(f'PS8 Only has usb0..1, not {num}')

	io = []

	return PS8Resource('usb', num, *io, Attrs(IOSTANDARD="LVCMOS33"))

def PCIEResource():
	io = []

	return PS8Resource('pcie', 0, *io, Attrs(IOSTANDARD="LVCMOS33"))

def DPResource():
	io = []

	return PS8Resource('dp', 0, *io, Attrs(IOSTANDARD="LVCMOS33"))

def SATAResource():
	io = []

	return PS8Resource('sata', 0, *io, Attrs(IOSTANDARD="LVCMOS33"))

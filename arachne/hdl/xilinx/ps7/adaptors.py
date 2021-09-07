# SPDX-License-Identifier: BSD-3-Clause
from nmigen import *

__all__ = (
	'DDR3Adaptor',
)

class DDR3Adaptor(Elaboratable):
	def __init__(self, *, bus):
		self._bus = bus

		self.rst_n = Signal()
		self.clk_p = Signal()
		self.clk_n = Signal()
		self.clk_en = Signal()
		self.cs_n = Signal()
		self.we_n = Signal()
		self.ras_n = Signal()
		self.cas_n = Signal()
		self.address = Signal(15)
		self.bank_address = Signal(3)

		self.data_strobe_p = Signal(4)
		self.data_strobe_n = Signal(4)
		self.data = Signal(32)
		self.data_mask = Signal(4)

		self.odt_en = Signal()
		self.voltage_ref_p = Signal()
		self.voltage_ref_n = Signal()

	def elaborate(self, _) -> Module:
		m = Module()
		bus = self._bus

		print(bus)

		m.d.comb += [
			bus.rst.o.eq(~self.rst_n),
			bus.clk_p.o.eq(self.clk_p),
			bus.clk_n.o.eq(self.clk_n),
			bus.clk_en.o.eq(self.clk_en),
			bus.cs.o.eq(~self.cs_n),
			bus.we.o.eq(~self.we_n),
			bus.ras.o.eq(~self.ras_n),
			bus.cas.o.eq(~self.cas_n),
			bus.a.o.eq(self.address[0:len(bus.a.o)]),
			bus.ba.o.eq(self.bank_address[0:len(bus.ba.o)]),

			bus.dqs_p.io.eq(self.data_strobe_p[0:len(bus.dqs.p.io)]),
			bus.dqs_n.io.eq(self.data_strobe_n[0:len(bus.dqs.n.io)]),
			bus.dq.io.eq(self.data[0:len(bus.dq.io)]),
			bus.dm.io.eq(self.data_mask[0:len(bus.dm.io)]),

			bus.odt.o.eq(self.odt_en),
			self.voltage_ref_p.eq(bus.vref_p.i),
			self.voltage_ref_n.eq(bus.vref_n.i),
		]
		return m

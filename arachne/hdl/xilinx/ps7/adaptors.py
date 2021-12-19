# SPDX-License-Identifier: BSD-3-Clause
from amaranth       import *
from amaranth.build import Resource

__all__ = (
	'DDR3Adaptor', 'GMIItoRGMII'
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

	def elaborate(self, platform) -> Module:
		m = Module()
		bus = self._bus

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

			bus.dqs_p.o.eq(self.data_strobe_p[0:len(bus.dqs_p.o)]),
			bus.dqs_n.o.eq(self.data_strobe_n[0:len(bus.dqs_n.o)]),
			bus.dq.o.eq(self.data[0:len(bus.dq.o)]),
			bus.dm.o.eq(self.data_mask[0:len(bus.dm.o)]),

			bus.odt.o.eq(self.odt_en),
			self.voltage_ref_p.eq(bus.vref_p.i),
			self.voltage_ref_n.eq(bus.vref_n.i),
		]
		return m

class GMIItoRGMII(Elaboratable):
	def __init__(self, *, rgmii : Resource):
		self.rx_clk = Signal()
		self.rx = Signal(8)
		self.rx_dv = Signal()
		self.rx_err = Signal()

		self.tx_clk = Signal()
		self.tx = Signal(8)
		self.tx_en = Signal()
		self.tx_err = Signal()

		self._iface = rgmii

	def elaborate(self, platform):
		m = Module()
		eth = self._iface

		m.d.comb += [
			self.rx_clk.eq(eth.rx_clk.i),

			self.rx[0:4].eq(eth.rx_dat.i0),
			self.rx[4:8].eq(eth.rx_dat.i1),
			eth.rx_dat.i_clk.eq(eth.rx_clk.i),

			self.rx_dv.eq(eth.rx_ctl.i0),
			self.rx_err.eq(eth.rx_ctl.i0 ^ eth.rx_ctl.i1),
			eth.rx_ctl.i_clk.eq(eth.rx_clk.i),

			self.tx_clk.eq(eth.tx_clk.i),

			eth.tx_dat.o0.eq(self.tx[0:4]),
			eth.tx_dat.o1.eq(self.tx[4:8]),
			eth.tx_dat.o_clk.eq(eth.tx_clk.i),

			eth.tx_ctl.o0.eq(self.tx_en),
			eth.tx_ctl.o1.eq(self.tx_en ^ self.tx_err),
			eth.tx_ctl.o_clk.eq(eth.tx_clk.i),
		]

		return m

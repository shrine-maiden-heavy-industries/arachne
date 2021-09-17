# SPDX-License-Identifier: BSD-3-Clause
from nmigen         import *
from nmigen.hdl.rec import (DIR_FANIN, DIR_FANOUT)

from .common        import *
from ..adaptors     import GMIItoRGMII

__all__ = (
	'EthernetResource'
)

class EthernetResource(PS7Resource):
	name = 'eth',
	claimable_mio = (
		(
			(MIOSet.MIO16, MIOSet.MIO27),
			(MIOSet.MIO52, MIOSet.MIO53),
		),
		(
			(MIOSet.MIO28, MIOSet.MIO39),
			(MIOSet.MIO52, MIOSet.MIO53),
		)
	)

	signals = (
		('rx_clk',  1, DIR_FANIN),
		('rx',      8, DIR_FANIN),
		('rx_dv',   1, DIR_FANIN),
		('rx_err',  1, DIR_FANIN),

		('tx_clk',  1, DIR_FANIN),
		('tx',      8, DIR_FANOUT),
		('tx_en',   1, DIR_FANOUT),
		('tx_err',  1, DIR_FANOUT),
		('col',     1, DIR_FANIN),
		('crs',     1, DIR_FANIN),

		('mdc',     1, DIR_FANOUT),
		('mdio_i',  1, DIR_FANIN),
		('mdio_o',  1, DIR_FANOUT),
		('mdio_oe', 1, DIR_FANOUT),
	)

	def __init__(self, num, *, emio = None, enable_mdio : bool = False):
		if emio is not None and enable_mdio:
			raise AssertionError(f'Cannot enable both EMIO for {self.name}{num} and the MIO MDIO pins')
		if num <= 1:
			if enable_mdio:
				mio = self.claimable_mio[num]
			elif emio is None:
				mio = self.claimable_mio[num][0]
			else:
				mio = MIOSet.EMIO

		if mio == MIOSet.EMIO and emio is True:
			layout = self.signals
			self._emio = None
		else:
			layout = ()
			self._emio = emio

		super().__init__(num = num, rnum_max = 1, mio_set = mio, allow_emio = True, layout = layout)

	def generate_mapping(self, m : Module) -> dict:
		num = self.number
		mdio_oe_n = Signal()

		if self._mios != MIOSet.EMIO:
			resource = Record(self.signals, name = f'eth_{num}')
			m.d.comb += resource.mdio_oe.eq(~mdio_oe_n)
			return {
				f'i_EMIOENET{num}GMIIRXCLK': resource.rx_clk,
				f'i_EMIOENET{num}GMIIRXD':   resource.rx,
				f'i_EMIOENET{num}GMIIRXDV':  resource.rx_dv,
				f'i_EMIOENET{num}GMIIRXER':  resource.rx_err,

				f'i_EMIOENET{num}GMIITXCLK': resource.tx_clk,
				f'o_EMIOENET{num}GMIITXD':   resource.tx,
				f'o_EMIOENET{num}GMIITXEN':  resource.tx_en,
				f'o_EMIOENET{num}GMIITXER':  resource.tx_err,
				f'i_EMIOENET{num}GMIICOL':   resource.col,
				f'i_EMIOENET{num}GMIICRS':   resource.crs,

				f'o_EMIOENET{num}MDIOMDC':   resource.mdc,
				f'i_EMIOENET{num}MDIOI':     resource.mdio_i,
				f'o_EMIOENET{num}MDIOO':     resource.mdio_o,
				f'o_EMIOENET{num}MDIOTN':    mdio_oe_n,
			}
		elif self._emio is None:
			m.d.comb += self.mdio_oe.eq(~mdio_oe_n)
			return {
				f'i_EMIOENET{num}GMIIRXCLK': self.rx_clk,
				f'i_EMIOENET{num}GMIIRXD':   self.rx,
				f'i_EMIOENET{num}GMIIRXDV':  self.rx_dv,
				f'i_EMIOENET{num}GMIIRXER':  self.rx_err,

				f'i_EMIOENET{num}GMIITXCLK': self.tx_clk,
				f'o_EMIOENET{num}GMIITXD':   self.tx,
				f'o_EMIOENET{num}GMIITXEN':  self.tx_en,
				f'o_EMIOENET{num}GMIITXER':  self.tx_err,
				f'i_EMIOENET{num}GMIICOL':   self.col,
				f'i_EMIOENET{num}GMIICRS':   self.crs,

				f'o_EMIOENET{num}MDIOMDC':   self.mdc,
				f'i_EMIOENET{num}MDIOI':     self.mdio_i,
				f'o_EMIOENET{num}MDIOO':     self.mdio_o,
				f'o_EMIOENET{num}MDIOTN':    mdio_oe_n,
			}
		else:
			eth = self._emio
			rx_domain = f'eth{num}_rx'
			tx_domain = f'eth{num}_tx'

			rx_clk = Signal()
			rx = Signal(8)
			rx_dv = Signal()
			rx_err = Signal()

			tx_clk = Signal()
			tx = Signal(8)
			tx_en = Signal()
			tx_err = Signal()
			col = Signal()
			crs = Signal()

			m.domains += ClockDomain(rx_domain)
			m.domains += ClockDomain(tx_domain)

			m.d.comb += [
				ClockSignal(rx_domain).eq(rx_clk),
				ClockSignal(tx_domain).eq(tx_clk),
			]

			# Apparently the Ethernet is miss-timed and requires a pipeline stage inserting.
			# RGMII
			if hasattr(eth, 'rx_ctl'):
				m.submodules[f'rgmii{num}'] = converter = GMIItoRGMII(rgmii = eth)

				m.d.comb += [
					rx_clk.eq(converter.rx_clk),
					tx_clk.eq(converter.tx_clk),
				]

				m.d[rx_domain] += [
					rx.eq(converter.rx),
					rx_dv.eq(converter.rx_dv),
					rx_err.eq(converter.rx_err),
				]

				m.d[tx_domain] += [
					converter.tx.eq(tx),
					converter.tx_en.eq(tx_en),
					converter.tx_err.eq(tx_err),
				]
			# GMII
			else:
				m.d.comb += [
					rx_clk.eq(eth.rx_clk.i),
					tx_clk.eq(eth.tx_clk.i),
				]

				m.d[rx_domain] += [
					rx.eq(eth.rx.i),
					rx_dv.eq(eth.rx_dv.i),
					rx_err.eq(eth.rx_err.i),
				]

				m.d[tx_domain] += [
					eth.tx.o.eq(tx),
					eth.tx_en.o.eq(tx_en),
					eth.tx_err.o.eq(tx_err),
				]
				if hasattr(eth, 'col'):
					m.d[tx_domain] += col.eq(eth.col.i)
				if hasattr(eth, 'crs'):
					m.d[tx_domain] == crs.eq(eth.crs.i)

			mdc = eth.mdc.o if hasattr(eth, 'mdc') else Signal()
			mdio_i = eth.mdio.i if hasattr(eth, 'mdio') else Signal()
			mdio_o = eth.mdio.o if hasattr(eth, 'mdio') else Signal()
			mdio_oe_n = Signal()

			if hasattr(eth, 'mdio'):
				m.d.comb += eth.mdio.oe.eq(~mdio_oe_n)

			return {
				f'i_EMIOENET{num}GMIIRXCLK': rx_clk,
				f'i_EMIOENET{num}GMIIRXD':   rx,
				f'i_EMIOENET{num}GMIIRXDV':  rx_dv,
				f'i_EMIOENET{num}GMIIRXER':  rx_err,

				f'i_EMIOENET{num}GMIITXCLK': tx_clk,
				f'o_EMIOENET{num}GMIITXD':   tx,
				f'o_EMIOENET{num}GMIITXEN':  tx_en,
				f'o_EMIOENET{num}GMIITXER':  tx_err,
				f'i_EMIOENET{num}GMIICOL':   col,
				f'i_EMIOENET{num}GMIICRS':   crs,

				f'o_EMIOENET{num}MDIOMDC':   mdc,
				f'i_EMIOENET{num}MDIOI':     mdio_i,
				f'o_EMIOENET{num}MDIOO':     mdio_o,
				f'o_EMIOENET{num}MDIOTN':    mdio_oe_n,
			}

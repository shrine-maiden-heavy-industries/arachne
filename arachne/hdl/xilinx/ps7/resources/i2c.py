# SPDX-License-Identifier: BSD-3-Clause
from nmigen         import *
from nmigen.hdl.rec import (DIR_FANIN, DIR_FANOUT)

from .common        import *

__all__ = (
	'I2CResource',
)

class I2CResource(PS7Resource):
	name = 'i2c'
	claimable_mio = {
		0: (
			(MIOSet.MIO10, MIOSet.MIO11),
			(MIOSet.MIO14, MIOSet.MIO15),
			(MIOSet.MIO18, MIOSet.MIO19),
			(MIOSet.MIO22, MIOSet.MIO23),
			(MIOSet.MIO26, MIOSet.MIO27),
			(MIOSet.MIO30, MIOSet.MIO31),
			(MIOSet.MIO34, MIOSet.MIO35),
			(MIOSet.MIO38, MIOSet.MIO39),
			(MIOSet.MIO42, MIOSet.MIO43),
			(MIOSet.MIO46, MIOSet.MIO47),
			(MIOSet.MIO50, MIOSet.MIO51),
		),
		1: (
			(MIOSet.MIO12, MIOSet.MIO13),
			(MIOSet.MIO16, MIOSet.MIO17),
			(MIOSet.MIO20, MIOSet.MIO21),
			(MIOSet.MIO24, MIOSet.MIO25),
			(MIOSet.MIO28, MIOSet.MIO29),
			(MIOSet.MIO32, MIOSet.MIO33),
			(MIOSet.MIO36, MIOSet.MIO37),
			(MIOSet.MIO40, MIOSet.MIO41),
			(MIOSet.MIO44, MIOSet.MIO45),
			(MIOSet.MIO48, MIOSet.MIO49),
			(MIOSet.MIO52, MIOSet.MIO53),
		),
	}

	signals = (
		('scl_i',  1, DIR_FANIN),
		('scl_o',  1, DIR_FANOUT),
		('scl_oe', 1, DIR_FANOUT),
		('sda_i',  1, DIR_FANIN),
		('sda_o',  1, DIR_FANOUT),
		('sda_oe', 1, DIR_FANOUT),
	)

	def __init__(self, num, *, mios = None, emio = None):
		assert (mios is not None and emio is None) or (mios is None and emio is not None)
		if mios is not None:
			self._validate_mios(num, mios)
			mio = mios
		elif emio is not None:
			mio = MIOSet.EMIO
		else:
			layout = self.signals
			mio = MIOSet.EMIO

		if mio == MIOSet.EMIO and emio is True:
			layout = self.signals
			self._emio = None
		else:
			layout = ()
			self._emio = emio

		super().__init__(num = num, rnum_max = 1, mio_set = mio, allow_emio = True, layout = layout)

	def _validate_mios(self, num, mios):
		assert num in self.claimable_mio
		assert isinstance(mios, (tuple, list)) and len(mios) == 2
		valid_mios = self.claimable_mio[num]
		begin, end = mios

		for valid_begin, valid_end in valid_mios:
			if valid_begin == begin and valid_end == end:
				return
		raise AssertionError(f'Requested invalid MIO pair {mios} for {self.name}{num}, valid MIOs are {valid_mios}')

	def generate_mapping(self, m : Module) -> dict:
		num = self.number
		scl_oe_n = Signal()
		sda_oe_n = Signal()

		if self._mios != MIOSet.EMIO:
			resource = Record(self.signals, name = f'i2c_{num}')
		elif self._emio is None:
			resource = self
		else:
			emio = self._emio
			resource = Record(self.signals, name = f'i2c_{num}', fields = {
				'scl_i':  emio.scl.i,
				'scl_o':  emio.scl.o,
				'scl_oe': emio.scl.oe,
				'sda_i':  emio.sda.i,
				'sda_o':  emio.sda.o,
				'sda_oe': emio.sda.oe,
			})

		m.d.comb += [
			resource.scl_oe.eq(~scl_oe_n),
			resource.sda_oe.eq(~sda_oe_n),
		]

		return  {
			f'i_EMIOI2C{num}SCLI':  resource.scl_i,
			f'o_EMIOI2C{num}SCLO':  resource.scl_o,
			f'o_EMIOI2C{num}SCLTN': scl_oe_n,
			f'i_EMIOI2C{num}SDAI':  resource.sda_i,
			f'o_EMIOI2C{num}SDAO':  resource.sda_o,
			f'o_EMIOI2C{num}SDATN': sda_oe_n,
		}

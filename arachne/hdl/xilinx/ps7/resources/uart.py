# SPDX-License-Identifier: BSD-3-Clause
from nmigen         import *
from nmigen.hdl.rec import (DIR_FANIN, DIR_FANOUT)

from .common        import *

__all__ = (
	'UARTResource',
)

class UARTResource(PS7Resource):
	name = 'uart'
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
			(MIOSet.MIO08, MIOSet.MIO09),
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
		('rx',    1, DIR_FANIN),
		('tx',    1, DIR_FANOUT),

		('rts_n', 1, DIR_FANOUT),
		('cts_n', 1, DIR_FANIN),
		('dtr_n', 1, DIR_FANOUT),
		('dsr_n', 1, DIR_FANIN),
		('dcd_n', 1, DIR_FANIN),
		('ri_n',  1, DIR_FANIN),
	)

	def __init__(self, num, *, mios = None, emio = None):
		assert mios is None or emio is None
		if mios is not None:
			self._validate_mios(num, mios)
			mio = mios
		elif emio is not None:
			mio = MIOSet.EMIO
		else:
			mio = ()

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

		if self._mios != MIOSet.EMIO:
			resource = Record(self.signals, name = f'uart_{num}')
		elif self._emio is None:
			resource = self
		else:
			emio = self._emio
			# TODO: Handle the other control signals here if they're present in the mapped EMIO
			fields = {
				'rx', emio.rx.i,
				'tx', emio.tx.o,
			}
			resource = Record(self.signals, name = f'uart_{num}', fields = fields)

		return  {
			f'i_EMIOUART{num}RX':   resource.rx,
			f'o_EMIOUART{num}TX':   resource.tx,

			f'o_EMIOUART{num}RTSN': resource.rts_n,
			f'i_EMIOUART{num}CTSN': resource.cts_n,
			f'o_EMIOUART{num}DTRN': resource.dtr_n,
			f'i_EMIOUART{num}DSRN': resource.dsr_n,
			f'i_EMIOUART{num}DCDN': resource.dcd_n,
			f'i_EMIOUART{num}RIN':  resource.ri_n,
		}

# SPDX-License-Identifier: BSD-3-Clause
from amaranth       import *
from amaranth.build import *

from ....util       import dbg

from .mio           import *
from .resources     import PS8Resource

from .ps8_test      import _PS8_TEST_SIGNALS

__all__ = (
	'PS8',
)

class BUFG_PS(Elaboratable):
	"""Xilinx Zynq UltraScale+ MPSoC PS Global Buffer

	"""
	def __init__(self, *, i : Signal, o : Signal):
		self._i = i
		self._o = o

	def elaborate(self, platform) -> Module:
		m = Module()

		m.submodules.bufg_ps = Instance(
			'BUFG_PS',
			i_I = self._i,
			o_O = self._o,
		)

		return m

class PS8(Elaboratable):
	"""Xilinx Zynq UltraScale+ MPSoC PS Block

	"""
	def __init__(self, *, resources = [], **kwargs):
		self._ps_resources = [ *resources ]

		self._block = 'PS8_TEST' if kwargs.get('test_instance', False)  else 'PS8'

	def elaborate(self, platform) -> Module:
		# check to see if there is a `ps8resources` block for us
		if hasattr(platform, 'ps8resources'):
			self._ps_resources.append(*platform.ps8resources)

		self._validate_ps_resources()

		mappings = self._generate_mappings()

		# Append the massive chunk of test signals to the instance
		if self._block == 'PS8_TEST':
			mappings.update(**_PS8_TEST_SIGNALS)


		m = Module()

		m.submodules.ps8 = Instance(
			self._block,
			# unpack the generated mappings into the instance
			**mappings,
		)

		return m

	def _validate_ps_resources(self):
		if any(map(lambda r: not isinstance(r, PS8Resource), self._ps_resources)):
			raise ValueError('Non-PS8Resource found in ps resources block')

	def _generate_mappings(self):
		mappings = {}

		if len(self._ps_resources) > 0:
			for res in self._ps_resources:
				mappings.update(res.generate_mapping())

		return mappings

"""
The following is a rough template of the PS8 and PS8_TEST blocks
with signal size and direction

PS8 ps8 (
	# DMA
	o_ADMA2PLCACK[7:0],
	o_ADMA2PLTVLD[7:0],
	i_ADMAFCICLK[7:0],
	o_GDMA2PLCACK[7:0],
	o_GDMA2PLTVLD[7:0],
	i_GDMAFCICLK[7:0],
	i_PL2ADMACVLD[7:0],
	i_PL2ADMATACK[7:0],
	i_PL2GDMACVLD[7:0],
	i_PL2GDMATACK[7:0],

	# PMU?
	i_AIBPMUAFIFMFPDACK,
	i_AIBPMUAFIFMLPDACK,

	# DDRC?
	i_DDRCEXTREFRESHRANK0REQ,
	i_DDRCEXTREFRESHRANK1REQ,
	i_DDRCREFRESHPLCLK,

	# Display Port,
	o_DPAUDIOREFCLK,
	i_DPAUXDATAIN,
	o_DPAUXDATAOEN,
	o_DPAUXDATAOUT,
	i_DPEXTERNALCUSTOMEVENT1,
	i_DPEXTERNALCUSTOMEVENT2,
	i_DPEXTERNALVSYNCEVENT,
	i_DPHOTPLUGDETECT,
	i_DPLIVEGFXALPHAIN[7:0],
	i_DPLIVEGFXPIXEL1IN[35:0],
	o_DPLIVEVIDEODEOUT,
	i_DPLIVEVIDEOINDE,
	i_DPLIVEVIDEOINHSYNC,
	i_DPLIVEVIDEOINPIXEL1[35:0],
	i_DPLIVEVIDEOINVSYNC,
	o_DPMAXISMIXEDAUDIOTDATA[31:0],
	o_DPMAXISMIXEDAUDIOTID,
	i_DPMAXISMIXEDAUDIOTREADY,
	o_DPMAXISMIXEDAUDIOTVALID,
	i_DPSAXISAUDIOCLK,
	i_DPSAXISAUDIOTDATA[31:0],
	i_DPSAXISAUDIOTID,
	o_DPSAXISAUDIOTREADY,
	i_DPSAXISAUDIOTVALID,
	i_DPVIDEOINCLK,
	o_DPVIDEOOUTHSYNC,
	o_DPVIDEOOUTPIXEL1[35:0],
	o_DPVIDEOOUTVSYNC,
	o_DPVIDEOREFCLK,

	# CAN0
	i_EMIOCAN0PHYRX,
	o_EMIOCAN0PHYTX,

	# CAN1
	i_EMIOCAN1PHYRX,
	o_EMIOCAN1PHYTX,

	# ETH0
	o_EMIOENET0DMABUSWIDTH[1:0],
	o_EMIOENET0DMATXENDTOG,
	i_EMIOENET0DMATXSTATUSTOG,
	i_EMIOENET0EXTINTIN,
	o_EMIOENET0GEMTSUTIMERCNT[93:0],
	i_EMIOENET0GMIICOL,
	i_EMIOENET0GMIICRS,
	i_EMIOENET0GMIIRXCLK,
	i_EMIOENET0GMIIRXD[7:0],
	i_EMIOENET0GMIIRXDV,
	i_EMIOENET0GMIIRXER,
	i_EMIOENET0GMIITXCLK,
	o_EMIOENET0GMIITXD[7:0],
	o_EMIOENET0GMIITXEN,
	o_EMIOENET0GMIITXER,
	i_EMIOENET0MDIOI,
	o_EMIOENET0MDIOMDC,
	o_EMIOENET0MDIOO,
	io_EMIOENET0MDIOTN, # ????
	o_EMIOENET0RXWDATA[7:0],
	o_EMIOENET0RXWEOP,
	o_EMIOENET0RXWERR,
	o_EMIOENET0RXWFLUSH,
	i_EMIOENET0RXWOVERFLOW,
	o_EMIOENET0RXWSOP,
	o_EMIOENET0RXWSTATUS[44:0],
	o_EMIOENET0RXWWR,
	o_EMIOENET0SPEEDMODE[2:0],
	i_EMIOENET0TXRCONTROL,
	i_EMIOENET0TXRDATA[7:0],
	i_EMIOENET0TXRDATARDY,
	i_EMIOENET0TXREOP,
	i_EMIOENET0TXRERR,
	i_EMIOENET0TXRFLUSHED,
	o_EMIOENET0TXRRD,
	i_EMIOENET0TXRSOP,
	o_EMIOENET0TXRSTATUS[3:0],
	i_EMIOENET0TXRUNDERFLOW,
	i_EMIOENET0TXRVALID,

	# ETH1
	o_EMIOENET1DMABUSWIDTH[1:0],
	o_EMIOENET1DMATXENDTOG,
	i_EMIOENET1DMATXSTATUSTOG,
	i_EMIOENET1EXTINTIN,
	o_EMIOENET1GEMTSUTIMERCNT[93:0],
	i_EMIOENET1GMIICOL,
	i_EMIOENET1GMIICRS,
	i_EMIOENET1GMIIRXCLK,
	i_EMIOENET1GMIIRXD[7:0],
	i_EMIOENET1GMIIRXDV,
	i_EMIOENET1GMIIRXER,
	i_EMIOENET1GMIITXCLK,
	o_EMIOENET1GMIITXD[7:0],
	o_EMIOENET1GMIITXEN,
	o_EMIOENET1GMIITXER,
	i_EMIOENET1MDIOI,
	o_EMIOENET1MDIOMDC,
	o_EMIOENET1MDIOO,
	io_EMIOENET1MDIOTN, # ????
	o_EMIOENET1RXWDATA[7:0],
	o_EMIOENET1RXWEOP,
	o_EMIOENET1RXWERR,
	o_EMIOENET1RXWFLUSH,
	i_EMIOENET1RXWOVERFLOW,
	o_EMIOENET1RXWSOP,
	o_EMIOENET1RXWSTATUS[44:0],
	o_EMIOENET1RXWWR,
	o_EMIOENET1SPEEDMODE[2:0],
	i_EMIOENET1TXRCONTROL,
	i_EMIOENET1TXRDATA[7:0],
	i_EMIOENET1TXRDATARDY,
	i_EMIOENET1TXREOP,
	i_EMIOENET1TXRERR,
	i_EMIOENET1TXRFLUSHED,
	o_EMIOENET1TXRRD,
	i_EMIOENET1TXRSOP,
	o_EMIOENET1TXRSTATUS[3:0],
	i_EMIOENET1TXRUNDERFLOW,
	i_EMIOENET1TXRVALID,

	# ETH2
	o_EMIOENET2DMABUSWIDTH[1:0],
	o_EMIOENET2DMATXENDTOG,
	i_EMIOENET2DMATXSTATUSTOG,
	i_EMIOENET2EXTINTIN,
	o_EMIOENET2GEMTSUTIMERCNT[93:0],
	i_EMIOENET2GMIICOL,
	i_EMIOENET2GMIICRS,
	i_EMIOENET2GMIIRXCLK,
	i_EMIOENET2GMIIRXD[7:0],
	i_EMIOENET2GMIIRXDV,
	i_EMIOENET2GMIIRXER,
	i_EMIOENET2GMIITXCLK,
	o_EMIOENET2GMIITXD[7:0],
	o_EMIOENET2GMIITXEN,
	o_EMIOENET2GMIITXER,
	i_EMIOENET2MDIOI,
	o_EMIOENET2MDIOMDC,
	o_EMIOENET2MDIOO,
	io_EMIOENET2MDIOTN, # ????
	o_EMIOENET2RXWDATA[7:0],
	o_EMIOENET2RXWEOP,
	o_EMIOENET2RXWERR,
	o_EMIOENET2RXWFLUSH,
	i_EMIOENET2RXWOVERFLOW,
	o_EMIOENET2RXWSOP,
	o_EMIOENET2RXWSTATUS[44:0],
	o_EMIOENET2RXWWR,
	o_EMIOENET2SPEEDMODE[2:0],
	i_EMIOENET2TXRCONTROL,
	i_EMIOENET2TXRDATA[7:0],
	i_EMIOENET2TXRDATARDY,
	i_EMIOENET2TXREOP,
	i_EMIOENET2TXRERR,
	i_EMIOENET2TXRFLUSHED,
	o_EMIOENET2TXRRD,
	i_EMIOENET2TXRSOP,
	o_EMIOENET2TXRSTATUS[3:0],
	i_EMIOENET2TXRUNDERFLOW,
	i_EMIOENET2TXRVALID,

	# ETH3
	o_EMIOENET3DMABUSWIDTH[1:0],
	o_EMIOENET3DMATXENDTOG,
	i_EMIOENET3DMATXSTATUSTOG,
	i_EMIOENET3EXTINTIN,
	o_EMIOENET3GEMTSUTIMERCNT[93:0],
	i_EMIOENET3GMIICOL,
	i_EMIOENET3GMIICRS,
	i_EMIOENET3GMIIRXCLK,
	i_EMIOENET3GMIIRXD[7:0],
	i_EMIOENET3GMIIRXDV,
	i_EMIOENET3GMIIRXER,
	i_EMIOENET3GMIITXCLK,
	o_EMIOENET3GMIITXD[7:0],
	o_EMIOENET3GMIITXEN,
	o_EMIOENET3GMIITXER,
	i_EMIOENET3MDIOI,
	o_EMIOENET3MDIOMDC,
	o_EMIOENET3MDIOO,
	io_EMIOENET3MDIOTN, # ????
	o_EMIOENET3RXWDATA[7:0],
	o_EMIOENET3RXWEOP,
	o_EMIOENET3RXWERR,
	o_EMIOENET3RXWFLUSH,
	i_EMIOENET3RXWOVERFLOW,
	o_EMIOENET3RXWSOP,
	o_EMIOENET3RXWSTATUS[44:0],
	o_EMIOENET3RXWWR,
	o_EMIOENET3SPEEDMODE[2:0],
	i_EMIOENET3TXRCONTROL,
	i_EMIOENET3TXRDATA[7:0],
	i_EMIOENET3TXRDATARDY,
	i_EMIOENET3TXREOP,
	i_EMIOENET3TXRERR,
	i_EMIOENET3TXRFLUSHED,
	o_EMIOENET3TXRRD,
	i_EMIOENET3TXRSOP,
	o_EMIOENET3TXRSTATUS[3:0],
	i_EMIOENET3TXRUNDERFLOW,
	i_EMIOENET3TXRVALID,

	# ???
	i_EMIOENETTSUCLK,
	i_FMIOGEMTSUCLKFROMPL,
	o_FMIOGEMTSUCLKTOPLBUFG,

	# GME0
	o_EMIOGEM0DELAYREQRX,
	o_EMIOGEM0DELAYREQTX,
	o_EMIOGEM0PDELAYREQRX,
	o_EMIOGEM0PDELAYREQTX,
	o_EMIOGEM0PDELAYRESPRX,
	o_EMIOGEM0PDELAYRESPTX,
	o_EMIOGEM0RXSOF,
	o_EMIOGEM0SYNCFRAMERX,
	o_EMIOGEM0SYNCFRAMETX,
	i_EMIOGEM0TSUINCCTRL[1:0],
	o_EMIOGEM0TSUTIMERCMPVAL,
	o_EMIOGEM0TXRFIXEDLAT,
	o_EMIOGEM0TXSOF,
	io_FMIOGEM0FIFORXCLKFROMPL,
	io_FMIOGEM0FIFORXCLKTOPLBUFG,
	io_FMIOGEM0FIFOTXCLKFROMPL,
	io_FMIOGEM0FIFOTXCLKTOPLBUFG,
	i_FMIOGEM0SIGNALDETECT,

	# GME1
	o_EMIOGEM1DELAYREQRX,
	o_EMIOGEM1DELAYREQTX,
	o_EMIOGEM1PDELAYREQRX,
	o_EMIOGEM1PDELAYREQTX,
	o_EMIOGEM1PDELAYRESPRX,
	o_EMIOGEM1PDELAYRESPTX,
	o_EMIOGEM1RXSOF,
	o_EMIOGEM1SYNCFRAMERX,
	o_EMIOGEM1SYNCFRAMETX,
	i_EMIOGEM1TSUINCCTRL[1:0],
	o_EMIOGEM1TSUTIMERCMPVAL,
	o_EMIOGEM1TXRFIXEDLAT,
	o_EMIOGEM1TXSOF,
	io_FMIOGEM1FIFORXCLKFROMPL,
	io_FMIOGEM1FIFORXCLKTOPLBUFG,
	io_FMIOGEM1FIFOTXCLKFROMPL,
	io_FMIOGEM1FIFOTXCLKTOPLBUFG,
	i_FMIOGEM1SIGNALDETECT,

	# GME2
	o_EMIOGEM2DELAYREQRX,
	o_EMIOGEM2DELAYREQTX,
	o_EMIOGEM2PDELAYREQRX,
	o_EMIOGEM2PDELAYREQTX,
	o_EMIOGEM2PDELAYRESPRX,
	o_EMIOGEM2PDELAYRESPTX,
	o_EMIOGEM2RXSOF,
	o_EMIOGEM2SYNCFRAMERX,
	o_EMIOGEM2SYNCFRAMETX,
	i_EMIOGEM2TSUINCCTRL[1:0],
	o_EMIOGEM2TSUTIMERCMPVAL,
	o_EMIOGEM2TXRFIXEDLAT,
	o_EMIOGEM2TXSOF,
	io_FMIOGEM2FIFORXCLKFROMPL,
	io_FMIOGEM2FIFORXCLKTOPLBUFG,
	io_FMIOGEM2FIFOTXCLKFROMPL,
	io_FMIOGEM2FIFOTXCLKTOPLBUFG,
	i_FMIOGEM2SIGNALDETECT,

	# GME3
	o_EMIOGEM3DELAYREQRX,
	o_EMIOGEM3DELAYREQTX,
	o_EMIOGEM3PDELAYREQRX,
	o_EMIOGEM3PDELAYREQTX,
	o_EMIOGEM3PDELAYRESPRX,
	o_EMIOGEM3PDELAYRESPTX,
	o_EMIOGEM3RXSOF,
	o_EMIOGEM3SYNCFRAMERX,
	o_EMIOGEM3SYNCFRAMETX,
	i_EMIOGEM3TSUINCCTRL[1:0],
	o_EMIOGEM3TSUTIMERCMPVAL,
	o_EMIOGEM3TXRFIXEDLAT,
	o_EMIOGEM3TXSOF,
	io_FMIOGEM3FIFORXCLKFROMPL,
	io_FMIOGEM3FIFORXCLKTOPLBUFG,
	io_FMIOGEM3FIFOTXCLKFROMPL,
	io_FMIOGEM3FIFOTXCLKTOPLBUFG,
	i_FMIOGEM3SIGNALDETECT,

	# GPIO?
	io_EMIOGPIOI[95:0],
	io_EMIOGPIOO[95:0],
	io_EMIOGPIOTN[95:0],

	# USB0
	i_EMIOHUBPORTOVERCRNTUSB20,
	i_EMIOHUBPORTOVERCRNTUSB30,
	o_EMIOU2DSPORTVBUSCTRLUSB30,
	o_EMIOU3DSPORTVBUSCTRLUSB30,

	# USB1
	i_EMIOHUBPORTOVERCRNTUSB21,
	i_EMIOHUBPORTOVERCRNTUSB31,
	o_EMIOU2DSPORTVBUSCTRLUSB31,
	o_EMIOU3DSPORTVBUSCTRLUSB31,

	# I2C0
	i_EMIOI2C0SCLI,
	o_EMIOI2C0SCLO,
	io_EMIOI2C0SCLTN,
	i_EMIOI2C0SDAI,
	o_EMIOI2C0SDAO,
	io_EMIOI2C0SDATN,

	# I2C1
	i_EMIOI2C1SCLI,
	o_EMIOI2C1SCLO,
	io_EMIOI2C1SCLTN,
	i_EMIOI2C1SDAI,
	o_EMIOI2C1SDAO,
	io_EMIOI2C1SDATN,

	# SD0
	o_EMIOSDIO0BUSPOWER,
	o_EMIOSDIO0BUSVOLT[2:0],
	i_EMIOSDIO0CDN,
	o_EMIOSDIO0CLKOUT,
	io_EMIOSDIO0CMDENA,
	i_EMIOSDIO0CMDIN,
	o_EMIOSDIO0CMDOUT,
	io_EMIOSDIO0DATAENA[7:0],
	i_EMIOSDIO0DATAIN[7:0],
	o_EMIOSDIO0DATAOUT[7:0],
	i_EMIOSDIO0FBCLKIN,
	o_EMIOSDIO0LEDCONTROL,
	i_EMIOSDIO0WP,

	# SD1
	o_EMIOSDIO1BUSPOWER,
	o_EMIOSDIO1BUSVOLT[2:0],
	i_EMIOSDIO1CDN,
	o_EMIOSDIO1CLKOUT,
	io_EMIOSDIO1CMDENA,
	i_EMIOSDIO1CMDIN,
	o_EMIOSDIO1CMDOUT,
	io_EMIOSDIO1DATAENA[7:0],
	i_EMIOSDIO1DATAIN[7:0],
	o_EMIOSDIO1DATAOUT[7:0],
	i_EMIOSDIO1FBCLKIN,
	o_EMIOSDIO1LEDCONTROL,
	i_EMIOSDIO1WP,

	# SPI0
	i_EMIOSPI0MI,
	o_EMIOSPI0MO,
	io_EMIOSPI0MOTN,
	i_EMIOSPI0SCLKI,
	o_EMIOSPI0SCLKO,
	io_EMIOSPI0SCLKTN,
	i_EMIOSPI0SI,
	o_EMIOSPI0SO,
	i_EMIOSPI0SSIN,
	io_EMIOSPI0SSNTN,
	o_EMIOSPI0SSON[2:0],
	io_EMIOSPI0STN,

	# SPI1
	i_EMIOSPI1MI,
	o_EMIOSPI1MO,
	io_EMIOSPI1MOTN,
	i_EMIOSPI1SCLKI,
	o_EMIOSPI1SCLKO,
	io_EMIOSPI1SCLKTN,
	i_EMIOSPI1SI,
	o_EMIOSPI1SO,
	i_EMIOSPI1SSIN,
	io_EMIOSPI1SSNTN,
	o_EMIOSPI1SSON[2:0],
	io_EMIOSPI1STN,

	# TTC0
	i_EMIOTTC0CLKI[2:0],
	o_EMIOTTC0WAVEO[2:0],

	# TTC1
	i_EMIOTTC1CLKI[2:0],
	o_EMIOTTC1WAVEO[2:0],

	# TTC2
	i_EMIOTTC2CLKI[2:0],
	o_EMIOTTC2WAVEO[2:0],

	# TTC3
	i_EMIOTTC3CLKI[2:0],
	o_EMIOTTC3WAVEO[2:0],

	# UART0
	i_EMIOUART0CTSN,
	i_EMIOUART0DCDN,
	i_EMIOUART0DSRN,
	o_EMIOUART0DTRN,
	i_EMIOUART0RIN,
	o_EMIOUART0RTSN,
	i_EMIOUART0RX,
	o_EMIOUART0TX,

	# UART1
	i_EMIOUART1CTSN,
	i_EMIOUART1DCDN,
	i_EMIOUART1DSRN,
	o_EMIOUART1DTRN,
	i_EMIOUART1RIN,
	o_EMIOUART1RTSN,
	i_EMIOUART1RX,
	o_EMIOUART1TX,

	# SWDT0
	i_EMIOWDT0CLKI,
	o_EMIOWDT0RSTO,

	# SWDT1
	i_EMIOWDT1CLKI,
	o_EMIOWDT1RSTO,

	# GP{I,O}
	i_FTMGPI[31:0],
	o_FTMGPO[31:0],

	# AXI Manager GP0
	i_MAXIGP0ACLK,
	o_MAXIGP0ARADDR[39:0],
	i_MAXIGP0ARBURST[1:0],
	o_MAXIGP0ARCACHE[3:0],
	o_MAXIGP0ARID[15:0],
	o_MAXIGP0ARLEN[7:0],
	o_MAXIGP0ARLOCK,
	o_MAXIGP0ARPROT[2:0],
	o_MAXIGP0ARQOS[3:0],
	i_MAXIGP0ARREADY,
	o_MAXIGP0ARSIZE[2:0],
	o_MAXIGP0ARUSER[15:0],
	o_MAXIGP0ARVALID,
	o_MAXIGP0AWADDR[39:0],
	o_MAXIGP0AWBURST[1:0],
	o_MAXIGP0AWCACHE[3:0],
	o_MAXIGP0AWID[15:0],
	o_MAXIGP0AWLEN[7:0],
	o_MAXIGP0AWLOCK,
	o_MAXIGP0AWPROT[2:0],
	o_MAXIGP0AWQOS[3:0],
	i_MAXIGP0AWREADY,
	o_MAXIGP0AWSIZE[2:0],
	o_MAXIGP0AWUSER[15:0],
	o_MAXIGP0AWVALID,
	i_MAXIGP0BID[15:0],
	o_MAXIGP0BREADY,
	i_MAXIGP0BRESP[1:0],
	i_MAXIGP0BVALID,
	io_MAXIGP0RDATA[127:0],
	i_MAXIGP0RID[15:0],
	i_MAXIGP0RLAST,
	o_MAXIGP0RREADY,
	i_MAXIGP0RRESP[1:0],
	i_MAXIGP0RVALID,
	io_MAXIGP0WDATA[127:0],
	o_MAXIGP0WLAST,
	i_MAXIGP0WREADY,
	io_MAXIGP0WSTRB[15:0],
	o_MAXIGP0WVALID,

	# AXI Manager GP1
	i_MAXIGP1ACLK,
	o_MAXIGP1ARADDR[39:0],
	i_MAXIGP1ARBURST[1:0],
	o_MAXIGP1ARCACHE[3:0],
	o_MAXIGP1ARID[15:0],
	o_MAXIGP1ARLEN[7:0],
	o_MAXIGP1ARLOCK,
	o_MAXIGP1ARPROT[2:0],
	o_MAXIGP1ARQOS[3:0],
	i_MAXIGP1ARREADY,
	o_MAXIGP1ARSIZE[2:0],
	o_MAXIGP1ARUSER[15:0],
	o_MAXIGP1ARVALID,
	o_MAXIGP1AWADDR[39:0],
	o_MAXIGP1AWBURST[1:0],
	o_MAXIGP1AWCACHE[3:0],
	o_MAXIGP1AWID[15:0],
	o_MAXIGP1AWLEN[7:0],
	o_MAXIGP1AWLOCK,
	o_MAXIGP1AWPROT[2:0],
	o_MAXIGP1AWQOS[3:0],
	i_MAXIGP1AWREADY,
	o_MAXIGP1AWSIZE[2:0],
	o_MAXIGP1AWUSER[15:0],
	o_MAXIGP1AWVALID,
	i_MAXIGP1BID[15:0],
	o_MAXIGP1BREADY,
	i_MAXIGP1BRESP[1:0],
	i_MAXIGP1BVALID,
	io_MAXIGP1RDATA[127:0],
	i_MAXIGP1RID[15:0],
	i_MAXIGP1RLAST,
	o_MAXIGP1RREADY,
	i_MAXIGP1RRESP[1:0],
	i_MAXIGP1RVALID,
	io_MAXIGP1WDATA[127:0],
	o_MAXIGP1WLAST,
	i_MAXIGP1WREADY,
	io_MAXIGP1WSTRB[15:0],
	o_MAXIGP1WVALID,

	# AXI Manager GP2
	i_MAXIGP2ACLK,
	o_MAXIGP2ARADDR[39:0],
	i_MAXIGP2ARBURST[1:0],
	o_MAXIGP2ARCACHE[3:0],
	o_MAXIGP2ARID[15:0],
	o_MAXIGP2ARLEN[7:0],
	o_MAXIGP2ARLOCK,
	o_MAXIGP2ARPROT[2:0],
	o_MAXIGP2ARQOS[3:0],
	i_MAXIGP2ARREADY,
	o_MAXIGP2ARSIZE[2:0],
	o_MAXIGP2ARUSER[15:0],
	o_MAXIGP2ARVALID,
	o_MAXIGP2AWADDR[39:0],
	o_MAXIGP2AWBURST[1:0],
	o_MAXIGP2AWCACHE[3:0],
	o_MAXIGP2AWID[15:0],
	o_MAXIGP2AWLEN[7:0],
	o_MAXIGP2AWLOCK,
	o_MAXIGP2AWPROT[2:0],
	o_MAXIGP2AWQOS[3:0],
	i_MAXIGP2AWREADY,
	o_MAXIGP2AWSIZE[2:0],
	o_MAXIGP2AWUSER[15:0],
	o_MAXIGP2AWVALID,
	i_MAXIGP2BID[15:0],
	o_MAXIGP2BREADY,
	i_MAXIGP2BRESP[1:0],
	i_MAXIGP2BVALID,
	io_MAXIGP2RDATA[127:0],
	i_MAXIGP2RID[15:0],
	i_MAXIGP2RLAST,
	o_MAXIGP2RREADY,
	i_MAXIGP2RRESP[1:0],
	i_MAXIGP2RVALID,
	io_MAXIGP2WDATA[127:0],
	o_MAXIGP2WLAST,
	i_MAXIGP2WREADY,
	io_MAXIGP2WSTRB[15:0],
	o_MAXIGP2WVALID,

	# IRQ0
	i_NFIQ0LPDRPU,
	i_NIRQ0LPDRPU,

	# IRQ1
	i_NFIQ1LPDRPU,
	i_NIRQ1LPDRPU,

	# ????
	o_OSCRTCCLK,

	# PL Stuff???
	i_PLACECLK,
	i_PLACPINACT,
	io_PLCLK[3:0],
	i_PLFPGASTOP[3:0],
	i_PLLAUXREFCLKFPD[2:0],
	i_PLLAUXREFCLKLPD[1:0],
	i_PLPMUGPI[31:0],


	# PL -> PS
	i_PLPSAPUGICFIQ[3:0],
	i_PLPSAPUGICIRQ[3:0],
	i_PLPSEVENTI,
	io_PLPSIRQ0[7:0],
	io_PLPSIRQ1[7:0],
	i_PLPSTRACECLK,
	i_PLPSTRIGACK[3:0],
	i_PLPSTRIGGER[3:0],

	# PMU
	o_PMUAIBAFIFMFPDREQ,
	o_PMUAIBAFIFMLPDREQ,
	i_PMUERRORFROMPL[3:0],
	o_PMUERRORTOPL[46:0],
	o_PMUPLGPO[31:0],

	# PS -> PL
	o_PSPLEVENTO,
	io_PSPLIRQFPD[62:0], # thicc girls,,,,,,
	io_PSPLIRQLPD[99:0], # thicc girls,,,,,,
	o_PSPLSTANDBYWFE[3:0],
	o_PSPLSTANDBYWFI[3:0],
	io_PSPLTRACECTL,
	io_PSPLTRACEDATA[31:0],
	o_PSPLTRIGACK[3:0],
	o_PSPLTRIGGER[3:0],

	# RPU0 Events
	i_RPUEVENTI0,
	o_RPUEVENTO0,

	# RPU1 Events
	i_RPUEVENTI1,
	o_RPUEVENTO1,


	# ACE Subordinate
	o_SACEFPDACADDR[43:0],
	o_SACEFPDACPROT[2:0],
	i_SACEFPDACREADY,
	o_SACEFPDACSNOOP[3:0],
	o_SACEFPDACVALID,
	i_SACEFPDARADDR[43:0],
	i_SACEFPDARBAR[1:0],
	i_SACEFPDARBURST[1:0],
	i_SACEFPDARCACHE[3:0],
	i_SACEFPDARDOMAIN[1:0],
	i_SACEFPDARID[5:0],
	i_SACEFPDARLEN[7:0],
	i_SACEFPDARLOCK,
	i_SACEFPDARPROT[2:0],
	i_SACEFPDARQOS[3:0],
	o_SACEFPDARREADY,
	i_SACEFPDARREGION[3:0],
	i_SACEFPDARSIZE[2:0],
	i_SACEFPDARSNOOP[3:0],
	i_SACEFPDARUSER[15:0],
	i_SACEFPDARVALID,
	i_SACEFPDAWADDR[43:0],
	i_SACEFPDAWBAR[1:0],
	i_SACEFPDAWBURST[1:0],
	i_SACEFPDAWCACHE[3:0],
	i_SACEFPDAWDOMAIN[1:0],
	i_SACEFPDAWID[5:0],
	i_SACEFPDAWLEN[7:0],
	i_SACEFPDAWLOCK,
	i_SACEFPDAWPROT[2:0],
	i_SACEFPDAWQOS[3:0],
	o_SACEFPDAWREADY,
	i_SACEFPDAWREGION[3:0],
	i_SACEFPDAWSIZE[2:0],
	i_SACEFPDAWSNOOP[2:0],
	i_SACEFPDAWUSER[15:0],
	i_SACEFPDAWVALID,
	o_SACEFPDBID[5:0],
	i_SACEFPDBREADY,
	i_SACEFPDBRESP[1:0],
	o_SACEFPDBUSER,
	o_SACEFPDBVALID,
	i_SACEFPDCDDATA[127:0],
	i_SACEFPDCDLAST,
	o_SACEFPDCDREADY,
	i_SACEFPDCDVALID,
	o_SACEFPDCRREADY,
	i_SACEFPDCRRESP[4:0],
	i_SACEFPDCRVALID,
	i_SACEFPDRACK,
	o_SACEFPDRDATA[127:0],
	o_SACEFPDRID[5:0],
	o_SACEFPDRLAST,
	i_SACEFPDRREADY,
	o_SACEFPDRRESP[3:0],
	o_SACEFPDRUSER,
	o_SACEFPDRVALID,
	i_SACEFPDWACK,
	i_SACEFPDWDATA[127:0],
	i_SACEFPDWLAST,
	o_SACEFPDWREADY,
	i_SACEFPDWSTRB[15:0],
	i_SACEFPDWUSER,
	i_SACEFPDWVALID,

	# AXI ACP Subordinate
	i_SAXIACPACLK,
	i_SAXIACPARADDR[39:0],
	i_SAXIACPARBURST[1:0],
	i_SAXIACPARCACHE[3:0],
	i_SAXIACPARID[4:0],
	i_SAXIACPARLEN[7:0],
	i_SAXIACPARLOCK,
	i_SAXIACPARPROT[2:0],
	i_SAXIACPARQOS[3:0],
	o_SAXIACPARREADY,
	i_SAXIACPARSIZE[2:0],
	i_SAXIACPARUSER[1:0],
	i_SAXIACPARVALID,
	i_SAXIACPAWADDR[39:0],
	i_SAXIACPAWBURST[1:0],
	i_SAXIACPAWCACHE[3:0],
	i_SAXIACPAWID[4:0],
	i_SAXIACPAWLEN[7:0],
	i_SAXIACPAWLOCK,
	i_SAXIACPAWPROT[2:0],
	i_SAXIACPAWQOS[3:0],
	o_SAXIACPAWREADY,
	i_SAXIACPAWSIZE[2:0],
	i_SAXIACPAWUSER[1:0],
	i_SAXIACPAWVALID,
	o_SAXIACPBID[4:0],
	i_SAXIACPBREADY,
	o_SAXIACPBRESP[1:0],
	o_SAXIACPBVALID,
	o_SAXIACPRDATA[127:0],
	o_SAXIACPRID[4:0],
	o_SAXIACPRLAST,
	i_SAXIACPRREADY,
	o_SAXIACPRRESP[1:0],
	o_SAXIACPRVALID,
	i_SAXIACPWDATA[127:0],
	i_SAXIACPWLAST,
	o_SAXIACPWREADY,
	i_SAXIACPWSTRB[15:0],
	i_SAXIACPWVALID,

	# AXI GP0 Subordinate
	i_SAXIGP0ARADDR[48:0],
	i_SAXIGP0ARBURST[1:0],
	i_SAXIGP0ARCACHE[3:0],
	i_SAXIGP0ARID[5:0],
	i_SAXIGP0ARLEN[7:0],
	i_SAXIGP0ARLOCK,
	i_SAXIGP0ARPROT[2:0],
	i_SAXIGP0ARQOS[3:0],
	o_SAXIGP0ARREADY,
	i_SAXIGP0ARSIZE[2:0],
	i_SAXIGP0ARUSER,
	i_SAXIGP0ARVALID,
	i_SAXIGP0AWADDR[48:0],
	i_SAXIGP0AWBURST[1:0],
	i_SAXIGP0AWCACHE[3:0],
	i_SAXIGP0AWID[5:0],
	i_SAXIGP0AWLEN[7:0],
	i_SAXIGP0AWLOCK,
	i_SAXIGP0AWPROT[2:0],
	i_SAXIGP0AWQOS[3:0],
	o_SAXIGP0AWREADY,
	i_SAXIGP0AWSIZE[2:0],
	i_SAXIGP0AWUSER,
	i_SAXIGP0AWVALID,
	o_SAXIGP0BID[5:0],
	i_SAXIGP0BREADY,
	o_SAXIGP0BRESP[1:0],
	o_SAXIGP0BVALID,
	o_SAXIGP0RACOUNT[3:0],
	io_SAXIGP0RCLK,
	o_SAXIGP0RCOUNT[7:0],
	io_SAXIGP0RDATA[127:0],
	o_SAXIGP0RID[5:0],
	o_SAXIGP0RLAST,
	i_SAXIGP0RREADY,
	o_SAXIGP0RRESP[1:0],
	o_SAXIGP0RVALID,
	o_SAXIGP0WACOUNT[3:0],
	io_SAXIGP0WCLK,
	o_SAXIGP0WCOUNT[7:0],
	io_SAXIGP0WDATA[127:0],
	i_SAXIGP0WLAST,
	o_SAXIGP0WREADY,
	io_SAXIGP0WSTRB[15:0],
	i_SAXIGP0WVALID,

	# AXI GP1 Subordinate
	i_SAXIGP1ARADDR[48:0],
	i_SAXIGP1ARBURST[1:0],
	i_SAXIGP1ARCACHE[3:0],
	i_SAXIGP1ARID[5:0],
	i_SAXIGP1ARLEN[7:0],
	i_SAXIGP1ARLOCK,
	i_SAXIGP1ARPROT[2:0],
	i_SAXIGP1ARQOS[3:0],
	o_SAXIGP1ARREADY,
	i_SAXIGP1ARSIZE[2:0],
	i_SAXIGP1ARUSER,
	i_SAXIGP1ARVALID,
	i_SAXIGP1AWADDR[48:0],
	i_SAXIGP1AWBURST[1:0],
	i_SAXIGP1AWCACHE[3:0],
	i_SAXIGP1AWID[5:0],
	i_SAXIGP1AWLEN[7:0],
	i_SAXIGP1AWLOCK,
	i_SAXIGP1AWPROT[2:0],
	i_SAXIGP1AWQOS[3:0],
	o_SAXIGP1AWREADY,
	i_SAXIGP1AWSIZE[2:0],
	i_SAXIGP1AWUSER,
	i_SAXIGP1AWVALID,
	o_SAXIGP1BID[5:0],
	i_SAXIGP1BREADY,
	o_SAXIGP1BRESP[1:0],
	o_SAXIGP1BVALID,
	o_SAXIGP1RACOUNT[3:0],
	io_SAXIGP1RCLK,
	o_SAXIGP1RCOUNT[7:0],
	io_SAXIGP1RDATA[127:0],
	o_SAXIGP1RID[5:0],
	o_SAXIGP1RLAST,
	i_SAXIGP1RREADY,
	o_SAXIGP1RRESP[1:0],
	o_SAXIGP1RVALID,
	o_SAXIGP0WACOUNT[3:0],
	io_SAXIGP1WCLK,
	o_SAXIGP1WCOUNT[7:0],
	io_SAXIGP1WDATA[127:0],
	i_SAXIGP1WLAST,
	o_SAXIGP1WREADY,
	io_SAXIGP1WSTRB[15:0],
	i_SAXIGP1WVALID,

	# AXI GP2 Subordinate
	i_SAXIGP2ARADDR[48:0],
	i_SAXIGP2ARBURST[1:0],
	i_SAXIGP2ARCACHE[3:0],
	i_SAXIGP2ARID[5:0],
	i_SAXIGP2ARLEN[7:0],
	i_SAXIGP2ARLOCK,
	i_SAXIGP2ARPROT[2:0],
	i_SAXIGP2ARQOS[3:0],
	o_SAXIGP2ARREADY,
	i_SAXIGP2ARSIZE[2:0],
	i_SAXIGP2ARUSER,
	i_SAXIGP2ARVALID,
	i_SAXIGP2AWADDR[48:0],
	i_SAXIGP2AWBURST[1:0],
	i_SAXIGP2AWCACHE[3:0],
	i_SAXIGP2AWID[5:0],
	i_SAXIGP2AWLEN[7:0],
	i_SAXIGP2AWLOCK,
	i_SAXIGP2AWPROT[2:0],
	i_SAXIGP2AWQOS[3:0],
	o_SAXIGP2AWREADY,
	i_SAXIGP2AWSIZE[2:0],
	i_SAXIGP2AWUSER,
	i_SAXIGP2AWVALID,
	o_SAXIGP2BID[5:0],
	i_SAXIGP2BREADY,
	o_SAXIGP2BRESP[1:0],
	o_SAXIGP2BVALID,
	o_SAXIGP2RACOUNT[3:0],
	io_SAXIGP2RCLK,
	o_SAXIGP2RCOUNT[7:0],
	io_SAXIGP2RDATA[127:0],
	o_SAXIGP2RID[5:0],
	o_SAXIGP2RLAST,
	i_SAXIGP2RREADY,
	o_SAXIGP2RRESP[1:0],
	o_SAXIGP2RVALID,
	o_SAXIGP2WACOUNT[3:0],
	io_SAXIGP2WCLK,
	o_SAXIGP2WCOUNT[7:0],
	io_SAXIGP2WDATA[127:0],
	i_SAXIGP2WLAST,
	o_SAXIGP2WREADY,
	io_SAXIGP2WSTRB[15:0],
	i_SAXIGP2WVALID,

	# AXI GP3 Subordinate
	i_SAXIGP3ARADDR[48:0],
	i_SAXIGP3ARBURST[1:0],
	i_SAXIGP3ARCACHE[3:0],
	i_SAXIGP3ARID[5:0],
	i_SAXIGP3ARLEN[7:0],
	i_SAXIGP3ARLOCK,
	i_SAXIGP3ARPROT[2:0],
	i_SAXIGP3ARQOS[3:0],
	o_SAXIGP3ARREADY,
	i_SAXIGP3ARSIZE[2:0],
	i_SAXIGP3ARUSER,
	i_SAXIGP3ARVALID,
	i_SAXIGP3AWADDR[48:0],
	i_SAXIGP3AWBURST[1:0],
	i_SAXIGP3AWCACHE[3:0],
	i_SAXIGP3AWID[5:0],
	i_SAXIGP3AWLEN[7:0],
	i_SAXIGP3AWLOCK,
	i_SAXIGP3AWPROT[2:0],
	i_SAXIGP3AWQOS[3:0],
	o_SAXIGP3AWREADY,
	i_SAXIGP3AWSIZE[2:0],
	i_SAXIGP3AWUSER,
	i_SAXIGP3AWVALID,
	o_SAXIGP3BID[5:0],
	i_SAXIGP3BREADY,
	o_SAXIGP3BRESP[1:0],
	o_SAXIGP3BVALID,
	o_SAXIGP3RACOUNT[3:0],
	io_SAXIGP3RCLK,
	o_SAXIGP3RCOUNT[7:0],
	io_SAXIGP3RDATA[127:0],
	o_SAXIGP3RID[5:0],
	o_SAXIGP3RLAST,
	i_SAXIGP3RREADY,
	o_SAXIGP3RRESP[1:0],
	o_SAXIGP3RVALID,
	o_SAXIGP3WACOUNT[3:0],
	io_SAXIGP3WCLK,
	o_SAXIGP3WCOUNT[7:0],
	io_SAXIGP3WDATA[127:0],
	i_SAXIGP3WLAST,
	o_SAXIGP3WREADY,
	io_SAXIGP3WSTRB[15:0],
	i_SAXIGP3WVALID,

	# AXI GP4 Subordinate
	i_SAXIGP4ARADDR[48:0],
	i_SAXIGP4ARBURST[1:0],
	i_SAXIGP4ARCACHE[3:0],
	i_SAXIGP4ARID[5:0],
	i_SAXIGP4ARLEN[7:0],
	i_SAXIGP4ARLOCK,
	i_SAXIGP4ARPROT[2:0],
	i_SAXIGP4ARQOS[3:0],
	o_SAXIGP4ARREADY,
	i_SAXIGP4ARSIZE[2:0],
	i_SAXIGP4ARUSER,
	i_SAXIGP4ARVALID,
	i_SAXIGP4AWADDR[48:0],
	i_SAXIGP4AWBURST[1:0],
	i_SAXIGP4AWCACHE[3:0],
	i_SAXIGP4AWID[5:0],
	i_SAXIGP4AWLEN[7:0],
	i_SAXIGP4AWLOCK,
	i_SAXIGP4AWPROT[2:0],
	i_SAXIGP4AWQOS[3:0],
	o_SAXIGP4AWREADY,
	i_SAXIGP4AWSIZE[2:0],
	i_SAXIGP4AWUSER,
	i_SAXIGP4AWVALID,
	o_SAXIGP4BID[5:0],
	i_SAXIGP4BREADY,
	o_SAXIGP4BRESP[1:0],
	o_SAXIGP4BVALID,
	o_SAXIGP4RACOUNT[3:0],
	io_SAXIGP4RCLK,
	o_SAXIGP4RCOUNT[7:0],
	io_SAXIGP4RDATA[127:0],
	o_SAXIGP4RID[5:0],
	o_SAXIGP4RLAST,
	i_SAXIGP4RREADY,
	o_SAXIGP4RRESP[1:0],
	o_SAXIGP4RVALID,
	o_SAXIGP4WACOUNT[3:0],
	io_SAXIGP4WCLK,
	o_SAXIGP4WCOUNT[7:0],
	io_SAXIGP4WDATA[127:0],
	i_SAXIGP4WLAST,
	o_SAXIGP4WREADY,
	io_SAXIGP4WSTRB[15:0],
	i_SAXIGP4WVALID,

	# AXI GP5 Subordinate
	i_SAXIGP5ARADDR[48:0],
	i_SAXIGP5ARBURST[1:0],
	i_SAXIGP5ARCACHE[3:0],
	i_SAXIGP5ARID[5:0],
	i_SAXIGP5ARLEN[7:0],
	i_SAXIGP5ARLOCK,
	i_SAXIGP5ARPROT[2:0],
	i_SAXIGP5ARQOS[3:0],
	o_SAXIGP5ARREADY,
	i_SAXIGP5ARSIZE[2:0],
	i_SAXIGP5ARUSER,
	i_SAXIGP5ARVALID,
	i_SAXIGP5AWADDR[48:0],
	i_SAXIGP5AWBURST[1:0],
	i_SAXIGP5AWCACHE[3:0],
	i_SAXIGP5AWID[5:0],
	i_SAXIGP5AWLEN[7:0],
	i_SAXIGP5AWLOCK,
	i_SAXIGP5AWPROT[2:0],
	i_SAXIGP5AWQOS[3:0],
	o_SAXIGP5AWREADY,
	i_SAXIGP5AWSIZE[2:0],
	i_SAXIGP5AWUSER,
	i_SAXIGP5AWVALID,
	o_SAXIGP5BID[5:0],
	i_SAXIGP5BREADY,
	o_SAXIGP5BRESP[1:0],
	o_SAXIGP5BVALID,
	o_SAXIGP5RACOUNT[3:0],
	io_SAXIGP5RCLK,
	o_SAXIGP5RCOUNT[7:0],
	io_SAXIGP5RDATA[127:0],
	o_SAXIGP5RID[5:0],
	o_SAXIGP5RLAST,
	i_SAXIGP5RREADY,
	o_SAXIGP5RRESP[1:0],
	o_SAXIGP5RVALID,
	o_SAXIGP5WACOUNT[3:0],
	io_SAXIGP5WCLK,
	o_SAXIGP5WCOUNT[7:0],
	io_SAXIGP5WDATA[127:0],
	i_SAXIGP5WLAST,
	o_SAXIGP5WREADY,
	io_SAXIGP5WSTRB[15:0],
	i_SAXIGP5WVALID,

	# AXI GP6 Subordinate
	i_SAXIGP6ARADDR[48:0],
	i_SAXIGP6ARBURST[1:0],
	i_SAXIGP6ARCACHE[3:0],
	i_SAXIGP6ARID[5:0],
	i_SAXIGP6ARLEN[7:0],
	i_SAXIGP6ARLOCK,
	i_SAXIGP6ARPROT[2:0],
	i_SAXIGP6ARQOS[3:0],
	o_SAXIGP6ARREADY,
	i_SAXIGP6ARSIZE[2:0],
	i_SAXIGP6ARUSER,
	i_SAXIGP6ARVALID,
	i_SAXIGP6AWADDR[48:0],
	i_SAXIGP6AWBURST[1:0],
	i_SAXIGP6AWCACHE[3:0],
	i_SAXIGP6AWID[5:0],
	i_SAXIGP6AWLEN[7:0],
	i_SAXIGP6AWLOCK,
	i_SAXIGP6AWPROT[2:0],
	i_SAXIGP6AWQOS[3:0],
	o_SAXIGP6AWREADY,
	i_SAXIGP6AWSIZE[2:0],
	i_SAXIGP6AWUSER,
	i_SAXIGP6AWVALID,
	o_SAXIGP6BID[5:0],
	i_SAXIGP6BREADY,
	o_SAXIGP6BRESP[1:0],
	o_SAXIGP6BVALID,
	o_SAXIGP6RACOUNT[3:0],
	io_SAXIGP6RCLK,
	o_SAXIGP6RCOUNT[7:0],
	io_SAXIGP6RDATA[127:0],
	o_SAXIGP6RID[5:0],
	o_SAXIGP6RLAST,
	i_SAXIGP6RREADY,
	o_SAXIGP6RRESP[1:0],
	o_SAXIGP6RVALID,
	o_SAXIGP6WACOUNT[3:0],
	io_SAXIGP6WCLK,
	o_SAXIGP6WCOUNT[7:0],
	io_SAXIGP6WDATA[127:0],
	i_SAXIGP6WLAST,
	o_SAXIGP6WREADY,
	io_SAXIGP6WSTRB[15:0],
	i_SAXIGP6WVALID,

	# STM Events
	i_STMEVENT[59:0]
)



PS8_TEST ps8_test (
	#= all of the same signals in PS8, also the following =#

	o_DBGPATHFIFOBYPASS,

	i_FMIOCHARAFIFSFPDTESTINPUT,
	o_FMIOCHARAFIFSFPDTESTOUTPUT,
	i_FMIOCHARAFIFSFPDTESTSELECTN,

	i_FMIOCHARAFIFSLPDTESTINPUT,
	o_FMIOCHARAFIFSLPDTESTOUTPUT,
	i_FMIOCHARAFIFSLPDTESTSELECTN,

	i_FMIOCHARGEMSELECTION[1:0],
	i_FMIOCHARGEMTESTINPUT,
	o_FMIOCHARGEMTESTOUTPUT,
	i_FMIOCHARGEMTESTSELECTN,

	i_FMIOSD0DLLTESTINN[3:0],
	o_FMIOSD0DLLTESTOUT[7:0],

	i_FMIOSD1DLLTESTINN[3:0],
	o_FMIOSD1DLLTESTOUT[7:0],

	i_FMIOTESTGEMSCANMUX1,
	i_FMIOTESTGEMSCANMUX2,

	i_FMIOTESTIOCHARSCANCLOCK,
	i_FMIOTESTIOCHARSCANENABLE,
	i_FMIOTESTIOCHARSCANIN,
	o_FMIOTESTIOCHARSCANOUT,
	i_FMIOTESTIOCHARSCANRESETN,

	i_FMIOTESTQSPISCANMUX1N,

	i_FMIOTESTSDIOSCANMUX1,
	i_FMIOTESTSDIOSCANMUX2,

	o_FPDPLLTESTOUT[31:0],

	o_FPDPLSPARE0OUT,
	o_FPDPLSPARE1OUT,
	o_FPDPLSPARE2OUT,
	o_FPDPLSPARE3OUT,
	o_FPDPLSPARE4OUT,

	i_IAFECMNBGENABLELOWLEAKAGE,
	i_IAFECMNBGISOCTRLBAR,
	i_IAFECMNBGPD,
	i_IAFECMNBGPDBGOK,
	i_IAFECMNBGPDPTAT,
	i_IAFECMNCALIBENABLELOWLEAKAGE,
	i_IAFECMNCALIBENICONST,
	i_IAFECMNCALIBISOCTRLBAR,

	i_IAFEMODE,

	i_IAFEPLLCOARSECODE[10:0],
	i_IAFEPLLENCLOCKHSDIV2,
	i_IAFEPLLFBDIV[15:0],
	i_IAFEPLLLOADFBDIV,
	i_IAFEPLLPD,
	i_IAFEPLLPDHSCLOCKR,
	i_IAFEPLLPDPFD,
	i_IAFEPLLRSTFDBKDIV,
	i_IAFEPLLSTARTLOOP,
	i_IAFEPLLV2ICODE[5:0],
	i_IAFEPLLV2IPROG[4:0],
	i_IAFEPLLVCOCNTWINDOW,

	i_IAFERXHSRXCLOCKSTOPREQ,
	i_IAFERXISOHSRXCTRLBAR,
	i_IAFERXISOLFPSCTRLBAR,
	i_IAFERXISOSIGDETCTRLBAR,
	i_IAFERXMPHYGATESYMBOLCLK,
	i_IAFERXMPHYMUXHSBLS,
	i_IAFERXPIPERXEQTRAINING,
	i_IAFERXPIPERXTERMENABLE,
	i_IAFERXRXPMAREFCLKDIG,
	i_IAFERXRXPMARSTB,
	i_IAFERXSYMBOLCLKBY2PL,
	i_IAFERXUPHYBIASGENICONSTCOREMIRRORENABLE,
	i_IAFERXUPHYBIASGENICONSTIOMIRRORENABLE,
	i_IAFERXUPHYBIASGENIRCONSTCOREMIRRORENABLE,
	i_IAFERXUPHYENABLECDR,
	i_IAFERXUPHYENABLELOWLEAKAGE,
	i_IAFERXUPHYHSCLKDIVISIONFACTOR[1:0],
	i_IAFERXUPHYHSRXRSTB,
	i_IAFERXUPHYPDNHSDES,
	i_IAFERXUPHYPDSAMPC2C,
	i_IAFERXUPHYPDSAMPC2CECLK,
	i_IAFERXUPHYPSOCLKLANE,
	i_IAFERXUPHYPSOEQ,
	i_IAFERXUPHYPSOHSRXDIG,
	i_IAFERXUPHYPSOIQPI,
	i_IAFERXUPHYPSOLFPSBCN,
	i_IAFERXUPHYPSOSAMPFLOPS,
	i_IAFERXUPHYPSOSIGDET,
	i_IAFERXUPHYRESTORECALCODE,
	i_IAFERXUPHYRESTORECALCODEDATA[7:0],
	i_IAFERXUPHYRUNCALIB,
	i_IAFERXUPHYRXLANEPOLARITYSWAP,
	i_IAFERXUPHYRXPMAOPMODE[7:0],
	i_IAFERXUPHYSTARTLOOPPLL,

	i_IAFETXANAIFRATE[1:0],
	i_IAFETXENABLEHSCLKDIVISION[1:0],
	i_IAFETXENABLELDO,
	i_IAFETXENABLEREF,
	i_IAFETXENABLESUPPLYHSCLK,
	i_IAFETXENABLESUPPLYPIPE,
	i_IAFETXENABLESUPPLYSERIALIZER,
	i_IAFETXENABLESUPPLYUPHY,
	i_IAFETXENDIGSUBLPMODE,
	i_IAFETXHSSERRSTB,
	i_IAFETXHSSYMBOL[19:0],
	i_IAFETXISOCTRLBAR,
	i_IAFETXLFPSCLK,
	i_IAFETXLPBKSEL[2:0],
	i_IAFETXMPHYTXLSDATA,
	i_IAFETXPIPETXENABLEIDLEMODE[1:0],
	i_IAFETXPIPETXENABLELFPS[1:0],
	i_IAFETXPIPETXENABLERXDET,
	i_IAFETXPIPETXFASTESTCOMMONMODE,
	i_IAFETXPLLSYMBCLK2,
	i_IAFETXPMADIGDIGITALRESETN,
	i_IAFETXSERIALIZERRSTB,
	i_IAFETXSERIALIZERRSTREL,
	i_IAFETXSERISOCTRLBAR,
	i_IAFETXUPHYTXPMAOPMODE[7:0],

	i_IBGCALAFEMODE,

	i_IDBGL0RXCLK,
	i_IDBGL0TXCLK,
	i_IDBGL1RXCLK,
	i_IDBGL1TXCLK,
	i_IDBGL2RXCLK,
	i_IDBGL2TXCLK,
	i_IDBGL3RXCLK,
	i_IDBGL3TXCLK,

	i_IOCHARAUDIOINTESTDATA,
	i_IOCHARAUDIOMUXSELN,
	o_IOCHARAUDIOOUTTESTDATA,

	i_IOCHARVIDEOINTESTDATA,
	i_IOCHARVIDEOMUXSELN,
	o_IOCHARVIDEOOUTTESTDATA,

	i_IPLLAFEMODE,

	o_LPDPLLTESTOUT[31:0],

	o_LPDPLSPARE0OUT,
	o_LPDPLSPARE1OUT,
	o_LPDPLSPARE2OUT,
	o_LPDPLSPARE3OUT,
	o_LPDPLSPARE4OUT,

	o_OAFECMNCALIBCOMPOUT,
	o_OAFEPGAVDDCR,
	o_OAFEPGAVDDIO,
	o_OAFEPGDVDDCR,
	o_OAFEPGSTATICAVDDCR,
	o_OAFEPGSTATICAVDDIO,
	o_OAFEPLLCLKSYMHS,
	o_OAFEPLLDCOCOUNT[12:0],
	o_OAFEPLLFBCLKFRAC,
	o_OAFERXHSRXCLOCKSTOPACK,
	o_OAFERXPIPELFPSBCNRXELECIDLE,
	o_OAFERXPIPESIGDET,
	o_OAFERXSYMBOL[19:0],
	o_OAFERXSYMBOLCLKBY2,
	o_OAFERXUPHYRXCALIBDONE,
	o_OAFERXUPHYSAVECALCODE,
	o_OAFERXUPHYSAVECALCODEDATA[7:0],
	o_OAFERXUPHYSTARTLOOPBUF,
	o_OAFETXDIGRESETRELACK,
	o_OAFETXPIPETXDNRXDET,
	o_OAFETXPIPETXDPRXDET,

	o_ODBGL0PHYSTATUS,
	o_ODBGL0POWERDOWN[1:0],
	o_ODBGL0RATE[1:0],
	o_ODBGL0RSTB,
	o_ODBGL0RXCLK,
	o_ODBGL0RXDATA[19:0],
	o_ODBGL0RXDATAK[1:0],
	o_ODBGL0RXELECIDLE,
	o_ODBGL0RXPOLARITY,
	o_ODBGL0RXSGMIIENCDET,
	o_ODBGL0RXSTATUS[2:0],
	o_ODBGL0RXVALID,
	o_ODBGL0SATACORECLOCKREADY,
	o_ODBGL0SATACOREREADY,
	o_ODBGL0SATACORERXDATA[19:0],
	o_ODBGL0SATACORERXDATAVALID[1:0],
	o_ODBGL0SATACORERXSIGNALDET,
	o_ODBGL0SATAPHYCTRLPARTIAL,
	o_ODBGL0SATAPHYCTRLRESET,
	o_ODBGL0SATAPHYCTRLRXRATE[1:0],
	o_ODBGL0SATAPHYCTRLRXRST,
	o_ODBGL0SATAPHYCTRLSLUMBER,
	o_ODBGL0SATAPHYCTRLTXDATA[19:0],
	o_ODBGL0SATAPHYCTRLTXIDLE,
	o_ODBGL0SATAPHYCTRLTXRATE[1:0],
	o_ODBGL0SATAPHYCTRLTXRST,
	o_ODBGL0TXCLK,
	o_ODBGL0TXDATA[19:0],
	o_ODBGL0TXDATAK[1:0],
	o_ODBGL0TXDETRXLPBACK,
	o_ODBGL0TXELECIDLE,
	o_ODBGL0TXSGMIIEWRAP,

	o_ODBGL1PHYSTATUS,
	o_ODBGL1POWERDOWN[1:0],
	o_ODBGL1RATE[1:0],
	o_ODBGL1RSTB,
	o_ODBGL1RXCLK,
	o_ODBGL1RXDATA[19:0],
	o_ODBGL1RXDATAK[1:0],
	o_ODBGL1RXELECIDLE,
	o_ODBGL1RXPOLARITY,
	o_ODBGL1RXSGMIIENCDET,
	o_ODBGL1RXSTATUS[2:0],
	o_ODBGL1RXVALID,
	o_ODBGL1SATACORECLOCKREADY,
	o_ODBGL1SATACOREREADY,
	o_ODBGL1SATACORERXDATA[19:0],
	o_ODBGL1SATACORERXDATAVALID[1:0],
	o_ODBGL1SATACORERXSIGNALDET,
	o_ODBGL1SATAPHYCTRLPARTIAL,
	o_ODBGL1SATAPHYCTRLRESET,
	o_ODBGL1SATAPHYCTRLRXRATE[1:0],
	o_ODBGL1SATAPHYCTRLRXRST,
	o_ODBGL1SATAPHYCTRLSLUMBER,
	o_ODBGL1SATAPHYCTRLTXDATA[19:0],
	o_ODBGL1SATAPHYCTRLTXIDLE,
	o_ODBGL1SATAPHYCTRLTXRATE[1:0],
	o_ODBGL1SATAPHYCTRLTXRST,
	o_ODBGL1TXCLK,
	o_ODBGL1TXDATA[19:0],
	o_ODBGL1TXDATAK[1:0],
	o_ODBGL1TXDETRXLPBACK,
	o_ODBGL1TXELECIDLE,
	o_ODBGL1TXSGMIIEWRAP,

	o_ODBGL2PHYSTATUS,
	o_ODBGL2POWERDOWN[1:0],
	o_ODBGL2RATE[1:0],
	o_ODBGL2RSTB,
	o_ODBGL2RXCLK,
	o_ODBGL2RXDATA[19:0],
	o_ODBGL2RXDATAK[1:0],
	o_ODBGL2RXELECIDLE,
	o_ODBGL2RXPOLARITY,
	o_ODBGL2RXSGMIIENCDET,
	o_ODBGL2RXSTATUS[2:0],
	o_ODBGL2RXVALID,
	o_ODBGL2SATACORECLOCKREADY,
	o_ODBGL2SATACOREREADY,
	o_ODBGL2SATACORERXDATA[19:0],
	o_ODBGL2SATACORERXDATAVALID[1:0],
	o_ODBGL2SATACORERXSIGNALDET,
	o_ODBGL2SATAPHYCTRLPARTIAL,
	o_ODBGL2SATAPHYCTRLRESET,
	o_ODBGL2SATAPHYCTRLRXRATE[1:0],
	o_ODBGL2SATAPHYCTRLRXRST,
	o_ODBGL2SATAPHYCTRLSLUMBER,
	o_ODBGL2SATAPHYCTRLTXDATA[19:0],
	o_ODBGL2SATAPHYCTRLTXIDLE,
	o_ODBGL2SATAPHYCTRLTXRATE[1:0],
	o_ODBGL2SATAPHYCTRLTXRST,
	o_ODBGL2TXCLK,
	o_ODBGL2TXDATA[19:0],
	o_ODBGL2TXDATAK[1:0],
	o_ODBGL2TXDETRXLPBACK,
	o_ODBGL2TXELECIDLE,
	o_ODBGL2TXSGMIIEWRAP,

	o_ODBGL3PHYSTATUS,
	o_ODBGL3POWERDOWN[1:0],
	o_ODBGL3RATE[1:0],
	o_ODBGL3RSTB,
	o_ODBGL3RXCLK,
	o_ODBGL3RXDATA[19:0],
	o_ODBGL3RXDATAK[1:0],
	o_ODBGL3RXELECIDLE,
	o_ODBGL3RXPOLARITY,
	o_ODBGL3RXSGMIIENCDET,
	o_ODBGL3RXSTATUS[2:0],
	o_ODBGL3RXVALID,
	o_ODBGL3SATACORECLOCKREADY,
	o_ODBGL3SATACOREREADY,
	o_ODBGL3SATACORERXDATA[19:0],
	o_ODBGL3SATACORERXDATAVALID[1:0],
	o_ODBGL3SATACORERXSIGNALDET,
	o_ODBGL3SATAPHYCTRLPARTIAL,
	o_ODBGL3SATAPHYCTRLRESET,
	o_ODBGL3SATAPHYCTRLRXRATE[1:0],
	o_ODBGL3SATAPHYCTRLRXRST,
	o_ODBGL3SATAPHYCTRLSLUMBER,
	o_ODBGL3SATAPHYCTRLTXDATA[19:0],
	o_ODBGL3SATAPHYCTRLTXIDLE,
	o_ODBGL3SATAPHYCTRLTXRATE[1:0],
	o_ODBGL3SATAPHYCTRLTXRST,
	o_ODBGL3TXCLK,
	o_ODBGL3TXDATA[19:0],
	o_ODBGL3TXDATAK[1:0],
	o_ODBGL3TXDETRXLPBACK,
	o_ODBGL3TXELECIDLE,
	o_ODBGL3TXSGMIIEWRAP,



	i_PLFPDPLLTESTCKSELN[2:0],
	i_PLFPDPLLTESTFRACTCLKSELN,
	i_PLFPDPLLTESTFRACTENN,
	i_PLFPDPLLTESTMUXSEL[1:0],
	i_PLFPDPLLTESTSEL[3:0],
	i_PLFPDSPARE0IN,
	i_PLFPDSPARE1IN,
	i_PLFPDSPARE2IN,
	i_PLFPDSPARE3IN,
	i_PLFPDSPARE4IN,
	i_PLFPGASTOP[3:0],

	i_PLLAUXREFCLKFPD[2:0],
	i_PLLAUXREFCLKLPD[1:0],
	i_PLLPDPLLTESTCKSELN[2:0],
	i_PLLPDPLLTESTFRACTCLKSELN,
	i_PLLPDPLLTESTFRACTENN,
	i_PLLPDPLLTESTMUXSEL,
	i_PLLPDPLLTESTSEL[3:0],
	i_PLLPDSPARE0IN,
	i_PLLPDSPARE1IN,
	i_PLLPDSPARE2IN,
	i_PLLPDSPARE3IN,
	i_PLLPDSPARE4IN,

	i_PSTPPLCLK[3:0],
	i_PSTPPLIN[31:0],
	o_PSTPPLOUT[31:0],
	i_PSTPPLTS[31:0],


	i_TESTADC2IN[31:0],
	i_TESTADCCLK[3:0],
	i_TESTADCIN[31:0],
	o_TESTADCOUT[19:0],
	o_TESTAMSOSC[7:0],

	i_TESTBSCANACMODE,
	i_TESTBSCANACTEST,
	i_TESTBSCANCLOCKDR,
	i_TESTBSCANENN,
	i_TESTBSCANEXTEST,
	i_TESTBSCANINITMEMORY,
	i_TESTBSCANINTEST,
	i_TESTBSCANMISRJTAGLOAD,
	i_TESTBSCANMODEC,
	i_TESTBSCANRESETTAPB,
	i_TESTBSCANSHIFTDR,
	i_TESTBSCANTDI,
	i_TESTBSCANTDO,
	i_TESTBSCANUPDATEDR,

	i_TESTCHARMODEFPDN,
	i_TESTCHARMODELPDN,
	i_TESTCONVST,
	i_TESTDADDR[7:0],
	o_TESTDB[15:0],
	i_TESTDCLK,
	o_TESTDDR2PLDCDSKEWOUT,
	i_TESTDEN,
	i_TESTDI[15:0],
	o_TESTDO[15:0],
	o_TESTDRDY,
	i_TESTDWE,
	o_TESTMONDATA[15:0],

	i_TESTPL2DDRDCDSAMPLEPULSE,

	o_TESTPLPLLLOCKOUT[4:0],

	i_TESTPLSCANCHOPPERSI,
	o_TESTPLSCANCHOPPERSO,
	i_TESTPLSCANCHOPPERTRIG,
	i_TESTPLSCANCLK0,
	i_TESTPLSCANCLK1,
	i_TESTPLSCANEDTCLK,
	i_TESTPLSCANEDTINAPU,
	i_TESTPLSCANEDTINCPU,
	i_TESTPLSCANEDTINDDR[3:0],
	i_TESTPLSCANEDTINFP[9:0],
	i_TESTPLSCANEDTINGPU[3:0],
	i_TESTPLSCANEDTINLP[8:0],
	i_TESTPLSCANEDTINUSB3[1:0],

	o_TESTPLSCANEDTOUTAPU,
	o_TESTPLSCANEDTOUTCPU0,
	o_TESTPLSCANEDTOUTCPU1,
	o_TESTPLSCANEDTOUTCPU2,
	o_TESTPLSCANEDTOUTCPU3,
	o_TESTPLSCANEDTOUTDDR[3:0],
	o_TESTPLSCANEDTOUTFP[9:0],
	o_TESTPLSCANEDTOUTGPU[3:0],
	o_TESTPLSCANEDTOUTLP[8:0],
	o_TESTPLSCANEDTOUTUSB3[1:0],
	i_TESTPLSCANEDTUPDATE,
	i_TESTPLSCANENABLE,
	i_TESTPLSCANENABLESLCREN,
	i_TESTPLSCANPLLRESET,
	i_TESTPLSCANRESETN,
	i_TESTPLSCANSLCRCONFIGCLK,
	i_TESTPLSCANSLCRCONFIGRSTN,
	i_TESTPLSCANSLCRCONFIGSI,
	o_TESTPLSCANSLCRCONFIGSO,
	i_TESTPLSCANSPAREIN0,
	i_TESTPLSCANSPAREIN1,
	i_TESTPLSCANSPAREIN2,
	o_TESTPLSCANSPAREOUT0,
	o_TESTPLSCANSPAREOUT1,
	i_TESTPLSCANWRAPCLK,
	i_TESTPLSCANWRAPISHIFT,
	i_TESTPLSCANWRAPOSHIFT,

	i_TESTUSB0FUNCMUX0N,
	i_TESTUSB0SCANMUX0N,

	i_TESTUSB1FUNCMUX0N,
	i_TESTUSB1SCANMUX0N,

	i_TSTRTCCALIBREGIN[20:0],
	o_TSTRTCCALIBREGOUT[20:0],
	i_TSTRTCCALIBREGWE,

	i_TSTRTCCLK,
	i_TSTRTCDISABLEBATOP,

	o_TSTRTCOSCCLKOUT,
	i_TSTRTCOSCCNTRLIN[3:0],
	o_TSTRTCOSCCNTRLOUT[3:0],
	i_TSTRTCOSCCNTRLWE,

	o_TSTRTCSECCOUNTEROUT[31:0],
	o_TSTRTCSECONDSRAWINT,
	i_TSTRTCSECRELOAD,
	i_TSTRTCTESTCLOCKSELECTN,
	i_TSTRTCTESTMODEN,
	o_TSTRTCTICKCOUNTEROUT[15:0],
	i_TSTRTCTIMESETREGIN[31:0],
	o_TSTRTCTIMESETREGOUT[31:0],
	i_TSTRTCTIMESETREGWE,

)

"""

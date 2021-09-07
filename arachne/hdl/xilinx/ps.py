# SPDX-License-Identifier: BSD-3-Clause

from nmigen import *


__all__ = (,)

_PS7_MIO_MAPPING = {
	# PN, PKG: PINS (MIO0...MION)
	('xc7z007s', 'clg225' ): {
		'mio': [

		],
		'ddr': { },
		'core': { 'clk': 'C7', 'por_n': 'C9', 'srst_n': 'B11' },
	},
	('xc7z007s', 'clg400' ): {
		'mio': [

		],
		'ddr': { },
		'core': { 'clk': 'E7', 'por_n': 'C7', 'srst_n': 'B10' },
	},
	('xc7z010',  'clg225' ): {
		'mio': [

		],
		'ddr': { },
		'core': { 'clk': 'C7', 'por_n': 'C9', 'srst_n': 'B11' },
	},
	('xc7z010',  'clg400' ): {
		'mio': [

		],
		'ddr': { },
		'core': { 'clk': 'E7', 'por_n': 'C7', 'srst_n': 'B10' },
	},
	('xc7z012s', 'clg485' ): {
		'mio': [

		],
		'ddr': { },
		'core': { 'clk': 'F16', 'por_n': 'B18', 'srst_n': 'C14' },
	},
	('xc7z014s', 'clg400' ): {
		'mio': [

		],
		'ddr': { },
		'core': { 'clk': 'E7', 'por_n': 'C7', 'srst_n': 'B10' },
	},
	('xc7z014s', 'clg484' ): {
		'mio': [

		],
		'ddr': { },
		'core': { 'clk': 'F7', 'por_n': 'B5', 'srst_n': 'C9' },
	},
	('xc7z015',  'clg485' ): {
		'mio': [

		],
		'ddr': { },
		'core': { 'clk': 'F16', 'por_n': 'B18', 'srst_n': 'C14' },
	},
	('xc7z020',  'clg400' ): {
		'mio': [

		],
		'ddr': { },
		'core': { 'clk': 'E7', 'por_n': 'C7', 'srst_n': 'B10' },
	},
	('xc7z020',  'clg484' ): {
		'mio': [

		],
		'ddr': { },
		'core': { 'clk': 'F7', 'por_n': 'B5', 'srst_n': 'C9' },
	},
	('xc7z030',  'fbg484' ): {
		'mio': [

		],
		'ddr': { },
		'core': { 'clk': 'A12', 'por_n': 'C12', 'srst_n': 'E11' },
	},
	('xc7z030',  'fbg676' ): {
		'mio': [

		],
		'ddr': { },
		'core': { 'clk': 'B24', 'por_n': 'C23', 'srst_n': 'A22' },
	},
	('xc7z030',  'ffg676' ): {
		'mio': [

		],
		'ddr': { },
		'core': { 'clk': 'B24', 'por_n': 'C23', 'srst_n': 'A22' },
	},
	('xc7z030',  'sbg485' ): {
		'mio': [

		],
		'ddr': { },
		'core': { 'clk': 'F16', 'por_n': 'B18', 'srst_n': 'C14' },
	},
	('xc7z035',  'fbg676' ): {
		'mio': [

		],
		'ddr': { },
		'core': { 'clk': 'B24', 'por_n': 'C23', 'srst_n': 'A22' },
	},
	('xc7z035',  'ffg676' ): {
		'mio': [

		],
		'ddr': { },
		'core': { 'clk': 'B24', 'por_n': 'C23', 'srst_n': 'A22' },
	},
	('xc7z035',  'ffg900' ): {
		'mio': [

		],
		'ddr': { },
		'core': { 'clk': 'A22', 'por_n': 'D21', 'srst_n': 'B19' },
	},
	('xc7z045',  'fbg676' ): {
		'mio': [

		],
		'ddr': { },
		'core': { 'clk': 'B24', 'por_n': 'C23', 'srst_n': 'A22' },
	},
	('xc7z045',  'ffg676' ): {
		'mio': [

		],
		'ddr': { },
		'core': { 'clk': 'B24', 'por_n': 'C23', 'srst_n': 'A22' },
	},
	('xc7z045',  'ffg900' ): {
		'mio': [

		],
		'ddr': { },
		'core': { 'clk': 'A22', 'por_n': 'D21', 'srst_n': 'B19' },
	},
	('xc7z100',  'ffg1156'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'clk': 'H24', 'por_n': 'F24', 'srst_n': 'C24' },
	},
	('xc7z100',  'ffg900' ): {
		'mio': [

		],
		'ddr': { },
		'core': { 'clk': 'A22', 'por_n': 'D21', 'srst_n': 'B19' },
	},
}

_PS8_MIO_MAPPING = {
	# PN, PKG: PINS (MIO0...MION)
	('xczu11eg', 'ffvb1517'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'AC26', 'error_out': 'Y28', 'error_status': 'AA28', 'init_n': 'AC27', 'tck': 'AD25', 'tdi': 'AC28', 'tdo': 'AA27', 'tms': 'AC25', 'mode0': 'AA25', 'mode1': 'AA26', 'mode2': 'W27', 'mode3': 'W25', 'padi': 'AB25', 'pado': 'AB26', 'por_n': 'AB28', 'prog_n': 'Y27', 'clk': 'Y25', 'srst_n': 'W26' },
	},
	('xczu11eg', 'ffvc1156'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'N24', 'error_out': 'T25', 'error_status': 'R25', 'init_n': 'P24', 'tck': 'K27', 'tdi': 'J27', 'tdo': 'G28', 'tms': 'H28', 'mode0': 'H27', 'mode1': 'J26', 'mode2': 'K26', 'mode3': 'K25', 'padi': 'M25', 'pado': 'L25', 'por_n': 'M24', 'prog_n': 'T24', 'clk': 'R24', 'srst_n': 'P25' },
	},
	('xczu11eg', 'ffvc1760'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'Y28', 'error_out': 'U27', 'error_status': 'V28', 'init_n': 'V27', 'tck': 'AC26', 'tdi': 'AD25', 'tdo': 'AD27', 'tms': 'AD26', 'mode0': 'AA27', 'mode1': 'AC28', 'mode2': 'AA28', 'mode3': 'AB28', 'padi': 'AE28', 'pado': 'AE27', 'por_n': 'W27', 'prog_n': 'Y27', 'clk': 'AC27', 'srst_n': 'AB27' },
	},
	('xczu11eg', 'ffvf1517'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'AJ31', 'error_out': 'AH32', 'error_status': 'AH31', 'init_n': 'AK30', 'tck': 'AG31', 'tdi': 'AE30', 'tdo': 'AF31', 'tms': 'AE29', 'mode0': 'AH27', 'mode1': 'AH28', 'mode2': 'AJ27', 'mode3': 'AH29', 'padi': 'AJ30', 'pado': 'AJ29', 'por_n': 'AF30', 'prog_n': 'AG30', 'clk': 'AG28', 'srst_n': 'AG29' },
	},
	('xczu15eg', 'ffvb1156'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'W21', 'error_out': 'T21', 'error_status': 'R21', 'init_n': 'V24', 'tck': 'R25', 'tdi': 'U25', 'tdo': 'T25', 'tms': 'R24', 'mode0': 'T22', 'mode1': 'R22', 'mode2': 'T23', 'mode3': 'R23', 'padi': 'V21', 'pado': 'V22', 'por_n': 'V23', 'prog_n': 'U21', 'clk': 'U24', 'srst_n': 'U23' },
	},
	('xczu15eg', 'ffvc900'):  {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'T18', 'error_out': 'P21', 'error_status': 'P22', 'init_n': 'T23', 'tck': 'R20', 'tdi': 'T21', 'tdo': 'T20', 'tms': 'R19', 'mode0': 'U18', 'mode1': 'U19', 'mode2': 'U20', 'mode3': 'U21', 'padi': 'R22', 'pado': 'R23', 'por_n': 'U23', 'prog_n': 'T22', 'clk': 'P20', 'srst_n': 'P19' },
	},
	('xczu17eg', 'ffvb1517'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'AC26', 'error_out': 'Y28', 'error_status': 'AA28', 'init_n': 'AC27', 'tck': 'AD25', 'tdi': 'AC28', 'tdo': 'AA27', 'tms': 'AC25', 'mode0': 'AA25', 'mode1': 'AA26', 'mode2': 'W27', 'mode3': 'W25', 'padi': 'AB25', 'pado': 'AB26', 'por_n': 'AB28', 'prog_n': 'Y27', 'clk': 'Y25', 'srst_n': 'W26' },
	},
	('xczu17eg', 'ffvc1760'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'Y28', 'error_out': 'U27', 'error_status': 'V28', 'init_n': 'V27', 'tck': 'AC26', 'tdi': 'AD25', 'tdo': 'AD27', 'tms': 'AD26', 'mode0': 'AA27', 'mode1': 'AC28', 'mode2': 'AA28', 'mode3': 'AB28', 'padi': 'AE28', 'pado': 'AE27', 'por_n': 'W27', 'prog_n': 'Y27', 'clk': 'AC27', 'srst_n': 'AB27' },
	},
	('xczu17eg', 'ffvd1760'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'W30', 'error_out': 'R30', 'error_status': 'T30', 'init_n': 'V30', 'tck': 'AC29', 'tdi': 'AD28', 'tdo': 'AD29', 'tms': 'AC30', 'mode0': 'V29', 'mode1': 'AB29', 'mode2': 'Y30', 'mode3': 'AA30', 'padi': 'AD30', 'pado': 'AE30', 'por_n': 'T29', 'prog_n': 'U29', 'clk': 'AA29', 'srst_n': 'W29' },
	},
	('xczu17eg', 'ffve1924'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'AH26', 'error_out': 'AD28', 'error_status': 'AD29', 'init_n': 'AH27', 'tck': 'AD26', 'tdi': 'AF29', 'tdo': 'AH28', 'tms': 'AF28', 'mode0': 'AE28', 'mode1': 'AD27', 'mode2': 'AE27', 'mode3': 'AF27', 'padi': 'AG29', 'pado': 'AH29', 'por_n': 'AE26', 'prog_n': 'AF26', 'clk': 'AG27', 'srst_n': 'AG26' },
	},
	('xczu19eg', 'ffvb1517'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'AC26', 'error_out': 'Y28', 'error_status': 'AA28', 'init_n': 'AC27', 'tck': 'AD25', 'tdi': 'AC28', 'tdo': 'AA27', 'tms': 'AC25', 'mode0': 'AA25', 'mode1': 'AA26', 'mode2': 'W27', 'mode3': 'W25', 'padi': 'AB25', 'pado': 'AB26', 'por_n': 'AB28', 'prog_n': 'Y27', 'clk': 'Y25', 'srst_n': 'W26' },
	},
	('xczu19eg', 'ffvc1760'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'Y28', 'error_out': 'U27', 'error_status': 'V28', 'init_n': 'V27', 'tck': 'AC26', 'tdi': 'AD25', 'tdo': 'AD27', 'tms': 'AD26', 'mode0': 'AA27', 'mode1': 'AC28', 'mode2': 'AA28', 'mode3': 'AB28', 'padi': 'AE28', 'pado': 'AE27', 'por_n': 'W27', 'prog_n': 'Y27', 'clk': 'AC27', 'srst_n': 'AB27' },
	},
	('xczu19eg', 'ffvd1760'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'W30', 'error_out': 'R30', 'error_status': 'T30', 'init_n': 'V30', 'tck': 'AC29', 'tdi': 'AD28', 'tdo': 'AD29', 'tms': 'AC30', 'mode0': 'V29', 'mode1': 'AB29', 'mode2': 'Y30', 'mode3': 'AA30', 'padi': 'AD30', 'pado': 'AE30', 'por_n': 'T29', 'prog_n': 'U29', 'clk': 'AA29', 'srst_n': 'W29' },
	},
	('xczu19eg', 'ffve1924'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'AH26', 'error_out': 'AD28', 'error_status': 'AD29', 'init_n': 'AH27', 'tck': 'AD26', 'tdi': 'AF29', 'tdo': 'AH28', 'tms': 'AF28', 'mode0': 'AE28', 'mode1': 'AD27', 'mode2': 'AE27', 'mode3': 'AF27', 'padi': 'AG29', 'pado': 'AH29', 'por_n': 'AE26', 'prog_n': 'AF26', 'clk': 'AG27', 'srst_n': 'AG26' },
	},
	('xczu21dr', 'ffvd1156'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'T26', 'error_out': 'L24', 'error_status': 'L26', 'init_n': 'T24', 'tck': 'N24', 'tdi': 'N25', 'tdo': 'R26', 'tms': 'N26', 'mode0': 'L25', 'mode1': 'M24', 'mode2': 'K24', 'mode3': 'M26', 'padi': 'H24', 'pado': 'J24', 'por_n': 'R25', 'prog_n': 'P25', 'clk': 'P24', 'srst_n': 'T25' },
	},
	('xczu25dr', 'ffve1156'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'T24', 'error_out': 'J24', 'error_status': 'R26', 'init_n': 'R24', 'tck': 'P26', 'tdi': 'M26', 'tdo': 'T26', 'tms': 'N25', 'mode0': 'L26', 'mode1': 'L24', 'mode2': 'K24', 'mode3': 'M24', 'padi': 'K26', 'pado': 'K25', 'por_n': 'N24', 'prog_n': 'P25', 'clk': 'M25', 'srst_n': 'R25' },
	},
	('xczu25dr', 'ffvg1517'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'AB27', 'error_out': 'AF30', 'error_status': 'AC32', 'init_n': 'AB26', 'tck': 'AA29', 'tdi': 'AD31', 'tdo': 'AD32', 'tms': 'AD30', 'mode0': 'AC31', 'mode1': 'AB30', 'mode2': 'AB31', 'mode3': 'AE32', 'padi': 'AE31', 'pado': 'AF31', 'por_n': 'AB29', 'prog_n': 'AA27', 'clk': 'AC30', 'srst_n': 'AB28' },
	},
	('xczu25dr', 'fsve1156'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'T24', 'error_out': 'J24', 'error_status': 'R26', 'init_n': 'R24', 'tck': 'P26', 'tdi': 'M26', 'tdo': 'T26', 'tms': 'N25', 'mode0': 'L26', 'mode1': 'L24', 'mode2': 'K24', 'mode3': 'M24', 'padi': 'K26', 'pado': 'K25', 'por_n': 'N24', 'prog_n': 'P25', 'clk': 'M25', 'srst_n': 'R25' },
	},
	('xczu25dr', 'fsvg1517'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'AB27', 'error_out': 'AF30', 'error_status': 'AC32', 'init_n': 'AB26', 'tck': 'AA29', 'tdi': 'AD31', 'tdo': 'AD32', 'tms': 'AD30', 'mode0': 'AC31', 'mode1': 'AB30', 'mode2': 'AB31', 'mode3': 'AE32', 'padi': 'AE31', 'pado': 'AF31', 'por_n': 'AB29', 'prog_n': 'AA27', 'clk': 'AC30', 'srst_n': 'AB28' },
	},
	('xczu27dr', 'ffve1156'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'T24', 'error_out': 'J24', 'error_status': 'R26', 'init_n': 'R24', 'tck': 'P26', 'tdi': 'M26', 'tdo': 'T26', 'tms': 'N25', 'mode0': 'L26', 'mode1': 'L24', 'mode2': 'K24', 'mode3': 'M24', 'padi': 'K26', 'pado': 'K25', 'por_n': 'N24', 'prog_n': 'P25', 'clk': 'M25', 'srst_n': 'R25' },
	},
	('xczu27dr', 'ffvg1517'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'AB27', 'error_out': 'AF30', 'error_status': 'AC32', 'init_n': 'AB26', 'tck': 'AA29', 'tdi': 'AD31', 'tdo': 'AD32', 'tms': 'AD30', 'mode0': 'AC31', 'mode1': 'AB30', 'mode2': 'AB31', 'mode3': 'AE32', 'padi': 'AE31', 'pado': 'AF31', 'por_n': 'AB29', 'prog_n': 'AA27', 'clk': 'AC30', 'srst_n': 'AB28' },
	},
	('xczu27dr', 'fsve1156'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'T24', 'error_out': 'J24', 'error_status': 'R26', 'init_n': 'R24', 'tck': 'P26', 'tdi': 'M26', 'tdo': 'T26', 'tms': 'N25', 'mode0': 'L26', 'mode1': 'L24', 'mode2': 'K24', 'mode3': 'M24', 'padi': 'K26', 'pado': 'K25', 'por_n': 'N24', 'prog_n': 'P25', 'clk': 'M25', 'srst_n': 'R25' },
	},
	('xczu27dr', 'fsvg1517'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'AB27', 'error_out': 'AF30', 'error_status': 'AC32', 'init_n': 'AB26', 'tck': 'AA29', 'tdi': 'AD31', 'tdo': 'AD32', 'tms': 'AD30', 'mode0': 'AC31', 'mode1': 'AB30', 'mode2': 'AB31', 'mode3': 'AE32', 'padi': 'AE31', 'pado': 'AF31', 'por_n': 'AB29', 'prog_n': 'AA27', 'clk': 'AC30', 'srst_n': 'AB28' },
	},
	('xczu28dr', 'ffve1156'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'T24', 'error_out': 'J24', 'error_status': 'R26', 'init_n': 'R24', 'tck': 'P26', 'tdi': 'M26', 'tdo': 'T26', 'tms': 'N25', 'mode0': 'L26', 'mode1': 'L24', 'mode2': 'K24', 'mode3': 'M24', 'padi': 'K26', 'pado': 'K25', 'por_n': 'N24', 'prog_n': 'P25', 'clk': 'M25', 'srst_n': 'R25' },
	},
	('xczu28dr', 'ffvg1517'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'AB27', 'error_out': 'AF30', 'error_status': 'AC32', 'init_n': 'AB26', 'tck': 'AA29', 'tdi': 'AD31', 'tdo': 'AD32', 'tms': 'AD30', 'mode0': 'AC31', 'mode1': 'AB30', 'mode2': 'AB31', 'mode3': 'AE32', 'padi': 'AE31', 'pado': 'AF31', 'por_n': 'AB29', 'prog_n': 'AA27', 'clk': 'AC30', 'srst_n': 'AB28' },
	},
	('xczu28dr', 'fsve1156'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'T24', 'error_out': 'J24', 'error_status': 'R26', 'init_n': 'R24', 'tck': 'P26', 'tdi': 'M26', 'tdo': 'T26', 'tms': 'N25', 'mode0': 'L26', 'mode1': 'L24', 'mode2': 'K24', 'mode3': 'M24', 'padi': 'K26', 'pado': 'K25', 'por_n': 'N24', 'prog_n': 'P25', 'clk': 'M25', 'srst_n': 'R25' },
	},
	('xczu28dr', 'fsvg1517'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'AB27', 'error_out': 'AF30', 'error_status': 'AC32', 'init_n': 'AB26', 'tck': 'AA29', 'tdi': 'AD31', 'tdo': 'AD32', 'tms': 'AD30', 'mode0': 'AC31', 'mode1': 'AB30', 'mode2': 'AB31', 'mode3': 'AE32', 'padi': 'AE31', 'pado': 'AF31', 'por_n': 'AB29', 'prog_n': 'AA27', 'clk': 'AC30', 'srst_n': 'AB28' },
	},
	('xczu29dr', 'ffvf1760'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'N31', 'error_out': 'AC30', 'error_status': 'AC31', 'init_n': 'P31', 'tck': 'T32', 'tdi': 'U31', 'tdo': 'V31', 'tms': 'W31', 'mode0': 'AA32', 'mode1': 'AB32', 'mode2': 'AB31', 'mode3': 'Y31', 'padi': 'W32', 'pado': 'Y32', 'por_n': 'R32', 'prog_n': 'P32', 'clk': 'U32', 'srst_n': 'R31' },
	},
	('xczu29dr', 'fsvf1760'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'N31', 'error_out': 'AC30', 'error_status': 'AC31', 'init_n': 'P31', 'tck': 'T32', 'tdi': 'U31', 'tdo': 'V31', 'tms': 'W31', 'mode0': 'AA32', 'mode1': 'AB32', 'mode2': 'AB31', 'mode3': 'Y31', 'padi': 'W32', 'pado': 'Y32', 'por_n': 'R32', 'prog_n': 'P32', 'clk': 'U32', 'srst_n': 'R31' },
	},
	('xczu2cg',  'sbva484'):  {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'L12', 'error_out': 'K16', 'error_status': 'K18', 'init_n': 'K15', 'tck': 'H13', 'tdi': 'H12', 'tdo': 'J13', 'tms': 'J12', 'mode0': 'J16', 'mode1': 'H15', 'mode2': 'J15', 'mode3': 'H18', 'padi': 'H17', 'pado': 'J17', 'por_n': 'K12', 'prog_n': 'K14', 'clk': 'H14', 'srst_n': 'K13' },
	},
	('xczu2cg',  'sfva625'):  {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'N21', 'error_out': 'J19', 'error_status': 'L20', 'init_n': 'L19', 'tck': 'K16', 'tdi': 'L15', 'tdo': 'L17', 'tms': 'L18', 'mode0': 'J18', 'mode1': 'J16', 'mode2': 'J17', 'mode3': 'K20', 'padi': 'K17', 'pado': 'K19', 'por_n': 'M20', 'prog_n': 'M18', 'clk': 'K15', 'srst_n': 'N20' },
	},
	('xczu2cg',  'sfvc784'):  {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'M21', 'error_out': 'P17', 'error_status': 'M20', 'init_n': 'P21', 'tck': 'R19', 'tdi': 'R18', 'tdo': 'T21', 'tms': 'N21', 'mode0': 'P19', 'mode1': 'P20', 'mode2': 'R20', 'mode3': 'T20', 'padi': 'N17', 'pado': 'N18', 'por_n': 'P16', 'prog_n': 'R17', 'clk': 'R16', 'srst_n': 'N19' },
	},
	('xczu2eg',  'sbva484'):  {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'L12', 'error_out': 'K16', 'error_status': 'K18', 'init_n': 'K15', 'tck': 'H13', 'tdi': 'H12', 'tdo': 'J13', 'tms': 'J12', 'mode0': 'J16', 'mode1': 'H15', 'mode2': 'J15', 'mode3': 'H18', 'padi': 'H17', 'pado': 'J17', 'por_n': 'K12', 'prog_n': 'K14', 'clk': 'H14', 'srst_n': 'K13' },
	},
	('xczu2eg',  'sfva625'):  {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'N21', 'error_out': 'J19', 'error_status': 'L20', 'init_n': 'L19', 'tck': 'K16', 'tdi': 'L15', 'tdo': 'L17', 'tms': 'L18', 'mode0': 'J18', 'mode1': 'J16', 'mode2': 'J17', 'mode3': 'K20', 'padi': 'K17', 'pado': 'K19', 'por_n': 'M20', 'prog_n': 'M18', 'clk': 'K15', 'srst_n': 'N20' },
	},
	('xczu2eg',  'sfvc784'):  {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'M21', 'error_out': 'P17', 'error_status': 'M20', 'init_n': 'P21', 'tck': 'R19', 'tdi': 'R18', 'tdo': 'T21', 'tms': 'N21', 'mode0': 'P19', 'mode1': 'P20', 'mode2': 'R20', 'mode3': 'T20', 'padi': 'N17', 'pado': 'N18', 'por_n': 'P16', 'prog_n': 'R17', 'clk': 'R16', 'srst_n': 'N19' },
	},
	('xczu39dr', 'ffvf1760'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'N31', 'error_out': 'AC30', 'error_status': 'AC31', 'init_n': 'P31', 'tck': 'T32', 'tdi': 'U31', 'tdo': 'V31', 'tms': 'W31', 'mode0': 'AA32', 'mode1': 'AB32', 'mode2': 'AB31', 'mode3': 'Y31', 'padi': 'W32', 'pado': 'Y32', 'por_n': 'R32', 'prog_n': 'P32', 'clk': 'U32', 'srst_n': 'R31' },
	},
	('xczu39dr', 'fsvf1760'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'N31', 'error_out': 'AC30', 'error_status': 'AC31', 'init_n': 'P31', 'tck': 'T32', 'tdi': 'U31', 'tdo': 'V31', 'tms': 'W31', 'mode0': 'AA32', 'mode1': 'AB32', 'mode2': 'AB31', 'mode3': 'Y31', 'padi': 'W32', 'pado': 'Y32', 'por_n': 'R32', 'prog_n': 'P32', 'clk': 'U32', 'srst_n': 'R31' },
	},
	('xczu3cg',  'sbva484'):  {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'L12', 'error_out': 'K16', 'error_status': 'K18', 'init_n': 'K15', 'tck': 'H13', 'tdi': 'H12', 'tdo': 'J13', 'tms': 'J12', 'mode0': 'J16', 'mode1': 'H15', 'mode2': 'J15', 'mode3': 'H18', 'padi': 'H17', 'pado': 'J17', 'por_n': 'K12', 'prog_n': 'K14', 'clk': 'H14', 'srst_n': 'K13' },
	},
	('xczu3cg',  'sfva625'):  {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'N21', 'error_out': 'J19', 'error_status': 'L20', 'init_n': 'L19', 'tck': 'K16', 'tdi': 'L15', 'tdo': 'L17', 'tms': 'L18', 'mode0': 'J18', 'mode1': 'J16', 'mode2': 'J17', 'mode3': 'K20', 'padi': 'K17', 'pado': 'K19', 'por_n': 'M20', 'prog_n': 'M18', 'clk': 'K15', 'srst_n': 'N20' },
	},
	('xczu3cg',  'sfvc784'):  {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'M21', 'error_out': 'P17', 'error_status': 'M20', 'init_n': 'P21', 'tck': 'R19', 'tdi': 'R18', 'tdo': 'T21', 'tms': 'N21', 'mode0': 'P19', 'mode1': 'P20', 'mode2': 'R20', 'mode3': 'T20', 'padi': 'N17', 'pado': 'N18', 'por_n': 'P16', 'prog_n': 'R17', 'clk': 'R16', 'srst_n': 'N19' },
	},
	('xczu3eg',  'sbva484'):  {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'L12', 'error_out': 'K16', 'error_status': 'K18', 'init_n': 'K15', 'tck': 'H13', 'tdi': 'H12', 'tdo': 'J13', 'tms': 'J12', 'mode0': 'J16', 'mode1': 'H15', 'mode2': 'J15', 'mode3': 'H18', 'padi': 'H17', 'pado': 'J17', 'por_n': 'K12', 'prog_n': 'K14', 'clk': 'H14', 'srst_n': 'K13' },
	},
	('xczu3eg',  'sfva625'):  {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'N21', 'error_out': 'J19', 'error_status': 'L20', 'init_n': 'L19', 'tck': 'K16', 'tdi': 'L15', 'tdo': 'L17', 'tms': 'L18', 'mode0': 'J18', 'mode1': 'J16', 'mode2': 'J17', 'mode3': 'K20', 'padi': 'K17', 'pado': 'K19', 'por_n': 'M20', 'prog_n': 'M18', 'clk': 'K15', 'srst_n': 'N20' },
	},
	('xczu3eg',  'sfvc784'):  {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'M21', 'error_out': 'P17', 'error_status': 'M20', 'init_n': 'P21', 'tck': 'R19', 'tdi': 'R18', 'tdo': 'T21', 'tms': 'N21', 'mode0': 'P19', 'mode1': 'P20', 'mode2': 'R20', 'mode3': 'T20', 'padi': 'N17', 'pado': 'N18', 'por_n': 'P16', 'prog_n': 'R17', 'clk': 'R16', 'srst_n': 'N19' },
	},
	('xczu43dr', 'ffve1156'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'T24', 'error_out': 'J24', 'error_status': 'R26', 'init_n': 'R24', 'tck': 'P26', 'tdi': 'M26', 'tdo': 'T26', 'tms': 'N25', 'mode0': 'L26', 'mode1': 'L24', 'mode2': 'K24', 'mode3': 'M24', 'padi': 'K26', 'pado': 'K25', 'por_n': 'N24', 'prog_n': 'P25', 'clk': 'M25', 'srst_n': 'R25' },
	},
	('xczu43dr', 'ffvg1517'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'AB27', 'error_out': 'AF30', 'error_status': 'AC32', 'init_n': 'AB26', 'tck': 'AA29', 'tdi': 'AD31', 'tdo': 'AD32', 'tms': 'AD30', 'mode0': 'AC31', 'mode1': 'AB30', 'mode2': 'AB31', 'mode3': 'AE32', 'padi': 'AE31', 'pado': 'AF31', 'por_n': 'AB29', 'prog_n': 'AA27', 'clk': 'AC30', 'srst_n': 'AB28' },
	},
	('xczu43dr', 'fsve1156'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'T24', 'error_out': 'J24', 'error_status': 'R26', 'init_n': 'R24', 'tck': 'P26', 'tdi': 'M26', 'tdo': 'T26', 'tms': 'N25', 'mode0': 'L26', 'mode1': 'L24', 'mode2': 'K24', 'mode3': 'M24', 'padi': 'K26', 'pado': 'K25', 'por_n': 'N24', 'prog_n': 'P25', 'clk': 'M25', 'srst_n': 'R25' },
	},
	('xczu43dr', 'fsvg1517'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'AB27', 'error_out': 'AF30', 'error_status': 'AC32', 'init_n': 'AB26', 'tck': 'AA29', 'tdi': 'AD31', 'tdo': 'AD32', 'tms': 'AD30', 'mode0': 'AC31', 'mode1': 'AB30', 'mode2': 'AB31', 'mode3': 'AE32', 'padi': 'AE31', 'pado': 'AF31', 'por_n': 'AB29', 'prog_n': 'AA27', 'clk': 'AC30', 'srst_n': 'AB28' },
	},
	('xczu46dr', 'ffvh1760'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'AA32', 'error_out': 'Y32', 'error_status': 'Y31', 'init_n': 'AB30', 'tck': 'AB31', 'tdi': 'AB32', 'tdo': 'AC31', 'tms': 'AD31', 'mode0': 'AC29', 'mode1': 'AD29', 'mode2': 'AE29', 'mode3': 'AE30', 'padi': 'AD32', 'pado': 'AD33', 'por_n': 'AF29', 'prog_n': 'AA29', 'clk': 'AC30', 'srst_n': 'AA30' },
	},
	('xczu46dr', 'fsvh1760'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'AA32', 'error_out': 'Y32', 'error_status': 'Y31', 'init_n': 'AB30', 'tck': 'AB31', 'tdi': 'AB32', 'tdo': 'AC31', 'tms': 'AD31', 'mode0': 'AC29', 'mode1': 'AD29', 'mode2': 'AE29', 'mode3': 'AE30', 'padi': 'AD32', 'pado': 'AD33', 'por_n': 'AF29', 'prog_n': 'AA29', 'clk': 'AC30', 'srst_n': 'AA30' },
	},
	('xczu47dr', 'ffve1156'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'T24', 'error_out': 'J24', 'error_status': 'R26', 'init_n': 'R24', 'tck': 'P26', 'tdi': 'M26', 'tdo': 'T26', 'tms': 'N25', 'mode0': 'L26', 'mode1': 'L24', 'mode2': 'K24', 'mode3': 'M24', 'padi': 'K26', 'pado': 'K25', 'por_n': 'N24', 'prog_n': 'P25', 'clk': 'M25', 'srst_n': 'R25' },
	},
	('xczu47dr', 'ffvg1517'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'AB27', 'error_out': 'AF30', 'error_status': 'AC32', 'init_n': 'AB26', 'tck': 'AA29', 'tdi': 'AD31', 'tdo': 'AD32', 'tms': 'AD30', 'mode0': 'AC31', 'mode1': 'AB30', 'mode2': 'AB31', 'mode3': 'AE32', 'padi': 'AE31', 'pado': 'AF31', 'por_n': 'AB29', 'prog_n': 'AA27', 'clk': 'AC30', 'srst_n': 'AB28' },
	},
	('xczu47dr', 'fsve1156'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'T24', 'error_out': 'J24', 'error_status': 'R26', 'init_n': 'R24', 'tck': 'P26', 'tdi': 'M26', 'tdo': 'T26', 'tms': 'N25', 'mode0': 'L26', 'mode1': 'L24', 'mode2': 'K24', 'mode3': 'M24', 'padi': 'K26', 'pado': 'K25', 'por_n': 'N24', 'prog_n': 'P25', 'clk': 'M25', 'srst_n': 'R25' },
	},
	('xczu47dr', 'fsvg1517'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'AB27', 'error_out': 'AF30', 'error_status': 'AC32', 'init_n': 'AB26', 'tck': 'AA29', 'tdi': 'AD31', 'tdo': 'AD32', 'tms': 'AD30', 'mode0': 'AC31', 'mode1': 'AB30', 'mode2': 'AB31', 'mode3': 'AE32', 'padi': 'AE31', 'pado': 'AF31', 'por_n': 'AB29', 'prog_n': 'AA27', 'clk': 'AC30', 'srst_n': 'AB28' },
	},
	('xczu48dr', 'ffve1156'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'T24', 'error_out': 'J24', 'error_status': 'R26', 'init_n': 'R24', 'tck': 'P26', 'tdi': 'M26', 'tdo': 'T26', 'tms': 'N25', 'mode0': 'L26', 'mode1': 'L24', 'mode2': 'K24', 'mode3': 'M24', 'padi': 'K26', 'pado': 'K25', 'por_n': 'N24', 'prog_n': 'P25', 'clk': 'M25', 'srst_n': 'R25' },
	},
	('xczu48dr', 'ffvg1517'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'AB27', 'error_out': 'AF30', 'error_status': 'AC32', 'init_n': 'AB26', 'tck': 'AA29', 'tdi': 'AD31', 'tdo': 'AD32', 'tms': 'AD30', 'mode0': 'AC31', 'mode1': 'AB30', 'mode2': 'AB31', 'mode3': 'AE32', 'padi': 'AE31', 'pado': 'AF31', 'por_n': 'AB29', 'prog_n': 'AA27', 'clk': 'AC30', 'srst_n': 'AB28' },
	},
	('xczu48dr', 'fsve1156'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'T24', 'error_out': 'J24', 'error_status': 'R26', 'init_n': 'R24', 'tck': 'P26', 'tdi': 'M26', 'tdo': 'T26', 'tms': 'N25', 'mode0': 'L26', 'mode1': 'L24', 'mode2': 'K24', 'mode3': 'M24', 'padi': 'K26', 'pado': 'K25', 'por_n': 'N24', 'prog_n': 'P25', 'clk': 'M25', 'srst_n': 'R25' },
	},
	('xczu48dr', 'fsvg1517'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'AB27', 'error_out': 'AF30', 'error_status': 'AC32', 'init_n': 'AB26', 'tck': 'AA29', 'tdi': 'AD31', 'tdo': 'AD32', 'tms': 'AD30', 'mode0': 'AC31', 'mode1': 'AB30', 'mode2': 'AB31', 'mode3': 'AE32', 'padi': 'AE31', 'pado': 'AF31', 'por_n': 'AB29', 'prog_n': 'AA27', 'clk': 'AC30', 'srst_n': 'AB28' },
	},
	('xczu49dr', 'ffvf1760'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'N31', 'error_out': 'AC30', 'error_status': 'AC31', 'init_n': 'P31', 'tck': 'T32', 'tdi': 'U31', 'tdo': 'V31', 'tms': 'W31', 'mode0': 'AA32', 'mode1': 'AB32', 'mode2': 'AB31', 'mode3': 'Y31', 'padi': 'W32', 'pado': 'Y32', 'por_n': 'R32', 'prog_n': 'P32', 'clk': 'U32', 'srst_n': 'R31' },
	},
	('xczu49dr', 'fsvf1760'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'N31', 'error_out': 'AC30', 'error_status': 'AC31', 'init_n': 'P31', 'tck': 'T32', 'tdi': 'U31', 'tdo': 'V31', 'tms': 'W31', 'mode0': 'AA32', 'mode1': 'AB32', 'mode2': 'AB31', 'mode3': 'Y31', 'padi': 'W32', 'pado': 'Y32', 'por_n': 'R32', 'prog_n': 'P32', 'clk': 'U32', 'srst_n': 'R31' },
	},
	('xczu4cg',  'fbvb900'):  {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'N22', 'error_out': 'R22', 'error_status': 'R20', 'init_n': 'N18', 'tck': 'L19', 'tdi': 'L20', 'tdo': 'M20', 'tms': 'L21', 'mode0': 'R18', 'mode1': 'R19', 'mode2': 'P21', 'mode3': 'P22', 'padi': 'M21', 'pado': 'N21', 'por_n': 'N19', 'prog_n': 'M19', 'clk': 'P19', 'srst_n': 'P20' },
	},
	('xczu4cg',  'sfvc784'):  {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'M21', 'error_out': 'P17', 'error_status': 'M20', 'init_n': 'P21', 'tck': 'R19', 'tdi': 'R18', 'tdo': 'T21', 'tms': 'N21', 'mode0': 'P19', 'mode1': 'P20', 'mode2': 'R20', 'mode3': 'T20', 'padi': 'N17', 'pado': 'N18', 'por_n': 'P16', 'prog_n': 'R17', 'clk': 'R16', 'srst_n': 'N19' },
	},
	('xczu4eg',  'fbvb900'):  {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'N22', 'error_out': 'R22', 'error_status': 'R20', 'init_n': 'N18', 'tck': 'L19', 'tdi': 'L20', 'tdo': 'M20', 'tms': 'L21', 'mode0': 'R18', 'mode1': 'R19', 'mode2': 'P21', 'mode3': 'P22', 'padi': 'M21', 'pado': 'N21', 'por_n': 'N19', 'prog_n': 'M19', 'clk': 'P19', 'srst_n': 'P20' },
	},
	('xczu4eg',  'sfvc784'):  {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'M21', 'error_out': 'P17', 'error_status': 'M20', 'init_n': 'P21', 'tck': 'R19', 'tdi': 'R18', 'tdo': 'T21', 'tms': 'N21', 'mode0': 'P19', 'mode1': 'P20', 'mode2': 'R20', 'mode3': 'T20', 'padi': 'N17', 'pado': 'N18', 'por_n': 'P16', 'prog_n': 'R17', 'clk': 'R16', 'srst_n': 'N19' },
	},
	('xczu4ev',  'fbvb900'):  {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'N22', 'error_out': 'R22', 'error_status': 'R20', 'init_n': 'N18', 'tck': 'L19', 'tdi': 'L20', 'tdo': 'M20', 'tms': 'L21', 'mode0': 'R18', 'mode1': 'R19', 'mode2': 'P21', 'mode3': 'P22', 'padi': 'M21', 'pado': 'N21', 'por_n': 'N19', 'prog_n': 'M19', 'clk': 'P19', 'srst_n': 'P20' },
	},
	('xczu4ev',  'sfvc784'):  {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'M21', 'error_out': 'P17', 'error_status': 'M20', 'init_n': 'P21', 'tck': 'R19', 'tdi': 'R18', 'tdo': 'T21', 'tms': 'N21', 'mode0': 'P19', 'mode1': 'P20', 'mode2': 'R20', 'mode3': 'T20', 'padi': 'N17', 'pado': 'N18', 'por_n': 'P16', 'prog_n': 'R17', 'clk': 'R16', 'srst_n': 'N19' },
	},
	('xczu5cg',  'fbvb900'):  {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'N22', 'error_out': 'R22', 'error_status': 'R20', 'init_n': 'N18', 'tck': 'L19', 'tdi': 'L20', 'tdo': 'M20', 'tms': 'L21', 'mode0': 'R18', 'mode1': 'R19', 'mode2': 'P21', 'mode3': 'P22', 'padi': 'M21', 'pado': 'N21', 'por_n': 'N19', 'prog_n': 'M19', 'clk': 'P19', 'srst_n': 'P20' },
	},
	('xczu5cg',  'sfvc784'):  {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'M21', 'error_out': 'P17', 'error_status': 'M20', 'init_n': 'P21', 'tck': 'R19', 'tdi': 'R18', 'tdo': 'T21', 'tms': 'N21', 'mode0': 'P19', 'mode1': 'P20', 'mode2': 'R20', 'mode3': 'T20', 'padi': 'N17', 'pado': 'N18', 'por_n': 'P16', 'prog_n': 'R17', 'clk': 'R16', 'srst_n': 'N19' },
	},
	('xczu5eg',  'fbvb900'):  {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'N22', 'error_out': 'R22', 'error_status': 'R20', 'init_n': 'N18', 'tck': 'L19', 'tdi': 'L20', 'tdo': 'M20', 'tms': 'L21', 'mode0': 'R18', 'mode1': 'R19', 'mode2': 'P21', 'mode3': 'P22', 'padi': 'M21', 'pado': 'N21', 'por_n': 'N19', 'prog_n': 'M19', 'clk': 'P19', 'srst_n': 'P20' },
	},
	('xczu5eg',  'sfvc784'):  {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'M21', 'error_out': 'P17', 'error_status': 'M20', 'init_n': 'P21', 'tck': 'R19', 'tdi': 'R18', 'tdo': 'T21', 'tms': 'N21', 'mode0': 'P19', 'mode1': 'P20', 'mode2': 'R20', 'mode3': 'T20', 'padi': 'N17', 'pado': 'N18', 'por_n': 'P16', 'prog_n': 'R17', 'clk': 'R16', 'srst_n': 'N19' },
	},
	('xczu5ev',  'fbvb900'):  {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'N22', 'error_out': 'R22', 'error_status': 'R20', 'init_n': 'N18', 'tck': 'L19', 'tdi': 'L20', 'tdo': 'M20', 'tms': 'L21', 'mode0': 'R18', 'mode1': 'R19', 'mode2': 'P21', 'mode3': 'P22', 'padi': 'M21', 'pado': 'N21', 'por_n': 'N19', 'prog_n': 'M19', 'clk': 'P19', 'srst_n': 'P20' },
	},
	('xczu5ev',  'sfvc784'):  {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'M21', 'error_out': 'P17', 'error_status': 'M20', 'init_n': 'P21', 'tck': 'R19', 'tdi': 'R18', 'tdo': 'T21', 'tms': 'N21', 'mode0': 'P19', 'mode1': 'P20', 'mode2': 'R20', 'mode3': 'T20', 'padi': 'N17', 'pado': 'N18', 'por_n': 'P16', 'prog_n': 'R17', 'clk': 'R16', 'srst_n': 'N19' },
	},
	('xczu6cg',  'ffvb1156'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'W21', 'error_out': 'T21', 'error_status': 'R21', 'init_n': 'V24', 'tck': 'R25', 'tdi': 'U25', 'tdo': 'T25', 'tms': 'R24', 'mode0': 'T22', 'mode1': 'R22', 'mode2': 'T23', 'mode3': 'R23', 'padi': 'V21', 'pado': 'V22', 'por_n': 'V23', 'prog_n': 'U21', 'clk': 'U24', 'srst_n': 'U23' },
	},
	('xczu6cg',  'ffvc900'):  {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'T18', 'error_out': 'P21', 'error_status': 'P22', 'init_n': 'T23', 'tck': 'R20', 'tdi': 'T21', 'tdo': 'T20', 'tms': 'R19', 'mode0': 'U18', 'mode1': 'U19', 'mode2': 'U20', 'mode3': 'U21', 'padi': 'R22', 'pado': 'R23', 'por_n': 'U23', 'prog_n': 'T22', 'clk': 'P20', 'srst_n': 'P19' },
	},
	('xczu6eg',  'ffvb1156'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'W21', 'error_out': 'T21', 'error_status': 'R21', 'init_n': 'V24', 'tck': 'R25', 'tdi': 'U25', 'tdo': 'T25', 'tms': 'R24', 'mode0': 'T22', 'mode1': 'R22', 'mode2': 'T23', 'mode3': 'R23', 'padi': 'V21', 'pado': 'V22', 'por_n': 'V23', 'prog_n': 'U21', 'clk': 'U24', 'srst_n': 'U23' },
	},
	('xczu6eg',  'ffvc900'):  {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'T18', 'error_out': 'P21', 'error_status': 'P22', 'init_n': 'T23', 'tck': 'R20', 'tdi': 'T21', 'tdo': 'T20', 'tms': 'R19', 'mode0': 'U18', 'mode1': 'U19', 'mode2': 'U20', 'mode3': 'U21', 'padi': 'R22', 'pado': 'R23', 'por_n': 'U23', 'prog_n': 'T22', 'clk': 'P20', 'srst_n': 'P19' },
	},
	('xczu7cg',  'fbvb900'):  {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'N22', 'error_out': 'R22', 'error_status': 'R20', 'init_n': 'N18', 'tck': 'L19', 'tdi': 'L20', 'tdo': 'M20', 'tms': 'L21', 'mode0': 'R18', 'mode1': 'R19', 'mode2': 'P21', 'mode3': 'P22', 'padi': 'M21', 'pado': 'N21', 'por_n': 'N19', 'prog_n': 'M19', 'clk': 'P19', 'srst_n': 'P20' },
	},
	('xczu7cg',  'ffvc1156'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'N24', 'error_out': 'T25', 'error_status': 'R25', 'init_n': 'P24', 'tck': 'K27', 'tdi': 'J27', 'tdo': 'G28', 'tms': 'H28', 'mode0': 'H27', 'mode1': 'J26', 'mode2': 'K26', 'mode3': 'K25', 'padi': 'M25', 'pado': 'L25', 'por_n': 'M24', 'prog_n': 'T24', 'clk': 'R24', 'srst_n': 'P25' },
	},
	('xczu7cg',  'ffvf1517'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'AJ31', 'error_out': 'AH32', 'error_status': 'AH31', 'init_n': 'AK30', 'tck': 'AG31', 'tdi': 'AE30', 'tdo': 'AF31', 'tms': 'AE29', 'mode0': 'AH27', 'mode1': 'AH28', 'mode2': 'AJ27', 'mode3': 'AH29', 'padi': 'AJ30', 'pado': 'AJ29', 'por_n': 'AF30', 'prog_n': 'AG30', 'clk': 'AG28', 'srst_n': 'AG29' },
	},
	('xczu7eg',  'fbvb900'):  {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'N22', 'error_out': 'R22', 'error_status': 'R20', 'init_n': 'N18', 'tck': 'L19', 'tdi': 'L20', 'tdo': 'M20', 'tms': 'L21', 'mode0': 'R18', 'mode1': 'R19', 'mode2': 'P21', 'mode3': 'P22', 'padi': 'M21', 'pado': 'N21', 'por_n': 'N19', 'prog_n': 'M19', 'clk': 'P19', 'srst_n': 'P20' },
	},
	('xczu7eg',  'ffvc1156'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'N24', 'error_out': 'T25', 'error_status': 'R25', 'init_n': 'P24', 'tck': 'K27', 'tdi': 'J27', 'tdo': 'G28', 'tms': 'H28', 'mode0': 'H27', 'mode1': 'J26', 'mode2': 'K26', 'mode3': 'K25', 'padi': 'M25', 'pado': 'L25', 'por_n': 'M24', 'prog_n': 'T24', 'clk': 'R24', 'srst_n': 'P25' },
	},
	('xczu7eg',  'ffvf1517'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'AJ31', 'error_out': 'AH32', 'error_status': 'AH31', 'init_n': 'AK30', 'tck': 'AG31', 'tdi': 'AE30', 'tdo': 'AF31', 'tms': 'AE29', 'mode0': 'AH27', 'mode1': 'AH28', 'mode2': 'AJ27', 'mode3': 'AH29', 'padi': 'AJ30', 'pado': 'AJ29', 'por_n': 'AF30', 'prog_n': 'AG30', 'clk': 'AG28', 'srst_n': 'AG29' },
	},
	('xczu7ev',  'fbvb900'):  {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'N22', 'error_out': 'R22', 'error_status': 'R20', 'init_n': 'N18', 'tck': 'L19', 'tdi': 'L20', 'tdo': 'M20', 'tms': 'L21', 'mode0': 'R18', 'mode1': 'R19', 'mode2': 'P21', 'mode3': 'P22', 'padi': 'M21', 'pado': 'N21', 'por_n': 'N19', 'prog_n': 'M19', 'clk': 'P19', 'srst_n': 'P20' },
	},
	('xczu7ev',  'ffvc1156'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'N24', 'error_out': 'T25', 'error_status': 'R25', 'init_n': 'P24', 'tck': 'K27', 'tdi': 'J27', 'tdo': 'G28', 'tms': 'H28', 'mode0': 'H27', 'mode1': 'J26', 'mode2': 'K26', 'mode3': 'K25', 'padi': 'M25', 'pado': 'L25', 'por_n': 'M24', 'prog_n': 'T24', 'clk': 'R24', 'srst_n': 'P25' },
	},
	('xczu7ev',  'ffvf1517'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'AJ31', 'error_out': 'AH32', 'error_status': 'AH31', 'init_n': 'AK30', 'tck': 'AG31', 'tdi': 'AE30', 'tdo': 'AF31', 'tms': 'AE29', 'mode0': 'AH27', 'mode1': 'AH28', 'mode2': 'AJ27', 'mode3': 'AH29', 'padi': 'AJ30', 'pado': 'AJ29', 'por_n': 'AF30', 'prog_n': 'AG30', 'clk': 'AG28', 'srst_n': 'AG29' },
	},
	('xczu9cg',  'ffvb1156'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'W21', 'error_out': 'T21', 'error_status': 'R21', 'init_n': 'V24', 'tck': 'R25', 'tdi': 'U25', 'tdo': 'T25', 'tms': 'R24', 'mode0': 'T22', 'mode1': 'R22', 'mode2': 'T23', 'mode3': 'R23', 'padi': 'V21', 'pado': 'V22', 'por_n': 'V23', 'prog_n': 'U21', 'clk': 'U24', 'srst_n': 'U23' },
	},
	('xczu9cg',  'ffvc900'):  {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'T18', 'error_out': 'P21', 'error_status': 'P22', 'init_n': 'T23', 'tck': 'R20', 'tdi': 'T21', 'tdo': 'T20', 'tms': 'R19', 'mode0': 'U18', 'mode1': 'U19', 'mode2': 'U20', 'mode3': 'U21', 'padi': 'R22', 'pado': 'R23', 'por_n': 'U23', 'prog_n': 'T22', 'clk': 'P20', 'srst_n': 'P19' },
	},
	('xczu9eg',  'ffvb1156'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'W21', 'error_out': 'T21', 'error_status': 'R21', 'init_n': 'V24', 'tck': 'R25', 'tdi': 'U25', 'tdo': 'T25', 'tms': 'R24', 'mode0': 'T22', 'mode1': 'R22', 'mode2': 'T23', 'mode3': 'R23', 'padi': 'V21', 'pado': 'V22', 'por_n': 'V23', 'prog_n': 'U21', 'clk': 'U24', 'srst_n': 'U23' },
	},
	('xczu9eg',  'ffvc900'):  {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'T18', 'error_out': 'P21', 'error_status': 'P22', 'init_n': 'T23', 'tck': 'R20', 'tdi': 'T21', 'tdo': 'T20', 'tms': 'R19', 'mode0': 'U18', 'mode1': 'U19', 'mode2': 'U20', 'mode3': 'U21', 'padi': 'R22', 'pado': 'R23', 'por_n': 'U23', 'prog_n': 'T22', 'clk': 'P20', 'srst_n': 'P19' },
	},
	('xqzu11eg', 'ffrc1156'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'N24', 'error_out': 'T25', 'error_status': 'R25', 'init_n': 'P24', 'tck': 'K27', 'tdi': 'J27', 'tdo': 'G28', 'tms': 'H28', 'mode0': 'H27', 'mode1': 'J26', 'mode2': 'K26', 'mode3': 'K25', 'padi': 'M25', 'pado': 'L25', 'por_n': 'M24', 'prog_n': 'T24', 'clk': 'R24', 'srst_n': 'P25' },
	},
	('xqzu11eg', 'ffrc1760'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'Y28', 'error_out': 'U27', 'error_status': 'V28', 'init_n': 'V27', 'tck': 'AC26', 'tdi': 'AD25', 'tdo': 'AD27', 'tms': 'AD26', 'mode0': 'AA27', 'mode1': 'AC28', 'mode2': 'AA28', 'mode3': 'AB28', 'padi': 'AE28', 'pado': 'AE27', 'por_n': 'W27', 'prog_n': 'Y27', 'clk': 'AC27', 'srst_n': 'AB27' },
	},
	('xqzu15eg', 'ffrb1156'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'W21', 'error_out': 'T21', 'error_status': 'R21', 'init_n': 'V24', 'tck': 'R25', 'tdi': 'U25', 'tdo': 'T25', 'tms': 'R24', 'mode0': 'T22', 'mode1': 'R22', 'mode2': 'T23', 'mode3': 'R23', 'padi': 'V21', 'pado': 'V22', 'por_n': 'V23', 'prog_n': 'U21', 'clk': 'U24', 'srst_n': 'U23' },
	},
	('xqzu15eg', 'ffrc900'):  {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'T18', 'error_out': 'P21', 'error_status': 'P22', 'init_n': 'T23', 'tck': 'R20', 'tdi': 'T21', 'tdo': 'T20', 'tms': 'R19', 'mode0': 'U18', 'mode1': 'U19', 'mode2': 'U20', 'mode3': 'U21', 'padi': 'R22', 'pado': 'R23', 'por_n': 'U23', 'prog_n': 'T22', 'clk': 'P20', 'srst_n': 'P19' },
	},
	('xqzu19eg', 'ffrb1517'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'AC26', 'error_out': 'Y28', 'error_status': 'AA28', 'init_n': 'AC27', 'tck': 'AD25', 'tdi': 'AC28', 'tdo': 'AA27', 'tms': 'AC25', 'mode0': 'AA25', 'mode1': 'AA26', 'mode2': 'W27', 'mode3': 'W25', 'padi': 'AB25', 'pado': 'AB26', 'por_n': 'AB28', 'prog_n': 'Y27', 'clk': 'Y25', 'srst_n': 'W26' },
	},
	('xqzu19eg', 'ffrc1760'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'Y28', 'error_out': 'U27', 'error_status': 'V28', 'init_n': 'V27', 'tck': 'AC26', 'tdi': 'AD25', 'tdo': 'AD27', 'tms': 'AD26', 'mode0': 'AA27', 'mode1': 'AC28', 'mode2': 'AA28', 'mode3': 'AB28', 'padi': 'AE28', 'pado': 'AE27', 'por_n': 'W27', 'prog_n': 'Y27', 'clk': 'AC27', 'srst_n': 'AB27' },
	},
	('xqzu21dr', 'ffrd1156'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'T26', 'error_out': 'L24', 'error_status': 'L26', 'init_n': 'T24', 'tck': 'N24', 'tdi': 'N25', 'tdo': 'R26', 'tms': 'N26', 'mode0': 'L25', 'mode1': 'M24', 'mode2': 'K24', 'mode3': 'M26', 'padi': 'H24', 'pado': 'J24', 'por_n': 'R25', 'prog_n': 'P25', 'clk': 'P24', 'srst_n': 'T25' },
	},
	('xqzu28dr', 'ffre1156'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'T24', 'error_out': 'J24', 'error_status': 'R26', 'init_n': 'R24', 'tck': 'P26', 'tdi': 'M26', 'tdo': 'T26', 'tms': 'N25', 'mode0': 'L26', 'mode1': 'L24', 'mode2': 'K24', 'mode3': 'M24', 'padi': 'K26', 'pado': 'K25', 'por_n': 'N24', 'prog_n': 'P25', 'clk': 'M25', 'srst_n': 'R25' },
	},
	('xqzu28dr', 'ffrg1517'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'AB27', 'error_out': 'AF30', 'error_status': 'AC32', 'init_n': 'AB26', 'tck': 'AA29', 'tdi': 'AD31', 'tdo': 'AD32', 'tms': 'AD30', 'mode0': 'AC31', 'mode1': 'AB30', 'mode2': 'AB31', 'mode3': 'AE32', 'padi': 'AE31', 'pado': 'AF31', 'por_n': 'AB29', 'prog_n': 'AA27', 'clk': 'AC30', 'srst_n': 'AB28' },
	},
	('xqzu29dr', 'ffrf1760'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'N31', 'error_out': 'AC30', 'error_status': 'AC31', 'init_n': 'P31', 'tck': 'T32', 'tdi': 'U31', 'tdo': 'V31', 'tms': 'W31', 'mode0': 'AA32', 'mode1': 'AB32', 'mode2': 'AB31', 'mode3': 'Y31', 'padi': 'W32', 'pado': 'Y32', 'por_n': 'R32', 'prog_n': 'P32', 'clk': 'U32', 'srst_n': 'R31' },
	},
	('xqzu3eg',  'sfra484'):  {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'L12', 'error_out': 'K16', 'error_status': 'K18', 'init_n': 'K15', 'tck': 'H13', 'tdi': 'H12', 'tdo': 'J13', 'tms': 'J12', 'mode0': 'J16', 'mode1': 'H15', 'mode2': 'J15', 'mode3': 'H18', 'padi': 'H17', 'pado': 'J17', 'por_n': 'K12', 'prog_n': 'K14', 'clk': 'H14', 'srst_n': 'K13' },
	},
	('xqzu3eg',  'sfrc784'):  {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'M21', 'error_out': 'P17', 'error_status': 'M20', 'init_n': 'P21', 'tck': 'R19', 'tdi': 'R18', 'tdo': 'T21', 'tms': 'N21', 'mode0': 'P19', 'mode1': 'P20', 'mode2': 'R20', 'mode3': 'T20', 'padi': 'N17', 'pado': 'N18', 'por_n': 'P16', 'prog_n': 'R17', 'clk': 'R16', 'srst_n': 'N19' },
	},
	('xqzu5ev',  'ffrb900'):  {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'N22', 'error_out': 'R22', 'error_status': 'R20', 'init_n': 'N18', 'tck': 'L19', 'tdi': 'L20', 'tdo': 'M20', 'tms': 'L21', 'mode0': 'R18', 'mode1': 'R19', 'mode2': 'P21', 'mode3': 'P22', 'padi': 'M21', 'pado': 'N21', 'por_n': 'N19', 'prog_n': 'M19', 'clk': 'P19', 'srst_n': 'P20' },
	},
	('xqzu5ev',  'sfrc784'):  {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'M21', 'error_out': 'P17', 'error_status': 'M20', 'init_n': 'P21', 'tck': 'R19', 'tdi': 'R18', 'tdo': 'T21', 'tms': 'N21', 'mode0': 'P19', 'mode1': 'P20', 'mode2': 'R20', 'mode3': 'T20', 'padi': 'N17', 'pado': 'N18', 'por_n': 'P16', 'prog_n': 'R17', 'clk': 'R16', 'srst_n': 'N19' },
	},
	('xqzu7ev',  'ffrb900'):  {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'N22', 'error_out': 'R22', 'error_status': 'R20', 'init_n': 'N18', 'tck': 'L19', 'tdi': 'L20', 'tdo': 'M20', 'tms': 'L21', 'mode0': 'R18', 'mode1': 'R19', 'mode2': 'P21', 'mode3': 'P22', 'padi': 'M21', 'pado': 'N21', 'por_n': 'N19', 'prog_n': 'M19', 'clk': 'P19', 'srst_n': 'P20' },
	},
	('xqzu7ev',  'ffrc1156'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'N24', 'error_out': 'T25', 'error_status': 'R25', 'init_n': 'P24', 'tck': 'K27', 'tdi': 'J27', 'tdo': 'G28', 'tms': 'H28', 'mode0': 'H27', 'mode1': 'J26', 'mode2': 'K26', 'mode3': 'K25', 'padi': 'M25', 'pado': 'L25', 'por_n': 'M24', 'prog_n': 'T24', 'clk': 'R24', 'srst_n': 'P25' },
	},
	('xqzu9eg',  'ffrb1156'): {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'W21', 'error_out': 'T21', 'error_status': 'R21', 'init_n': 'V24', 'tck': 'R25', 'tdi': 'U25', 'tdo': 'T25', 'tms': 'R24', 'mode0': 'T22', 'mode1': 'R22', 'mode2': 'T23', 'mode3': 'R23', 'padi': 'V21', 'pado': 'V22', 'por_n': 'V23', 'prog_n': 'U21', 'clk': 'U24', 'srst_n': 'U23' },
	},
	('xqzu9eg',  'ffrc900'):  {
		'mio': [

		],
		'ddr': { },
		'core': { 'done': 'T18', 'error_out': 'P21', 'error_status': 'P22', 'init_n': 'T23', 'tck': 'R20', 'tdi': 'T21', 'tdo': 'T20', 'tms': 'R19', 'mode0': 'U18', 'mode1': 'U19', 'mode2': 'U20', 'mode3': 'U21', 'padi': 'R22', 'pado': 'R23', 'por_n': 'U23', 'prog_n': 'T22', 'clk': 'P20', 'srst_n': 'P19' },
	},
}


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

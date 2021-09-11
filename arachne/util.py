# SPDX-License-Identifier: BSD-3-Clause
import sys

from os import environ

__all__ = (
	'log',
	'err',
	'wrn',
	'inf',
	'dbg',
)

def log(str, end = '\n', file = sys.stdout):
	print(f'\x1B[35m[*]\x1B[0m {str}', end = end, file = file)

def err(str, end = '\n', file = sys.stderr):
	print(f'\x1B[31m[!]\x1B[0m {str}', end = end, file = file)

def wrn(str, end = '\n', file = sys.stderr):
	print(f'\x1B[33m[~]\x1B[0m {str}', end = end, file = file)

def inf(str, end = '\n', file = sys.stdout):
	print(f'\x1B[36m[~]\x1B[0m {str}', end = end, file = file)

def dbg(str, end = '\n', file = sys.stdout):
	if 'ARACHNE_DEBUG' in environ:
		print(f'\x1B[34m[~]\x1B[0m {str}', end = end, file = file)

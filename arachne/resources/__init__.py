# SPDX-License-Identifier: BSD-3-Clause
from typing import Tuple

def assert_width(names : str, assert_widths : Tuple[int]):
	if not isinstance(names, str):
		raise TypeError(f'Names must be a whitespace-separated string, not {names!r}')
	names = names.split()
	for assert_width in assert_widths:
		if len(names) == assert_width:
			return

	raise AssertionError(f"{len(names)} names are specified ({' '.join(names)}), " +
		f"but one of {assert_widths} names are expected")

# SPDX-License-Identifier: BSD-3-Clause
from unittest                         import TestCase

from arachne.hdl.xilinx.ps8.resources import *

class PS8ResourcesTestCase(TestCase):
	def test_resource(self):
		with self.assertRaises(TypeError):
			r = PS8Resource(0, 0)

		class TestResource0(PS8Resource):
			name          = 'test'
			claimable_mio = []

			def __init__(self, num):
				super().__init__(num, 1)

			def used_mio(self, **kwargs):
				raise NotImplementedError

			def generate_mapping(self, **kwargs):
				raise NotImplementedError

		tr = TestResource0(0)

		with self.assertRaisesRegex(ValueError,
				(r'^PS8 Only has test0\.\.1, not 2$')
			):

			_ = TestResource0(2)

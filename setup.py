# SPDX-License-Identifier: BSD-3-Clause
from setuptools import setup, find_packages

setup(
	name = 'arachne',
	# TODO
	# use_scm_version =
	author          = 'Aki \'lethalbit\' Van Ness',
	author_email    = 'nya@catgirl.link',
	description     = 'Toolkit for nMigen',
	license         = 'BSD-3-Clause',
	python_requires = '~=3.8',
	setup_requires  = [
		'wheel', 'setuptools', 'setuptools_scm'
	],
	install_requires = [
		'nmigen>=0.2',
	],
	packages = find_packages(
		exclude = [
			'tests*'
		]
	),

	project_urls = {
		'Documentation': 'https://github.com/shrine-maiden-heavy-industries/arachne',
		'Source Code'  : 'https://github.com/shrine-maiden-heavy-industries/arachne',
		'Bug Tracker'  : 'https://github.com/shrine-maiden-heavy-industries/arachne/issues',

	}
)

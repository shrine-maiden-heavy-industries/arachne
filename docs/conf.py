# SPDX-License-Identifier: BSD-3-Clause
import os, sys
sys.path.insert(0, os.path.abspath('.'))



import arachne

project = 'Arachne'
version = arachne.__version__
release = version.split('+')[0]
copyright = '2021, Arachne developers'

extensions = [
	'sphinx.ext.intersphinx',
	'sphinx.ext.doctest',
    'sphinx.ext.todo',
	'sphinx.ext.githubpages',
	'sphinx.ext.graphviz',
	'sphinx.ext.autosectionlabel',
	'sphinxcontrib.mermaid',
	'sphinxcontrib.platformpicker'
	'sphinx_rtd_theme',,
	'myst_parser',
]

source_suffix = {
	'.md': 'markdown',
}

graphviz_output_format = 'svg'


import sphinx_rtd_theme

html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'collapse_navigation' : False
}

html_static_path = [
	'_static'
]
html_css_files = [
	'custom.css'
]

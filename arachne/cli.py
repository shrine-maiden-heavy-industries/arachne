# SPDX-License-Identifier: BSD-3-Clause

__all__ = (
	'register_cli',
)

def _register_core_cli(parser):
	# Logging options and the like
	display = parser.add_argument_group('Arachne Display Settings')
	verbosity = display.add_mutually_exclusive_group()
	verbosity_opts.add_argument(
		'--verbose',
		dest   = 'arachne_display_verbose',
		action = 'store_true',
		help   = 'Enable verbose debug logging'
	)

	verbosity_opts.add_argument(
		'--debug',
		dest   = 'arachne_display_debug',
		action = 'store_true',
		help   = 'Enable debug logging. THIS IS NOISY'
	)

	verbosity_opts.add_argument(
		'--quiet',
		dest   = 'arachne_display_quiet',
		action = 'store_true',
		help   = 'Disable all output except for warnings and errors'
	)

	display.add_argument(
		'--disable-color',
		dest   = 'arachne_display_color',
		action = 'store_true',
		help   = 'Disable Arachne colorized output'
	)

def _register_simulation_cli(parser):
	pass

def _register_verification_cli(parser):
	pass

def register_cli(*, parser = None):
	from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

	# If there is no parser passed in, then make one
	if parser is None:
		parser = ArgumentParser(
			formatter_class = ArgumentDefaultsHelpFormatter,
			description = 'Arachne toolkit'
		)

	# Check to see if there are any sub-parsers, if not, create it
	if parser._subparsers is None:
		parser.add_subparsers(dest = 'action')

	# Extract the `action` sub-parser
	_subparsers = list(filter(lambda sp: sp.dest == 'action', parser._subparsers._group_actions))
	if len(_subparsers) == 0:
		raise RuntimeError('How did this even happen?')

	actions = _subparsers[0]

	# Register Core Options
	_register_core_cli(parser.add_argument_group('Arachne'))

	# Register action options
	_register_simulation_cli(actions.add_parser('arachne-sim', help = 'Arachne Simulation'))
	_register_verification_cli(actions.add_parser('arachne-formal', help = 'Arachne Formal Verification'))


	return parser

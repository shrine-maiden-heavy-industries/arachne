# SPDX-License-Identifier: BSD-3-Clause

from ..util import *

__all__ = (
	'sim_case',
	'run_sims',
)

def _collect_sims(*, pkg):
	import pkgutil
	from inspect import getmembers
	from os      import path

	sims = []

	if not path.exists(pkg):
		raise RuntimeError(f'The package {pkg} does not exist, unable to attempt to import test cases')

	for _, name, is_pkg in pkgutil.itr_modules(path = pkg):
		if not is_pkg:
			pkg_import = __import__(f'{pkg}.{name}')
			# TODO: Figure out the import stuff
			# sims.append({
			# 	'name' : name,
			# 	'cases': getmembers(pkg, lambda o: isinstance(o, ))
			# })

	return sims


def sim_case(*, domains, dut, platform = None, engine = 'pysim'):
	def _reg_sim(func):
		from nmigen.sim    import Simulator
		from nmigen.hdl.ir import Fragment

		sim = Simulator(
			Fragment.get(dut, platform = platform),
			engine = engine
		)

		for dom, clk in domains:
			sim.add_clock(1 / clk, domain = dom)

		for case, dom in func(sim, dut):
			sim.add_sync_process(case, domain = dom)

		return (sim, getattr(func, '__name__'))
	return _reg_sim

def run_sims(*, pkg, result_dir, skip = []):
	from os import path, mkdir

	if not path.exists(result_dir):
		mkdir(result_dir)

	for sim in _collect_sims(pkg = pkg):
		log(f'Running simulation {sim["name"]}...')

		out_dir = path.join(result_dir, sim['name'])
		if not path.exists(out_dir):
			mkdir(out_dir)

		for case, name in sim['cases']:
			inf(f' => Running {name}')

			with case.write_vcd(path.join(out_dir, f'{name}.vcd')):
				case.reset()
				case.run()


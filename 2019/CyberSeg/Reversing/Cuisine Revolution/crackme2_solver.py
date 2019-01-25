import angr
import claripy

def is_alnum(state, c):
	is_num = state.solver.And(c >= ord("0"), c <= ord("9"))
	is_alpha_lower = state.solver.And(c >= ord("a"), c <= ord("z"))
	is_alpha_upper = state.solver.And(c >= ord("A"), c <= ord("Z"))
	isalphanum = state.solver.Or(is_num, is_alpha_lower, is_alpha_upper)
	return isalphanum

proj = angr.Project("./crackme2", main_opts={'base_addr': 0})
input_size = 9;

flag_chars = [claripy.BVS('flag_%d' % i, 8) for i in range(input_size)]
flag = claripy.Concat(*flag_chars + [claripy.BVV(b'\n')])

initial_state = proj.factory.entry_state(args=["./crackme2"], stdin=flag)
for i in range(input_size):
	initial_state.add_constraints(flag.get_byte(i) >= 32)
	initial_state.add_constraints(flag.get_byte(i) <= 127)

sm = proj.factory.simulation_manager(initial_state)
sm.explore(find=0x12AE, avoid=0x12D0)

if sm.found:
	for p in sm.found:
		found = p
		iter_sol = found.solver.eval_upto(flag, 500, cast_to=bytes) 
		
		for sol in iter_sol:

			if sol == None:
				break

			if "Slapchop" in sol.decode("utf-8"):
				print("Solution: {}".format(sol))
import angr
import claripy

def is_alnum(state, c):
	# set some constraints on the char, let it
	# be a null char or alphanumeric
	is_num = state.solver.And(c >= ord("0"), c <= ord("9"))
	is_alpha_lower = state.solver.And(c >= ord("a"), c <= ord("z"))
	is_alpha_upper = state.solver.And(c >= ord("A"), c <= ord("Z"))
	isalphanum = state.solver.Or(is_num, is_alpha_lower, is_alpha_upper)
	return isalphanum

proj = angr.Project("./crackme2", main_opts={'custom_base_addr': 0})

input_size = 10; # Max length from strncpy, see 0x4005ae.

flag_chars = [claripy.BVS('flag_%d' % i, 8) for i in range(input_size)]
flag = claripy.Concat(*flag_chars + [claripy.BVV(b'\n')])

initial_state = proj.factory.entry_state(args=["./crackme2"], stdin=flag)
#initial_state.libc.buf_symbolic_bytes=input_size + 1 # Thanks to Christopher Salls (@salls) for pointing this out. By default there's only 60 symbolic bytes, which is too small.

# For some reason if you constrain too few bytes, the solution isn't found. To be safe, I'm constraining them all.
for i in range(input_size):
	initial_state.add_constraints(flag.get_byte(i) >= 32)
	initial_state.add_constraints(flag.get_byte(i) <= 127)

sm = proj.factory.simulation_manager(initial_state)
sm.explore(find=0x12AE, avoid=0x12D0)

'''
found = sm.found[0]

solution = found.solver.eval_upto(flag, cast_to=bytes)
#solution = solution[:solution.find(b"/n")+1] # Trim off the null bytes at the end of the flag (if any).
print(solution)
'''
if sm.found:
	for p in sm.found:
		found = p
		#found.stack_pop() # ignore, our args start at offset 0x8

		iter_sol = found.solver.eval_upto(flag, 500, cast_to=bytes) # ask for up to 10 solutions if possible
		for sol in iter_sol:

			if sol == None:
				break

			if b"Slapchop" or b"SlapchoP" in sol:
				print("Solution: {}".format(sol))
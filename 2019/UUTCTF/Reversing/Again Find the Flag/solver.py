import angr
import claripy

proj = angr.Project("./chal_re_med.so", main_opts={'base_addr': 0})

input_size = 19
argv1 = claripy.BVS("argv1", input_size * 8)
initial_state = proj.factory.entry_state(args=["./chal_re_med.so", argv1])

for i in range(input_size):
	initial_state.add_constraints(argv1.get_byte(i) >= ord(' '))
	initial_state.add_constraints(argv1.get_byte(i) <= ord('~'))

find_address = 0xAE1
avoid_address = (0x9FC, 0xA06, 0xA10, 0xA1A, 0xA24, 0xA2E, 0xA38, 0xA42, 0xA4C, 0xA56, 0xA60, 0xA6A, 0xA74, 0xA7E)
	
sm = proj.factory.simulation_manager(initial_state)
sm.explore(find=find_address, avoid=avoid_address)

if sm.found:
	for p in sm.found:
		found = p
		sol = found.solver.eval(argv1, cast_to=bytes)
		print(b"Solution: " + sol)
		print(found.posix.dumps(1))
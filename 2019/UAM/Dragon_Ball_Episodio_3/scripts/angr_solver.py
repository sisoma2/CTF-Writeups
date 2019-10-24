import angr
import claripy

proj = angr.Project("./main")

input_size = 12

argv1 = claripy.BVS("argv1", input_size * 8)
initial_state = proj.factory.entry_state(args=["./main"], stdin=argv1, add_options=angr.options.unicorn)

for i in range(input_size - 1):
	initial_state.add_constraints(argv1.get_byte(i) >= ord(' '))
	initial_state.add_constraints(argv1.get_byte(i) <= ord('}'))

initial_state.add_constraints(argv1.get_byte(input_size - 1) == 0x10)

find_address = 0x400D32
avoid_address = (0x400D58, 0x400D08)
	
sm = proj.factory.simulation_manager(initial_state)
sm.explore(find=find_address, avoid=avoid_address)

if sm.found:
	found = sm.found[0] 
	solution = found.solver.eval(argv1, cast_to=bytes)
	print(f"Flag is: {str(solution)}")

else:
	print("Failed! No flag for u")
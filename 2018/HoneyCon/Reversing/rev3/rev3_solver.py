from z3 import *

xs = [BitVec('x{}'.format(i), 8) for i in xrange(9)]
s = Solver()

for x in xs:
	s.add((x & ~0xff) == 0)
	
s.add(xs[0] ^ ord('h') == 11)
s.add(xs[1] ^ ord('o') == 0)
s.add(xs[2] ^ ord('o') == 0)
s.add(xs[3] ^ ord('e') == 9)
s.add(xs[4] ^ ord('y') == 3)
s.add(xs[5] ^ ord('_') == 0)
s.add(xs[6] ^ ord('c') == 27)
s.add(xs[7] ^ ord('o') == 0)
s.add(xs[8] ^ ord('o') == 29)

if s.check() == sat:
	m = s.model()
	flag = ""
	for x in xs:
		flag += chr(m[x].as_long())
	print flag
else:
	print("Unsat")
	
#honeyCON18{coolz_xor}
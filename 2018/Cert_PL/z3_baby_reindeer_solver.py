from z3 import *

xs = [BitVec('x{}'.format(i), 8) for i in xrange(25)]
s = Solver()

for x in xs:
	s.add((x & ~0xff) == 0)
	
s.add(xs[0] == 101)
s.add(xs[14] ^ xs[0] == 14)
s.add(xs[23] ^ xs[18] == 64)
s.add(xs[16] ^ xs[12] == 93)
s.add(xs[2] ^ xs[18] == 18)
s.add(xs[21] ^ xs[20] == 19)
s.add(xs[3] ^ xs[2] == 16)
s.add(xs[4] ^ xs[24] == 6)
s.add(xs[19] ^ xs[14] == 52)
s.add(xs[12] ^ xs[20] == 85)
s.add(xs[7] ^ xs[21] == 7)
s.add(xs[6] ^ xs[15] == 1)
s.add(xs[17] ^ xs[10] == 80)
s.add(xs[9] ^ xs[0] == 58)
s.add(xs[1] ^ xs[16] == 13)
s.add(xs[8] ^ xs[20] == 66)
s.add(xs[15] ^ xs[8] == 21)
s.add(xs[11] ^ xs[22] == 28)
s.add(xs[20] ^ xs[0] == 3)
s.add(xs[5] ^ xs[9] == 39)
s.add(xs[18] ^ xs[20] == 7)
s.add(xs[13] ^ xs[18] == 62)
s.add(xs[10] ^ xs[20] == 82)
s.add(xs[24] ^ xs[0] == 24)
s.add(xs[22] ^ xs[24] == 19)

if s.check() == sat:
	m = s.model()
	flag = ""
	for x in xs:
		flag += chr(m[x].as_long())
	print flag
else:
	print("Unsat")
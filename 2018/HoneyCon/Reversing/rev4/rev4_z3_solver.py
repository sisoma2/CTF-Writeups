from z3 import *

length = 7
xs = [BitVec('x{}'.format(i), 8) for i in xrange(length)]
s = Solver()

def ascii_printable(x):
    return And(0x32 <= (x & 0xff), (x & 0xff) <= 122)
	
for i in range(5,length):
	s.add(ascii_printable(xs[i]))

# Constrain 5 first chars to I_X0r
s.add(xs[0] == ord('I'))
s.add(xs[1] == ord('_'))
s.add(xs[2] == ord('X'))
s.add(xs[3] == ord('0'))
s.add(xs[4] == ord('r'))

s.add(xs[0] + xs[1] + xs[2] + xs[3] + xs[4] + xs[5] + xs[6] == 0x239)
s.add((xs[0] ^ 0xD) + (xs[1] ^ 0x3C) + (xs[2] ^ 0xF) + (xs[3] ^ 0x48) + (xs[4] ^ 0x1E) + (xs[5] ^ 0x57) + (xs[6] ^ 0x30) == 0x29A)


if s.check() == sat:
	m = s.model()
	flag = ""
	for x in xs:
		flag += chr(m[x].as_long())
	print flag
else:
	print("Unsat")
	
#Keygen: I_X0r3d
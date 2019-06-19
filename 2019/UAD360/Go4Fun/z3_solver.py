from z3 import *

def ascii_numbers(x):
    return And(x  > ord('/'), x  < ord(':') )

def nor (a,b):
    return ~(a|b)
	
LENGTH = 20

b = [BitVec('%d' % i, 8) for i in range(LENGTH)]
s = Solver()

for i in range(LENGTH):
	s.add(ascii_numbers(b[i]))

offset15Val = b[15] - 0x30 
s.add(offset15Val <= 9)

offset4Val = b[4] - 0x30
s.add(offset4Val <= 9)

s.add((offset15Val + offset4Val) ^ 0xC == 0)

offset1Val = b[1] - 0x30
s.add(offset1Val <= 9)

offset18Val = b[18] - 0x30
s.add(offset18Val <= 9)

s.add((offset1Val * offset18Val) ^ 0xF == 0)

offset9Val = b[9] - 0x30
s.add(offset9Val <= 9)

s.add((offset15Val / offset9Val) ^ 0x1 == 0)

offset17Val = b[17] - 0x30
s.add(offset17Val <= 9)

offset0Val = b[0] - 0x30
s.add(offset0Val <= 9)

s.add((offset17Val - offset0Val) ^ 0x8 == 0)

offset5Val = b[5] - 0x30
s.add(offset5Val <= 9)

s.add(nor((offset5Val - offset17Val), 0) == 0)

s.add((offset15Val - offset1Val) ^ 0x6 == 0)

offset10Val = b[10] - 0x30
s.add(offset10Val <= 9)

s.add((offset10Val * offset1Val) ^ 0x18 == 0)

offset8Val = b[8] - 0x30
s.add(offset8Val <= 9)

offset13Val = b[13] - 0x30
s.add(offset13Val <= 9)

s.add((offset8Val + offset13Val) ^ 0xB == 0)

s.add((offset18Val * offset8Val) ^ 0xF == 0)

offset11Val = b[11] - 0x30
s.add(offset11Val <= 9)

s.add((offset11Val * offset4Val) ^ 0x12 == 0)

s.add((offset9Val + offset8Val) ^ 0xC == 0)

offset12Val = b[12] - 0x30
s.add(offset12Val <= 9)

offset19Val = b[19] - 0x30
s.add(offset19Val <= 9)

s.add((offset12Val - offset19Val) ^ 0xFFFFFFFC == 0)

s.add((offset9Val % offset17Val) ^ 0x1 == 0)

offset14Val = b[14] - 0x30
s.add(offset14Val <= 9)

offset16Val = b[16] - 0x30
s.add(offset16Val <= 9)

s.add((offset14Val * offset16Val) ^ 0x2 == 0)

offset7Val = b[7] - 0x30
s.add(offset7Val <= 9)

s.add((offset7Val - offset4Val) ^ 0x1 == 0)

offset6Val = b[6] - 0x30
s.add(offset7Val <= 9)

s.add(offset6Val + offset0Val == 0)

offset2Val = b[2] - 0x30
s.add(offset2Val <= 9)

s.add(nor((offset2Val - offset16Val), 0) == 0)

s.add((offset0Val % offset5Val) == 0)

s.add((offset11Val * offset5Val) ^ 0x2A == 0)

s.add((offset10Val % offset15Val) ^ 0x8 == 0)

offset3Val = b[3] - 0x30
s.add(offset3Val <= 9)

s.add((offset11Val / offset3Val) ^ 0x2 == 0)

s.add((offset14Val - offset13Val) ^ 0xFFFFFFF9 == 0)

s.add((offset19Val + offset18Val) ^ 0xC == 0)

if s.check() == sat:
	flag = ""
	ans = s.model()
	for i in b:
		print("[*] Char {} = {}".format(i, chr(ans[i].as_long())))
		flag += chr(ans[i].as_long())
	print("[*] Flag is: {}".format(flag))
else:
	print("Unsat!")
	
import string
chrs = string.printable.replace(' \t\n\r\x0b\x0c', '')
joins = ' '.join(chrs).split()
out = []
flag = ""
verificaPassword = [98, 130, 162, 195, 64, 7, 134, 166, 73, 104, 0, 161, 193, 226, 162, 132, 226, 130, 131, 73, 162, 192]

for char in chrs:
	out.append( (((ord(char) << 5) | (ord(char) >> 3)) ^ 111) & 255 )

for item in verificaPassword:
	if item in out:
		index = out.index(item)
		flag += joins[index]
	else:
		pass

print flag
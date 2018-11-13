import string, time
from itertools import chain, product

def bruteforce(charset, maxlength):
    return (''.join(candidate)
        for candidate in chain.from_iterable(product(charset, repeat=i)
        for i in range(maxlength, maxlength + 1)))

start_time = time.clock()
length = 3
check1 = 0
check2 = 0
xor_list = [ 0xD, 0x3C, 0xF, 0x48, 0x1E, 0x57, 0x30 ]	
leak = [ ord('D'), ord('c'), ord('w'), ord('x') ]
serial = ''

for char, xor in zip(leak, xor_list):
	serial += chr(char ^ xor)

for length in range(length, length+1):
	for attempt in bruteforce(string.ascii_letters+string.digits, length):
		check1 = 0
		check2 = 0
		
		attempt = serial + attempt
		for char, xor_value in zip(attempt, xor_list):
			check1 += ord(char)
			check2 += ord(char) ^ xor_value
		
		if (check1 == 0x239 and check2 == 0x29A):
			print "[+] PASS FOUND: " + attempt

print "[+] Script Done! Last attempt: " + attempt
print time.clock() - start_time, "seconds"
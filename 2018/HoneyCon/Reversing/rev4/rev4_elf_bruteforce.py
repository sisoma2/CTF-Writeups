import string, time
from subprocess import Popen, PIPE
import subprocess
from itertools import chain, product

def bruteforce(charset, maxlength):
    return (''.join(candidate)
        for candidate in chain.from_iterable(product(charset, repeat=i)
        for i in range(maxlength, maxlength + 1)))
	
flag = "I_X0r"
length = 2

for length in range(length, length+1):
	for attempt in bruteforce(string.digits+string.ascii_letters, length):
		test_flag = flag + attempt
		
		p = subprocess.Popen(['./rev4', test_flag], stdout=subprocess.PIPE)
		out = p.stdout.readlines()
		
		if "Enhorabuena" in out[2]:
			print "[+] PASS FOUND: " + test_flag
			break
			
print "[+] Script Done! Last attempt: " + test_flag
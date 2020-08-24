import struct
import string
import itertools

'''
Charsets
string.ascii_letters + '_!?{}' + string.digits
string.ascii_letters + '_'
'''

def pw_guess(charset):
    charset = string.ascii_letters + '_!?{}' + string.digits
    res = itertools.product(charset, repeat = 4)
    for guess in res:
        yield ''.join(guess)

def fibo_hash(a, b):
    if a == 0:
        result = [0] * 2
        result[0] = 0
        result[1] = 1
        return result
        
    else:
        temp = fibo_hash(b % a, a)
        
        final_result = [0] * 2
        v3 = temp[1]
        v5 = b // a
        v8 = temp[0]
        v5 = v5 * v8
        v3 = v3 - v5
        
        final_result[0] = v3 & 0xFFFFFFFF
        final_result[1] = temp[0] & 0xFFFFFFFF
        
        return final_result

flag_hash = [
            0x271986b, # We know it's 'CTF{'
            0xa64239c9,
            0x271ded4b,
            0x1186143,
            0xc0fa229f,
            0x690e10bf,
            0x28dca257,
            0x16c699d1,
            0x55a56ffd,
            0x7eb870a1,
            0xc5c9799f,
            0x2f838e65
            ]

default_charset = string.ascii_letters + '_!?{}' + string.digits     
flag = ''
for hash_to_crack in flag_hash:
    print('[+] Trying to crack 0x{:02x}'.format(hash_to_crack))
    if hash_to_crack == 0x55a56ffd:
        guess_generator = pw_guess(string.ascii_letters + '_')
    else:
        guess_generator = pw_guess(default_charset)
        
    for guess in guess_generator:
        if hash_to_crack == 0x271986b:
            guess = 'CTF{'
            
        char_value = struct.unpack("<I", guess.encode('utf-8'))[0]
        hash_result = fibo_hash(char_value, 0x100000000)
        
        result_set = frozenset(hash_result)
        if hash_to_crack in result_set:
            print('Hash 0x{:02x} cracked to: {}'.format(hash_to_crack, guess))
            flag += guess
            break

print('[+] Flag is: ', flag)
    

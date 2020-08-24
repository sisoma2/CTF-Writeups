import struct
import sys

INSTRUCTION_SIZE = 16
shuffle = bytearray([0x02, 0x06, 0x07, 0x01, 0x05, 0x0b, 0x09, 0x0e, 0x03, 0x0f, 0x04, 0x08, 0x0a, 0x0c, 0x0d, 0x00])
add_values = bytearray([0xef, 0xbe, 0xad, 0xde, 0xad, 0xde, 0xe1, 0xfe, 0x37, 0x13, 0x37, 0x13, 0x66, 0x74, 0x63, 0x67])
xor_values = bytearray([0x76, 0x58, 0xb4, 0x49, 0x8d, 0x1a, 0x5f, 0x38, 0xd4, 0x23, 0xf8, 0x34, 0xeb, 0x86, 0xf9, 0xaa])

if len(sys.argv) != 2:
    print('[-] Missing flag argument')
    sys.exit(0)
    
# Flag = CTF{S1MDf0rM3!}
user_input = bytearray(sys.argv[1], 'utf-8')

# Add null byte to input
user_input.append(0x00)
result = bytearray([0] * INSTRUCTION_SIZE)

print('User Input: {}'.format(user_input.decode('ascii')))
print('User input bytes:')
print(' '.join('{:02x}'.format(x) for x in user_input))

# pshufb xmm0, cs:SHUFFLE instruction emulation
for i, num in enumerate(shuffle):
    if num == 0xFF:
        result[i] = 0
    else:
        result[i] = user_input[num % INSTRUCTION_SIZE]

# paddd   xmm0, cs:ADD32 instruction emulation
for i in range(0, INSTRUCTION_SIZE, 4):
    dword_result = struct.unpack('<I', result[i:i+4])[0]
    dword_values = struct.unpack('<I', add_values[i:i+4])[0]
    add_result = (dword_result + dword_values) & 0xFFFFFFFF
    result[i:i+4] = struct.pack('<I', add_result)

# pxor    xmm0, cs:XOR instruction emulation
for i in range(INSTRUCTION_SIZE):
    result[i] = result[i] ^ xor_values[i]

print('Output bytes')
print(' '.join('{:02x}'.format(x) for x in result))

try:
    print('Final Result: {}'.format(result.decode('utf-8')))
except:
    pass
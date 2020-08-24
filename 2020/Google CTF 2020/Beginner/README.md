# Google CTF 2020 - Beginner

> Reversing
>
> easy
>
> Dust off the cobwebs, let's reverse!

## Solution

First, we analyze the filetype and we see it's and ELF x64 executable:

```console
❯ file a.out
a.out: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/
ld-linux-x86-64.so.2, BuildID[sha1]=e3a5d8dc3eee0e960c602b9b2207150c91dc9dff, for GNU/Linux 3.2.0, not stripped
```

We run the file in order to see the program logic:

```console
❯ ./a.out
Flag: CTF{flag}
FAILURE
```

Next, we open the binary in our favorite disassembler/decompiler tool in order to analyze the code of the program. In this case I used IDA and I got the following decompiled code:

```c
int __cdecl main(int argc, const char **argv, const char **envp)
{
  int v3; // er12
  __m128i UserInput; // [rsp+0h] [rbp-38h]
  __m128i s2[2]; // [rsp+10h] [rbp-28h]

  printf("Flag: ", argv, envp);
  __isoc99_scanf("%15s", &UserInput);
  s2[0] = _mm_xor_si128(
            _mm_add_epi32(_mm_shuffle_epi8(_mm_load_si128(&UserInput), (__m128i)SHUFFLE), (__m128i)ADD32),
            (__m128i)XOR);
  if ( !strncmp(UserInput.m128i_i8, (const char *)s2, 16uLL)
    && (v3 = strncmp((const char *)s2, EXPECTED_PREFIX, 4uLL)) == 0 )
  {
    puts("SUCCESS");
  }
  else
  {
    v3 = 1;
    puts("FAILURE");
  }
  return v3;
}
```

It looks pretty simple at first sight so let's try to understand what the code does.

First, the flag is read from STDIN using `scanf` function and length is 15 chars plus the null byte (\x00):

```c
printf("Flag: ", argv, envp);
  __isoc99_scanf("%15s", &UserInput);
```

Then, we can see in the decompiled code that makes some alteration to the flag with XMM instructions like `_mm_shuffle_epi8`, `_mm_add_epi32` and 

`_mm_xor_si128`, if we change to the disassembly view we see the following:

```assembly
.text:000055FF289DE0AE 66 0F 6F 04 24                      movdqa  xmm0, [rsp+38h+UserInput]
.text:000055FF289DE0BE 66 0F 38 00 05 A9 2F 00 00          pshufb  xmm0, cs:SHUFFLE
.text:000055FF289DE0C7 66 0F FE 05 91 2F 00 00             paddd   xmm0, cs:ADD32
.text:000055FF289DE0CF 66 0F EF 05 79 2F 00 00             pxor    xmm0, cs:XOR
.text:000055FF289DE0D7 0F 29 44 24 10                      movaps  xmmword ptr [rsp+38h+s2], xmm0
```

The `movdqa` instruction loads from a stack pointer the contents to the XMM0 register. In this case, the content is the flag the user entered.

The `pshufb` instruction performs in-place shuffles of bytes in the destination operand (the first operand) according to the shuffle control mask in the source operand (the second operand). The shuffle mask `SHUFFLE` has the following content:

```sh
02 06 07 01 05 0b 09 0e 03 0f 04 08 0a 0c 0d 00
```

The `paddd` instructions add packed doubleword integers from the first source operand and second source operand and store the packed integer results in the destination operand. The content of `ADD32` is the following:

```sh
ef be ad de ad de e1 fe 37 13 37 13 66 74 63 67
```

The `pxor` instruction performs a bitwise XOR operation on the source operand (second operand) and the destination operand (first operand) and stores the result in the destination operand. The content of the `XOR` key is:

```sh
76 58 b4 49 8d 1a 5f 38 d4 23 f8 34 eb 86 f9 aa
```

And last, the `movaps`moves the bytes from the`XMM0`resgister, which has the results of the computation, and store it in the `s2` stack variable.

The `s2` variable with the result of the operations is compared with the original input from the user. If they are equal, and both start with the prefix 'CTF{' the flag is correct:

```c
if ( !strncmp(UserInput.m128i_i8, (const char *)s2, 16uLL)
    && (v3 = strncmp((const char *)s2, EXPECTED_PREFIX, 4uLL)) == 0 )
  {
    puts("SUCCESS");
  }
```

I used the following Python code in order to emulate the execution of the program and understand how the XMM instructions modify the flag string:

```python
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
```

We know the flag has the `CTF{}` format and the input and the output string have to be the same but the bytes are shuffled. If we execute the aforementioned script with the input `CTF{0000000000}` the output is:

```console
User Input: CTF{0000000000}
User input bytes:
43 54 46 7b 30 30 30 30 30 30 30 30 30 30 7d 00
Output bytes
43 b7 69 7b 50 14 4d 44 66 30 9f 77 7d 22 6a 00
```

We know that the fourth byte input[3] has to be '{' which is 0x7B in hexadecimal. The output[3] has to be the same as input[3] which is 0x7B -> '{'. Using the shuffle mask we know that the char at input[8] is exchanged and modifies the char at output[3].  With that info we can calculate the output[8] as the following:

```
((0x7B + ADD32[8]) & 0xFF) ^ XOR[8] = ((0x7B + 0x37) & 0xFF) ^ 0xD4 = 0x66 = 'f'
```


We execute it and we get the following output:

```console
User Input: CTF{0000f00000}
User input bytes:
43 54 46 7b 30 30 30 30 66 30 30 30 30 30 7d 00
Output bytes
43 b7 69 7b 50 14 4d 44 66 30 9f 4d 7d 22 6a 00
```

As a result we can see that now the input[8] byte (0x66) is the same as output[8] (0x66) so the char is correct.

In order to solve the challenge, I used the script and manually calculated and changed the bytes in the script till I got the same input and output bytes which is:

```console
User Input: CTF{S1MDf0rM3!}
User input bytes:
43 54 46 7b 53 31 4d 44 66 30 72 4d 33 21 7d 00
Output bytes
43 54 46 7b 53 31 4d 44 66 30 72 4d 33 21 7d 00
Final Result: CTF{S1MDf0rM3!}
```

This is the correct flag for the challenge.

```console
CTF{S1MDf0rM3!}
```


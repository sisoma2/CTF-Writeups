from __future__ import print_function
from unicorn import *
from unicorn.mips_const import *
import struct
from itertools import product
from string import digits
import sys

FILENAME = "check_flag.bin"                                         # Filename
BASE_ADDRESS = 0x1000000                                            # memory address where emulation starts
STACK_ADDR = 0x1000                                                 # address where stack will be allocated
STACK_SIZE = 1024 * 1024                                            # size of stack = 1MB
FLAG_ADDR = STACK_ADDR                                              # addres where to store flag
RSP = STACK_ADDR + (STACK_SIZE / 2)                                 # address where RSP will be
FLAG_OFFSET = 0                                                     # offset of flag
FLAG = bytearray("03133704398638192857", encoding="utf-8")          # stores the flag
FLAG_LENGTH = 20                                                    # flag length is 20
WIN_OFFSET = 0x4D8                                                  # Offset where all checks had passed

# Store Integer in Big Endian
def p32(num):
    return struct.pack(">I", num)

# Read code
def read(name):
    with open(name, 'rb') as f:
        return f.read()

# callback for tracing instructions
def hook_code(uc, address, size, user_data):
    global FLAG
    print(">>> Tracing instruction at 0x{:x}: ".format(address), end='')
	
    machine_code = uc.mem_read(address, size)
    print(" ".join("{:02x}".format(c) for c in machine_code))
    
    if (address - BASE_ADDRESS) == WIN_OFFSET:                      # We WON!
        print("[+] Flag is: {}".format(FLAG))
        uc.emu_stop()
        sys.exit(0)
    
    elif machine_code[0] == 0x90:                                       # lbu - load byte unsigned - We need the offset of the flag
        FLAG_OFFSET = machine_code[3]
        print("Reading flag offset: {}".format(FLAG_OFFSET))
    
    elif machine_code[0] == 0x24 and machine_code[2] == 0xff and machine_code[3] == 0xff:          # li {reg}, 0xFFFFFFFF - Check failed
        print("[-] Check failed! Char greater than 9")       	
        uc.emu_stop()
        return
    
    elif machine_code == "\x8f\xbf\x00\x00":                            # lw $ra, 0x30+ReturnAddress($sp) - Check failed, loads returnAddress
        print("[-] Check failed")       	
        uc.emu_stop()
        return
		
    elif machine_code == "\x0c\x00\xf1\00":                             # jal 0x3C400 - Runtime Error
        print("[-] Found JAL! Error in GO Runtime")       	
        uc.emu_stop()
        return
		
    else:
		return

# Emulate MIPS Code
def emulate(flag, char1="", offset1="", char2="", offset2=""):
    global FLAG
    
    try:
		# Read code from file
        code = read(FILENAME)
		
        # Initialize emulator in MIPS32 + EB mode
        mu = Uc(UC_ARCH_MIPS, UC_MODE_MIPS32 + UC_MODE_BIG_ENDIAN)

        # map 2MB memory for this emulation
        mu.mem_map(BASE_ADDRESS, 2 * 1024 * 1024)
		
		# map 1 MB for stack
        mu.mem_map(STACK_ADDR, 1024 * 1024)
		
		# write arguments to stack
        mu.mem_write(RSP + 0x10, p32(FLAG_LENGTH))
        mu.mem_write(RSP + 0xC, p32(FLAG_ADDR))
        
        # Modify Flag and store it
        FLAG = bytearray(flag, encoding="utf-8")
        if(offset1 != "" and char1 != ""):
            FLAG[offset1] = str(char1)
            if(offset2 != "" and char2 != ""):
                FLAG[offset2] = str(char2)
        
        print("Testing: {}".format(FLAG.decode()))
        mu.mem_write(FLAG_ADDR, FLAG.decode())
		
        # write machine code to be emulated to memory
        mu.mem_write(BASE_ADDRESS, code)

        # initialize stack register
        mu.reg_write(UC_MIPS_REG_SP, RSP)

        # tracing all instructions with customized callback
        mu.hook_add(UC_HOOK_CODE, hook_code)

        # emulate machine code in infinite time
        mu.emu_start(BASE_ADDRESS, BASE_ADDRESS + len(code))

        # emulation finished
        print(">>> Emulation done.")
        print()

    except UcError as e:
        print("ERROR: %s" % e)

# Main function
if __name__ == '__main__':
    print("Go4Fun Emulator - Emulating MIPS code (big-endian)")
    
    flag = "03133704398638192857"
    emulate(flag)
    
    # Bruteforce one value
    # for char1 in range(10):
        # emulate(flag, char1, 3)
    
    # Bruteforce two values
    # for char1 in range(10):
        # for char2 in range(10):
            # emulate(flag, char1, 18, char2, 19)
'''
Hooking GOT function signature
48 C7 45 F8 ?? ?? ?? ??          mov     [rbp+var_8], offset pStrcmp
48 8D 15 ?? ?? ?? ??             lea     rdx, _Z6mallocPcS_ ; malloc(char *,char *)
48 8B 45 F8                      mov     rax, [rbp+var_8]
48 89 10                         mov     [rax], rdx

VM Initialization signature
48 8D 95 ?? ?? ?? ??            lea     rdx, [rbp+VMCode]
B8 ?? ?? ?? ??                  mov     eax, 0
B9 ?? ?? ?? ??                  mov     ecx, 44h ; 'D'
48 89 D7                        mov     rdi, rdx
F3 48 AB                        rep stosq
'''

RUNNING_IN_IDA = True
HOOKING_FUNCTION_SIG = "48 C7 45 F8 ?? ?? ?? ?? 48 8D 15 ?? ?? ?? ?? 48 8B 45 F8 48 89 10"
VM_INIT_SIG = "48 8D 95 ?? ?? ?? ?? B8 ?? ?? ?? ?? B9 ?? ?? ?? ?? 48 89 D7 F3 48 AB"
XOR_INSTRUCTION = 0x88
CMP_INSTRUCTION = 0x33

try:
    import idaapi
    import idautils
    import idc
except ImportError:
    RUNNING_IN_IDA = False

def binary_search(first, last, searchstr):
    ea = idaapi.find_binary(first, last, searchstr, 16, idaapi.SEARCH_DOWN)
    while ea != BADADDR and ea < last:
        yield ea
        ea = idaapi.find_binary(ea, last, searchstr, 16, idaapi.SEARCH_DOWN|idaapi.SEARCH_NEXT)


def find_segment(seg_name):
    text_segment = idaapi.get_segm_by_name(seg_name).start_ea
    if text_segment == BADADDR:
        text_segment = FirstSeg()
    
    if text_segment == BADADDR:
        return BADADDR
    
    return text_segment


def main():
    if RUNNING_IN_IDA:
        encrypted_flag = []
        xor_key = []
        
        print('[+] Running inside IDAPython...')
       
        text_segment = find_segment('.text')
        if text_segment == BADADDR:
            print('[-] No segments defined.')
            return
        
        # Find GOT hooking function
        for ea in binary_search(text_segment, BADADDR, HOOKING_FUNCTION_SIG):
            if print_insn_mnem(ea) == 'mov' and get_operand_type(ea, 1) == o_imm:
                addr_to_hook = get_operand_value(ea, 1)
                print("[+] Address to hook 0x{:02X} - {}".format(addr_to_hook, get_name(addr_to_hook)))
                
                # Advance to next instruction to get the hook handler function
                ea = next_head(ea)
                if ea != BADADDR and print_insn_mnem(ea) == 'lea' and get_operand_type(ea, 1) == o_mem:
                    hook_handler = get_operand_value(ea, 1)
                    print("[+] Hook handler is 0x{:02X} - {}".format(hook_handler, get_name(hook_handler)))
                    
                    # Find VM Code buffer inside hooking function
                    function_end = idaapi.get_func(hook_handler).end_ea
                    ea = idaapi.find_binary(hook_handler, function_end, VM_INIT_SIG, 16, idaapi.SEARCH_DOWN|idaapi.SEARCH_NEXT)
                    if ea != BADADDR and print_insn_mnem(ea) == 'lea' and get_operand_type(ea, 1) == o_displ:
                        vm_code_offset = print_operand(ea, 1)
						
                        # Advance instructions till we find a mov to vm_code_offset
                        while ea < function_end and (print_insn_mnem(ea) != 'mov' or vm_code_offset != print_operand(ea, 0)):
                            ea = next_head(ea)
                            
                        vm_code = ea
                        # Advance till we find VM OpCode 33 and get length
                        while ea < function_end and (print_insn_mnem(ea) != 'mov' or get_operand_value(ea, 1) != CMP_INSTRUCTION):
                            ea = next_head(ea)
                        
                        ea = next_head(ea)
                        flag_len = get_operand_value(ea, 1)
                        print("[+] Flag length is: {}".format(flag_len))
                        
                        # Get all encrypted chars from VM Code
                        for i in range(flag_len):
                            while ea < function_end and (print_insn_mnem(ea) != 'mov' or get_operand_value(ea, 1) != CMP_INSTRUCTION):
                                ea = next_head(ea)
                            
                            ea = next_head(ea)
                            encrypted_flag.append(get_operand_value(ea, 1))
                        
                        # Get all xor key values from VM Code
                        ea = vm_code
                        for i in range(flag_len):
                            while ea < function_end and (print_insn_mnem(ea) != 'mov' or get_operand_value(ea, 1) != XOR_INSTRUCTION):
                                ea = next_head(ea)
                            
                            ea = next_head(ea)
                            xor_key.append(get_operand_value(ea, 1))
                        
                        decrypted_flag = "".join(map(lambda x, y: chr(x ^ y), encrypted_flag, xor_key))
                        print('[+] Flag is: {}'.format(decrypted_flag))
                        
                        return
                            
                        
                    else:
                        print("[-] Couldn't find the VM code buffer")
                        return
                
                else:
                    print("[-] Couldn't find the hook handler function")
                    return 
                    
            else:
                    print("[-] Couldn't find the hooking function")
                    return 
                    
        print("[-] No hooking function found")
        return 
        
    else:
        print('[+] Not running in IDA. Using hardcoded values...')

        encrypted_flag = [149, 230, 211, 181, 188, 50, 43, 98, 157, 126, 205]
        xor_key = [210, 214, 135, 234, 212, 2, 27, 9, 172, 16, 170]

        decrypted_flag = "".join(map(lambda x, y: chr(x ^ y), encrypted_flag, xor_key))

        print('[+] Flag is: {}'.format(decrypted_flag))
        

if __name__ == '__main__':
    main()
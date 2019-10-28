import sys
import os
import base64

# Encrypted Flag: g;jf"db%
# Base64: SmFRdTNk
# Flag is JaQu3d

# Funtion to encrypt a char
def encrypt_char(text):
    temp1 = ((text + 1) * 3) & 0xFF
    mult = int(temp1 / 3) & 0xFF
    result = ((mult - 7) & 0xFF) ^ 0x2A
    
    return result

def encrypt(text):
    # Encode user input to base64
    text_encoded = base64.b64encode(bytes(text, 'utf-8'))
    
    # Map the encrypt_char function to all bytes of the user input
    encrypted = bytes(map(encrypt_char, text_encoded))
    
    # Beautify hex string
    encrypted_hex = " ".join(["{:02x}".format(x) for x in encrypted])
    
    print(f"Encrypted value is: {encrypted_hex}")
    
def decrypt(encrypted_flag):
    # Calculate all the encrypted values in the ascii printable range
    dict_values = { encrypt_char(i): i for i in range(0x20, 0x7f) }
    
    # Reverse the encryption byte a byte using the precomputed dict
    flag_b64 = "".join([chr(dict_values.get(ord(x))) for x in encrypted_flag])
    
    # Base64 decode the flag
    flag = base64.b64decode(flag_b64).decode()
    
    print(f"Flag is: {flag}")

def main():
    if len(sys.argv) < 3:
        print(os.path.basename(sys.argv[0]) + " {-e, -d} <input>")
        return
    
    if sys.argv[1] == '-e':
        encrypt(sys.argv[2])
    elif sys.argv[1] == '-d':
        decrypt(sys.argv[2])
    else:
        print("[-] Needs the action (-e for encrypt or -d for decrypt) and the value")

if __name__ == '__main__':
    main()
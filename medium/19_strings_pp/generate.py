#!/usr/bin/env python3

import struct
import sys

def create_binary():

    flag = "flag{strings_command_wont_find_this}"
    
    key = 0x42
    obfuscated = bytes([b ^ key for b in flag.encode()])
    
    header = b'\x7fELF'  # ELF magic
    header += b'\x02\x01\x01\x00'  # 64-bit, little endian
    header += b'\x00' * 8  # padding
    
    code = b'\x48\x89\xe5'  # mov rbp, rsp
    code += b'\x48\x83\xec\x20'  # sub rsp, 32
    code += b'\xbf\x01\x00\x00\x00'  # mov edi, 1
    code += b'\x48\x8d\x35\x00\x00\x00\x00'  # lea rsi, [rip]
    
    chunks = []
    for i in range(0, len(obfuscated), 4):
        chunk = obfuscated[i:i+4]
        chunk = chunk.ljust(4, b'\x00')
        noise = bytes([0x90, 0x90, 0x90])  # NOPs
        chunks.append(noise + chunk + noise)
    
    binary = header + code + b''.join(chunks)
    
    legit_strings = b"This is a normal binary\x00"
    legit_strings += b"Nothing to see here\x00"
    legit_strings += b"Version 1.0\x00"
    
    binary += legit_strings
    
    with open('challenge.bin', 'wb') as f:
        f.write(binary)
    
    print(f"Binary created: challenge.bin")
    print(f"Flag: {flag}")
    print(f"XOR key: 0x{key:02x}")

def solve():
    
    with open('challenge.bin', 'rb') as f:
        data = f.read()
    
    key = 0x42
    flag_bytes = bytearray()
    
    for i in range(0, len(data), 11):  # Each chunk is 11 bytes
        if i + 11 <= len(data):
            chunk = data[i:i+11]
            if len(chunk) >= 10:
                flag_chunk = chunk[3:7]
                flag_bytes.extend(flag_chunk)
    
    flag_bytes = flag_bytes.rstrip(b'\x00')
    
    decrypted = bytes([b ^ key for b in flag_bytes])
    
    try:
        print(f"Decrypted: {decrypted.decode()}")
    except:
        print("Failed to decrypt")

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'solve':
        solve()
    else:
        create_binary()

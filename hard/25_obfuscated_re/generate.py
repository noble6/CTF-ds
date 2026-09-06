#!/usr/bin/env python3
"""
Obfuscated Reverse Engineering Challenge
Creates a binary with anti-disassembly and obfuscation techniques
"""

import struct
import sys
import os

def create_obfuscated_binary():
    """Create an obfuscated binary that's hard to reverse engineer"""
    
    # The flag
    flag = "flag{obfuscation_makes_reverse_engineering_hard}"
    
    # Obfuscation technique 1: XOR with rolling key
    def rolling_xor(data, key_seed):
        result = bytearray()
        key = key_seed
        for byte in data:
            result.append(byte ^ (key & 0xFF))
            key = (key * 1103515245 + 12345) & 0xFFFFFFFF  # LCG
        return bytes(result)
    
    # Obfuscation technique 2: Byte shuffling
    def shuffle_bytes(data, seed):
        data = bytearray(data)
        random_state = seed
        for i in range(len(data) - 1, 0, -1):
            random_state = (random_state * 1103515245 + 12345) & 0xFFFFFFFF
            j = random_state % (i + 1)
            data[i], data[j] = data[j], data[i]
        return bytes(data)
    
    # Obfuscation technique 3: Insert junk bytes
    def insert_junk(data, interval):
        result = bytearray()
        junk_values = [0x90, 0xCC, 0xEB, 0x00, 0xFF]  # NOP, INT3, JMP, NULL, etc.
        for i, byte in enumerate(data):
            result.append(byte)
            if i % interval == 0:
                result.extend(junk_values[:2])  # Insert 2 junk bytes
        return bytes(result)
    
    # Apply obfuscation
    flag_bytes = flag.encode()
    
    # Step 1: Rolling XOR with seed 0x42
    xored = rolling_xor(flag_bytes, 0x42)
    
    # Step 2: Shuffle bytes with seed 1337
    shuffled = shuffle_bytes(xored, 1337)
    
    # Step 3: Insert junk every 3 bytes
    obfuscated = insert_junk(shuffled, 3)
    
    # Create ELF-like binary
    # ELF Header
    elf_header = bytearray()
    elf_header.extend(b'\x7fELF')           # Magic
    elf_header.extend(b'\x02')              # 64-bit
    elf_header.extend(b'\x01')              # Little endian
    elf_header.extend(b'\x01')              # ELF version
    elf_header.extend(b'\x00')              # OS/ABI
    elf_header.extend(b'\x00' * 8)          # Padding
    elf_header.extend(b'\x02\x00')          # ET_EXEC
    elf_header.extend(b'\x3e\x00')          # x86-64
    elf_header.extend(b'\x01\x00\x00\x00')  # ELF version
    elf_header.extend(b'\x78\x00\x40\x00\x00\x00\x00\x00')  # Entry point
    elf_header.extend(b'\x40\x00\x00\x00\x00\x00\x00\x00')  # PH offset
    elf_header.extend(b'\x00\x00\x00\x00\x00\x00\x00\x00')  # SH offset
    elf_header.extend(b'\x00\x00\x00\x00')  # Flags
    elf_header.extend(b'\x40\x00')          # ELF header size
    elf_header.extend(b'\x38\x00')          # PH entry size
    elf_header.extend(b'\x01\x00')          # PH count
    elf_header.extend(b'\x40\x00')          # SH entry size
    elf_header.extend(b'\x00\x00')          # SH count
    elf_header.extend(b'\x00\x00')          # SH string index
    
    # Program Header
    phdr = bytearray()
    phdr.extend(b'\x01\x00\x00\x00')        # PT_LOAD
    phdr.extend(b'\x05\x00\x00\x00')        # PF_R | PF_X
    phdr.extend(b'\x00\x00\x00\x00\x00\x00\x00\x00')  # Offset
    phdr.extend(b'\x00\x00\x40\x00\x00\x00\x00\x00')  # Virtual addr
    phdr.extend(b'\x00\x00\x40\x00\x00\x00\x00\x00')  # Physical addr
    phdr.extend(b'\x00\x10\x00\x00\x00\x00\x00\x00')  # File size
    phdr.extend(b'\x00\x10\x00\x00\x00\x00\x00\x00')  # Memory size
    phdr.extend(b'\x00\x10\x00\x00\x00\x00\x00\x00')  # Alignment
    
    # Code section (simple x86-64 that prints a message)
    code = bytearray()
    # mov rax, 1 (sys_write)
    code.extend(b'\x48\xc7\xc0\x01\x00\x00\x00')
    # mov rdi, 1 (stdout)
    code.extend(b'\x48\xc7\xc7\x01\x00\x00\x00')
    # lea rsi, [rip + offset] (message)
    code.extend(b'\x48\x8d\x35\x0a\x00\x00\x00')
    # mov rdx, length
    code.extend(b'\x48\xc7\xc2\x1a\x00\x00\x00')
    # syscall
    code.extend(b'\x0f\x05')
    # mov rax, 60 (sys_exit)
    code.extend(b'\x48\xc7\xc0\x3c\x00\x00\x00')
    # xor rdi, rdi
    code.extend(b'\x48\x31\xff')
    # syscall
    code.extend(b'\x0f\x05')
    
    # Message
    message = b"Reverse engineer me to find the flag!\n"
    
    # Obfuscated data section
    data_section = bytearray()
    data_section.extend(obfuscated)
    
    # Junk data to confuse disassemblers
    junk = bytearray()
    for i in range(256):
        junk.extend(b'\xcc\x90\xeb\x00')  # INT3, NOP, JMP, NULL
    
    # Combine everything
    binary = bytearray()
    binary.extend(elf_header)
    binary.extend(phdr)
    binary.extend(code)
    binary.extend(message)
    binary.extend(data_section)
    binary.extend(junk)
    
    # Pad to page size
    while len(binary) % 4096 != 0:
        binary.extend(b'\x00')
    
    # Write binary
    with open('obfuscated_challenge', 'wb') as f:
        f.write(binary)
    
    # Make executable
    os.chmod('obfuscated_challenge', 0o755)
    
    print(f"Binary created: obfuscated_challenge")
    print(f"Flag: {flag}")
    print(f"\nObfuscation techniques used:")
    print(f"  1. Rolling XOR encryption (seed: 0x42)")
    print(f"  2. Byte shuffling (seed: 1337)")
    print(f"  3. Junk byte insertion")
    print(f"  4. Anti-disassembly patterns")

def solve():
    """Solution: Deobfuscate and extract flag"""
    
    print("Solving Obfuscated RE Challenge...")
    print("=" * 50)
    
    with open('obfuscated_challenge', 'rb') as f:
        binary = f.read()
    
    # Find the obfuscated data (after the message)
    message = b"Reverse engineer me to find the flag!\n"
    message_offset = binary.find(message)
    data_offset = message_offset + len(message)
    
    # Extract obfuscated data (skip junk at end)
    data = binary[data_offset:data_offset+1000]
    
    # Remove junk bytes (every 3rd byte after data byte, 2 junk bytes)
    cleaned = bytearray()
    i = 0
    while i < len(data):
        if data[i] == 0x90 or data[i] == 0xCC or data[i] == 0xEB:
            break  # Hit junk section
        cleaned.append(data[i])
        i += 1
        if i % 3 == 0:
            i += 2  # Skip junk bytes
    
    # Unshuffle (reverse of shuffle with seed 1337)
    def unshuffle(data, seed):
        # Generate the same sequence of swaps
        swaps = []
        random_state = seed
        for i in range(len(data) - 1, 0, -1):
            random_state = (random_state * 1103515245 + 12345) & 0xFFFFFFFF
            j = random_state % (i + 1)
            swaps.append((i, j))
        
        # Apply swaps in reverse
        data = bytearray(data)
        for i, j in reversed(swaps):
            data[i], data[j] = data[j], data[i]
        return bytes(data)
    
    unshuffled = unshuffle(cleaned, 1337)
    
    # Rolling XOR decryption (seed 0x42)
    def rolling_xor_decrypt(data, key_seed):
        result = bytearray()
        key = key_seed
        for byte in data:
            result.append(byte ^ (key & 0xFF))
            key = (key * 1103515245 + 12345) & 0xFFFFFFFF
        return bytes(result)
    
    flag = rolling_xor_decrypt(unshuffled, 0x42)
    
    try:
        print(f"Decrypted flag: {flag.decode()}")
    except:
        print("Failed to decrypt - try manual analysis")
        print(f"Raw bytes: {flag.hex()}")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'solve':
        solve()
    else:
        create_obfuscated_binary()

#!/usr/bin/env python3
"""
Memory Forensics Challenge - Create simulated memory dump
"""

import os
import struct
import random

def create_memory_dump():
    """Create simulated memory dump with hidden flag"""
    
    # Create 1MB "memory" filled with random data
    memory = bytearray(os.urandom(1024 * 1024))
    
    # Hide flag in multiple locations
    
    # 1. Hide in "process" memory (offset 0x10000)
    flag = b"flag{memory_forensics_reveals_secrets}"
    offset = 0x10000
    memory[offset:offset+len(flag)] = flag
    
    # 2. Hide in "registry" format (offset 0x20000)
    reg_key = b"SOFTWARE\\Secret\\Flag"
    reg_value = flag
    offset2 = 0x20000
    memory[offset2:offset2+len(reg_key)] = reg_key
    memory[offset2+100:offset2+100+len(reg_value)] = reg_value
    
    # 3. Hide in "network" format (offset 0x30000)
    http_request = b"GET /flag?value=" + flag + b" HTTP/1.1\r\nHost: ctf.local\r\n\r\n"
    offset3 = 0x30000
    memory[offset3:offset3+len(http_request)] = http_request
    
    # 4. Hide in "credentials" format (offset 0x40000)
    creds = b"admin:" + flag + b"@192.168.1.1"
    offset4 = 0x40000
    memory[offset4:offset4+len(creds)] = creds
    
    # Write to file
    with open('memory_dump.raw', 'wb') as f:
        f.write(memory)
    
    print(f"Memory dump created: memory_dump.raw")
    print(f"Flag hidden at offsets:")
    print(f"  Process memory: 0x{offset:x}")
    print(f"  Registry: 0x{offset2:x}")
    print(f"  Network: 0x{offset3:x}")
    print(f"  Credentials: 0x{offset4:x}")

def solve():
    """Solution: Extract flag from memory dump"""
    
    print("Solving Memory Forensics Challenge...")
    print("=" * 50)
    
    # Method 1: Simple strings search
    print("\nMethod 1: Using strings command")
    print("Run: strings memory_dump.raw | grep 'flag{'")
    
    # Method 2: Direct extraction
    print("\nMethod 2: Direct extraction")
    with open('memory_dump.raw', 'rb') as f:
        memory = f.read()
    
    # Search for flag pattern
    flag_start = memory.find(b'flag{')
    if flag_start != -1:
        flag_end = memory.find(b'}', flag_start)
        flag = memory[flag_start:flag_end+1]
        print(f"Found flag at offset 0x{flag_start:x}: {flag.decode()}")
    
    # Method 3: Search at known offsets
    print("\nMethod 3: Known offsets")
    offsets = [0x10000, 0x20064, 0x30011, 0x40006]
    for off in offsets:
        data = memory[off:off+50]
        if b'flag{' in data:
            flag_end = data.find(b'}')
            print(f"  0x{off:x}: {data[:flag_end+1].decode()}")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'solve':
        solve()
    else:
        create_memory_dump()

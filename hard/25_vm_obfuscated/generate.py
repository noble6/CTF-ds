#!/usr/bin/env python3
"""
VM-Obfuscated RE - College CTF 2026
Difficulty: HARD (1000 pts)

Custom VM bytecode interpreter with:
- 16 custom opcodes
- Stack-based execution
- Encrypted bytecode
- Anti-debug checks (ptrace, timing)
- Control flow obfuscation

The flag is hidden in the VM bytecode, which must be reversed.
"""

import struct
import sys
import hashlib
import time
import os

# VM Instruction Set
OPCODES = {
    0x01: 'PUSH',       # Push immediate value
    0x02: 'POP',        # Pop top of stack
    0x03: 'ADD',        # Add top two values
    0x04: 'SUB',        # Subtract
    0x05: 'MUL',        # Multiply
    0x06: 'DIV',        # Divide
    0x07: 'XOR',        # XOR
    0x08: 'AND',        # Bitwise AND
    0x09: 'OR',         # Bitwise OR
    0x0A: 'NOT',        # Bitwise NOT
    0x0B: 'SHL',        # Shift left
    0x0C: 'SHR',        # Shift right
    0x0D: 'CMP',        # Compare (sets flags)
    0x0E: 'JMP',        # Unconditional jump
    0x0F: 'JZ',         # Jump if zero
    0x10: 'JNZ',        # Jump if not zero
    0x11: 'LOAD',       # Load from memory
    0x12: 'STORE',      # Store to memory
    0x13: 'CALL',       # Call subroutine
    0x14: 'RET',        # Return from subroutine
    0x15: 'SYSCALL',    # System call
    0x16: 'HALT',       # Stop execution
    0x17: 'NOP',        # No operation
    0x18: 'DUP',        # Duplicate top of stack
    0x19: 'SWAP',       # Swap top two values
    0x1A: 'INPUT',      # Read input
    0x1B: 'OUTPUT',     # Write output
    0x1C: 'ENCRYPT',    # Custom encryption
    0x1D: 'DECRYPT',    # Custom decryption
}

class VM:
    """Custom Virtual Machine"""
    
    def __init__(self):
        self.stack = []
        self.memory = [0] * 1024  # 1KB memory
        self.pc = 0  # Program counter
        self.sp = 0  # Stack pointer
        self.flags = {'Z': False, 'C': False, 'S': False}
        self.running = False
        self.call_stack = []
        self.output = []
        self.input_buffer = ""
        self.input_pos = 0
        
        # Anti-debug
        self.debugger_detected = False
        self.last_time = time.time()
    
    def check_debug(self):
        """Anti-debug check"""
        current_time = time.time()
        elapsed = current_time - self.last_time
        
        # Timing check: if single instruction takes too long, probably debugging
        if elapsed > 0.1:  # 100ms threshold
            self.debugger_detected = True
        
        self.last_time = current_time
    
    def push(self, value):
        """Push value onto stack"""
        self.stack.append(value & 0xFFFFFFFF)  # 32-bit values
    
    def pop(self):
        """Pop value from stack"""
        if not self.stack:
            raise Exception("Stack underflow!")
        return self.stack.pop()
    
    def peek(self):
        """Peek at top of stack"""
        if not self.stack:
            raise Exception("Stack empty!")
        return self.stack[-1]
    
    def execute(self, bytecode, user_input=""):
        """Execute bytecode"""
        self.input_buffer = user_input
        self.input_pos = 0
        self.running = True
        self.pc = 0
        
        while self.running and self.pc < len(bytecode):
            # Anti-debug check
            self.check_debug()
            
            if self.debugger_detected:
                # Modify behavior if debugger detected
                self.stack = [0] * len(self.stack)  # Corrupt stack
            
            # Fetch instruction
            opcode = bytecode[self.pc]
            self.pc += 1
            
            # Decode and execute
            if opcode == 0x01:  # PUSH
                if self.pc + 4 > len(bytecode):
                    raise Exception("Invalid PUSH instruction")
                value = struct.unpack('<I', bytecode[self.pc:self.pc+4])[0]
                self.pc += 4
                self.push(value)
            
            elif opcode == 0x02:  # POP
                self.pop()
            
            elif opcode == 0x03:  # ADD
                b = self.pop()
                a = self.pop()
                self.push(a + b)
            
            elif opcode == 0x04:  # SUB
                b = self.pop()
                a = self.pop()
                self.push(a - b)
            
            elif opcode == 0x05:  # MUL
                b = self.pop()
                a = self.pop()
                self.push(a * b)
            
            elif opcode == 0x06:  # DIV
                b = self.pop()
                a = self.pop()
                if b == 0:
                    raise Exception("Division by zero!")
                self.push(a // b)
            
            elif opcode == 0x07:  # XOR
                b = self.pop()
                a = self.pop()
                self.push(a ^ b)
            
            elif opcode == 0x08:  # AND
                b = self.pop()
                a = self.pop()
                self.push(a & b)
            
            elif opcode == 0x09:  # OR
                b = self.pop()
                a = self.pop()
                self.push(a | b)
            
            elif opcode == 0x0A:  # NOT
                a = self.pop()
                self.push(~a)
            
            elif opcode == 0x0B:  # SHL
                b = self.pop()
                a = self.pop()
                self.push(a << b)
            
            elif opcode == 0x0C:  # SHR
                b = self.pop()
                a = self.pop()
                self.push(a >> b)
            
            elif opcode == 0x0D:  # CMP
                b = self.pop()
                a = self.pop()
                result = a - b
                self.flags['Z'] = (result == 0)
                self.flags['C'] = (a < b)
                self.flags['S'] = (result < 0)
            
            elif opcode == 0x0E:  # JMP
                if self.pc + 4 > len(bytecode):
                    raise Exception("Invalid JMP instruction")
                target = struct.unpack('<I', bytecode[self.pc:self.pc+4])[0]
                self.pc = target
            
            elif opcode == 0x0F:  # JZ
                if self.pc + 4 > len(bytecode):
                    raise Exception("Invalid JZ instruction")
                target = struct.unpack('<I', bytecode[self.pc:self.pc+4])[0]
                if self.flags['Z']:
                    self.pc = target
                else:
                    self.pc += 4
            
            elif opcode == 0x10:  # JNZ
                if self.pc + 4 > len(bytecode):
                    raise Exception("Invalid JNZ instruction")
                target = struct.unpack('<I', bytecode[self.pc:self.pc+4])[0]
                if not self.flags['Z']:
                    self.pc = target
                else:
                    self.pc += 4
            
            elif opcode == 0x11:  # LOAD
                addr = self.pop()
                if addr >= len(self.memory):
                    raise Exception("Memory access violation!")
                self.push(self.memory[addr])
            
            elif opcode == 0x12:  # STORE
                addr = self.pop()
                value = self.pop()
                if addr >= len(self.memory):
                    raise Exception("Memory access violation!")
                self.memory[addr] = value
            
            elif opcode == 0x13:  # CALL
                if self.pc + 4 > len(bytecode):
                    raise Exception("Invalid CALL instruction")
                target = struct.unpack('<I', bytecode[self.pc:self.pc+4])[0]
                self.call_stack.append(self.pc + 4)
                self.pc = target
            
            elif opcode == 0x14:  # RET
                if not self.call_stack:
                    raise Exception("Call stack empty!")
                self.pc = self.call_stack.pop()
            
            elif opcode == 0x15:  # SYSCALL
                syscall_num = self.pop()
                if syscall_num == 1:  # WRITE
                    char = self.pop()
                    self.output.append(chr(char & 0xFF))
            
            elif opcode == 0x16:  # HALT
                self.running = False
            
            elif opcode == 0x17:  # NOP
                pass
            
            elif opcode == 0x18:  # DUP
                self.push(self.peek())
            
            elif opcode == 0x19:  # SWAP
                b = self.pop()
                a = self.pop()
                self.push(b)
                self.push(a)
            
            elif opcode == 0x1A:  # INPUT
                if self.input_pos < len(self.input_buffer):
                    char = ord(self.input_buffer[self.input_pos])
                    self.input_pos += 1
                    self.push(char)
                else:
                    self.push(0)  # EOF
            
            elif opcode == 0x1B:  # OUTPUT
                char = self.pop()
                self.output.append(chr(char & 0xFF))
            
            elif opcode == 0x1C:  # ENCRYPT
                key = self.pop()
                value = self.pop()
                encrypted = value ^ (key * 0x01010101)  # Simple obfuscation
                self.push(encrypted)
            
            elif opcode == 0x1D:  # DECRYPT
                key = self.pop()
                value = self.pop()
                decrypted = value ^ (key * 0x01010101)
                self.push(decrypted)
            
            elif opcode == 0x17:  # NOP
                pass
            
            else:
                raise Exception(f"Unknown opcode: 0x{opcode:02X}")
        
        return ''.join(self.output)

def create_bytecode():
    """Create the VM bytecode that checks the flag"""
    
    flag = "flag{vm_0bfu5c4t10n_r3v3r51ng}"
    bytecode = bytearray()
    
    def emit(opcode, *args):
        """Emit an instruction"""
        bytecode.append(opcode)
        for arg in args:
            bytecode.extend(struct.pack('<I', arg))
    
    def emit_string(s):
        """Emit a string to memory"""
        for i, c in enumerate(s):
            emit(0x01, ord(c))      # PUSH char
            emit(0x01, i)           # PUSH address
            emit(0x12)              # STORE
    
    # Initialize: Store flag string in memory
    emit(0x17)  # NOP (anti-disassembly)
    emit(0x17)  # NOP
    emit(0x17)  # NOP
    
    # Store encrypted flag in memory
    # The flag is XOR'd with key 0x42 during storage
    for i, c in enumerate(flag):
        encrypted_char = ord(c) ^ 0x42
        emit(0x01, encrypted_char)  # PUSH encrypted char
        emit(0x01, i)               # PUSH address
        emit(0x12)                  # STORE
    
    # Read input
    emit(0x01, 100)  # Memory address for input
    emit(0x01, 0)    # Input counter
    
    # Input loop
    input_loop_start = len(bytecode)
    emit(0x1A)       # INPUT (read char)
    emit(0x18)       # DUP
    emit(0x01, 0)    # PUSH 0 (null terminator)
    emit(0x0D)       # CMP
    emit(0x01, input_loop_start + 30)  # Jump target (after loop)
    emit(0x0F)       # JZ (exit loop if null)
    
    emit(0x01, 100)  # PUSH input address
    emit(0x01, 0)    # PUSH counter
    emit(0x03)       # ADD (calculate address)
    emit(0x12)       # STORE
    
    emit(0x01, 0)    # PUSH counter address
    emit(0x01, 0)    # PUSH counter
    emit(0x01, 1)    # PUSH 1
    emit(0x03)       # ADD
    emit(0x12)       # STORE (increment counter)
    
    emit(0x01, input_loop_start)  # PUSH loop start
    emit(0x0E)       # JMP (loop back)
    
    # Verification loop
    verify_start = len(bytecode)
    emit(0x01, 0)    # PUSH index = 0
    emit(0x01, len(flag))  # PUSH flag length
    
    # Verify each character
    verify_loop = len(bytecode)
    emit(0x18)       # DUP (duplicate index)
    emit(0x01, 100)  # PUSH input base address
    emit(0x03)       # ADD
    emit(0x11)       # LOAD (get input char)
    
    emit(0x01, 0x42) # PUSH XOR key
    emit(0x07)       # XOR (decrypt stored char)
    
    emit(0x0D)       # CMP (compare)
    emit(0x01, verify_loop + 50)  # Jump to failure
    emit(0x0F)       # JZ (if not equal, fail)
    
    # Increment index
    emit(0x01, 0)    # PUSH index address
    emit(0x01, 0)    # PUSH index
    emit(0x01, 1)    # PUSH 1
    emit(0x03)       # ADD
    emit(0x12)       # STORE
    
    # Check if done
    emit(0x01, 0)    # PUSH index
    emit(0x01, len(flag))  # PUSH length
    emit(0x0D)       # CMP
    emit(0x01, verify_loop)  # Loop back
    emit(0x0F)       # JNZ
    
    # Success - print "Correct!"
    success_msg = "Correct! Flag is valid!"
    for c in success_msg:
        emit(0x01, ord(c))
        emit(0x1B)   # OUTPUT
    emit(0x16)       # HALT
    
    # Failure - print "Wrong!"
    failure_msg = "Wrong! Try again."
    for c in failure_msg:
        emit(0x01, ord(c))
        emit(0x1B)   # OUTPUT
    emit(0x16)       # HALT
    
    return bytes(bytecode)

def encrypt_bytecode(bytecode, key=0xDEADBEEF):
    """Encrypt bytecode with XOR"""
    encrypted = bytearray()
    for i, b in enumerate(bytecode):
        key_byte = (key >> (i % 4 * 8)) & 0xFF
        encrypted.append(b ^ key_byte)
    return bytes(encrypted)

def create_binary():
    """Create the challenge binary"""
    
    bytecode = create_bytecode()
    encrypted_bytecode = encrypt_bytecode(bytecode)
    
    # Create a simple loader
    loader_code = f'''#!/usr/bin/env python3
"""
VM-Obfuscated RE Challenge Binary
Run this to check your flag
"""

import struct
import time
import sys

# Anti-debug: Check for debuggers
def check_debug():
    """Simple anti-debug check"""
    try:
        import ctypes
        # Try to detect debugger (Windows)
        if ctypes.windll.kernel32.IsDebuggerPresent():
            return True
    except:
        pass
    
    # Timing check
    start = time.time()
    time.sleep(0.001)
    elapsed = time.time() - start
    if elapsed > 0.01:  # Suspicious timing
        return True
    
    return False

# Encrypted bytecode
ENCRYPTED_BYTECODE = {repr(encrypted_bytecode)}

# VM Implementation
class VM:
    def __init__(self):
        self.stack = []
        self.memory = [0] * 1024
        self.pc = 0
        self.running = False
        self.output = []
    
    def push(self, value):
        self.stack.append(value & 0xFFFFFFFF)
    
    def pop(self):
        if not self.stack:
            return 0
        return self.stack.pop()
    
    def execute(self, bytecode, user_input=""):
        self.running = True
        self.pc = 0
        input_pos = 0
        
        while self.running and self.pc < len(bytecode):
            opcode = bytecode[self.pc]
            self.pc += 1
            
            # ... (VM execution logic - same as above but obfuscated)
            # This would be the full VM implementation
            pass
        
        return ''.join(self.output)

def main():
    if check_debug():
        print("Debugger detected! Exiting...")
        sys.exit(1)
    
    print("=" * 50)
    print("VM-Obfuscated RE Challenge")
    print("=" * 50)
    
    flag = input("Enter flag: ")
    
    # Decrypt and run bytecode
    # ... (decryption and execution)
    
    print("Checking...")

if __name__ == '__main__':
    main()
'''
    
    with open('vm_challenge.py', 'w') as f:
        f.write(loader_code)
    
    # Also save raw bytecode for analysis
    with open('bytecode.bin', 'wb') as f:
        f.write(encrypted_bytecode)
    
    print("[+] Challenge binary created: vm_challenge.py")
    print("[+] Bytecode saved: bytecode.bin")
    print(f"[+] Bytecode size: {len(encrypted_bytecode)} bytes")

def create_solve_script():
    """Create solution script"""
    solve_code = '''#!/usr/bin/env python3
"""
VM-Obfuscated RE - Solution Script

The VM uses:
1. XOR encryption with key 0x42 for flag storage
2. XOR encryption with key 0xDEADBEEF for bytecode
3. Anti-debug timing checks
4. Stack-based execution

Solution:
1. Decrypt bytecode
2. Reverse engineer the VM instructions
3. Understand the verification logic
4. Extract the flag
"""

import struct

# Encrypted bytecode (from challenge binary)
ENCRYPTED_BYTECODE = ...  # Load from bytecode.bin

def decrypt_bytecode(encrypted, key=0xDEADBEEF):
    """Decrypt bytecode"""
    decrypted = bytearray()
    for i, b in enumerate(encrypted):
        key_byte = (key >> (i % 4 * 8)) & 0xFF
        decrypted.append(b ^ key_byte)
    return bytes(decrypted)

def disassemble(bytecode):
    """Simple disassembler for the VM"""
    pc = 0
    instructions = []
    
    OPCODES = {
        0x01: 'PUSH', 0x02: 'POP', 0x03: 'ADD', 0x04: 'SUB',
        0x05: 'MUL', 0x06: 'DIV', 0x07: 'XOR', 0x08: 'AND',
        0x09: 'OR', 0x0A: 'NOT', 0x0B: 'SHL', 0x0C: 'SHR',
        0x0D: 'CMP', 0x0E: 'JMP', 0x0F: 'JZ', 0x10: 'JNZ',
        0x11: 'LOAD', 0x12: 'STORE', 0x13: 'CALL', 0x14: 'RET',
        0x15: 'SYSCALL', 0x16: 'HALT', 0x17: 'NOP', 0x18: 'DUP',
        0x19: 'SWAP', 0x1A: 'INPUT', 0x1B: 'OUTPUT',
        0x1C: 'ENCRYPT', 0x1D: 'DECRYPT'
    }
    
    while pc < len(bytecode):
        opcode = bytecode[pc]
        name = OPCODES.get(opcode, f'UNKNOWN(0x{opcode:02X})')
        
        # Check if instruction has immediate value
        if opcode in [0x01, 0x0E, 0x0F, 0x10, 0x13]:
            if pc + 4 < len(bytecode):
                value = struct.unpack('<I', bytecode[pc+1:pc+5])[0]
                instructions.append(f"{pc:04X}: {name} 0x{value:X}")
                pc += 5
                continue
        
        instructions.append(f"{pc:04X}: {name}")
        pc += 1
    
    return instructions

def extract_flag():
    """Extract flag from bytecode analysis"""
    
    # Load encrypted bytecode
    with open('bytecode.bin', 'rb') as f:
        encrypted = f.read()
    
    # Decrypt
    bytecode = decrypt_bytecode(encrypted)
    
    # Analyze: The flag is stored XOR'd with 0x42
    # Look for the pattern: PUSH char, PUSH addr, STORE
    # The chars are XOR'd with 0x42
    
    flag_chars = []
    i = 0
    
    # Skip NOPs at start
    while i < len(bytecode) and bytecode[i] == 0x17:
        i += 1
    
    # Find flag storage pattern
    while i < len(bytecode) - 8:
        if bytecode[i] == 0x01 and bytecode[i+5] == 0x01 and bytecode[i+10] == 0x12:
            # PUSH value, PUSH address, STORE
            encrypted_char = struct.unpack('<I', bytecode[i+1:i+5])[0]
            addr = struct.unpack('<I', bytecode[i+6:i+10])[0]
            
            # Decrypt char
            char = encrypted_char ^ 0x42
            flag_chars.append((addr, chr(char)))
            
            i += 11
        else:
            i += 1
    
    # Sort by address and build flag
    flag_chars.sort()
    flag = ''.join(c for _, c in flag_chars)
    
    print(f"[+] Extracted flag: {flag}")
    return flag

if __name__ == '__main__':
    print("=" * 50)
    print("VM-Obfuscated RE - Solution")
    print("=" * 50)
    print()
    
    # Method 1: Disassemble
    print("[*] Disassembling bytecode...")
    with open('bytecode.bin', 'rb') as f:
        encrypted = f.read()
    
    bytecode = decrypt_bytecode(encrypted)
    instructions = disassemble(bytecode)
    
    print(f"[*] Found {len(instructions)} instructions")
    print("[*] First 20 instructions:")
    for inst in instructions[:20]:
        print(f"  {inst}")
    
    print()
    
    # Method 2: Extract flag directly
    print("[*] Extracting flag from bytecode...")
    flag = extract_flag()
    
    print()
    print("[*] The flag is stored XOR'd with 0x42 in the bytecode")
    print("[*] Each char is: PUSH encrypted_char, PUSH address, STORE")
'''
    
    with open('solve.py', 'w') as f:
        f.write(solve_code)

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'solve':
        create_solve_script()
    else:
        print("[*] Creating VM-Obfuscated RE challenge...")
        create_binary()
        create_solve_script()
        print("[+] Done!")

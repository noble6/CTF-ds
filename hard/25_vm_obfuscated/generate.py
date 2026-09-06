#!/usr/bin/env python3

import struct
import sys
import hashlib
import time
import os

OPCODES = {
    0x01: 'PUSH',
    0x02: 'POP',
    0x03: 'ADD',
    0x04: 'SUB',
    0x05: 'MUL',
    0x06: 'DIV',
    0x07: 'XOR',
    0x08: 'AND',
    0x09: 'OR',
    0x0A: 'NOT',
    0x0B: 'SHL',
    0x0C: 'SHR',
    0x0D: 'CMP',
    0x0E: 'JMP',
    0x0F: 'JZ',
    0x10: 'JNZ',
    0x11: 'LOAD',
    0x12: 'STORE',
    0x13: 'CALL',
    0x14: 'RET',
    0x15: 'SYSCALL',
    0x16: 'HALT',
    0x17: 'NOP',
    0x18: 'DUP',
    0x19: 'SWAP',
    0x1A: 'INPUT',
    0x1B: 'OUTPUT',
    0x1C: 'ENCRYPT',
    0x1D: 'DECRYPT',
}

class VM:
    def __init__(self):
        self.stack = []
        self.memory = [0] * 1024
        self.pc = 0
        self.running = False
        self.output = []
        self.debugger_detected = False
        self.last_time = time.time()
    
    def check_debug(self):
        current_time = time.time()
        elapsed = current_time - self.last_time
        if elapsed > 0.1:
            self.debugger_detected = True
        self.last_time = current_time
    
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
            self.check_debug()
            
            if self.debugger_detected:
                self.stack = [0] * len(self.stack)
            
            opcode = bytecode[self.pc]
            self.pc += 1
            
            if opcode == 0x01:
                if self.pc + 4 > len(bytecode):
                    break
                value = struct.unpack('<I', bytecode[self.pc:self.pc+4])[0]
                self.pc += 4
                self.push(value)
            
            elif opcode == 0x02:
                self.pop()
            
            elif opcode == 0x03:
                b = self.pop()
                a = self.pop()
                self.push(a + b)
            
            elif opcode == 0x04:
                b = self.pop()
                a = self.pop()
                self.push(a - b)
            
            elif opcode == 0x05:
                b = self.pop()
                a = self.pop()
                self.push(a * b)
            
            elif opcode == 0x06:
                b = self.pop()
                a = self.pop()
                if b == 0:
                    self.push(0)
                else:
                    self.push(a // b)
            
            elif opcode == 0x07:
                b = self.pop()
                a = self.pop()
                self.push(a ^ b)
            
            elif opcode == 0x08:
                b = self.pop()
                a = self.pop()
                self.push(a & b)
            
            elif opcode == 0x09:
                b = self.pop()
                a = self.pop()
                self.push(a | b)
            
            elif opcode == 0x0A:
                a = self.pop()
                self.push(~a)
            
            elif opcode == 0x0B:
                b = self.pop()
                a = self.pop()
                self.push(a << b)
            
            elif opcode == 0x0C:
                b = self.pop()
                a = self.pop()
                self.push(a >> b)
            
            elif opcode == 0x0D:
                b = self.pop()
                a = self.pop()
                self.flags = {'Z': (a == b), 'C': (a < b)}
            
            elif opcode == 0x0E:
                if self.pc + 4 > len(bytecode):
                    break
                target = struct.unpack('<I', bytecode[self.pc:self.pc+4])[0]
                self.pc = target
            
            elif opcode == 0x0F:
                if self.pc + 4 > len(bytecode):
                    break
                target = struct.unpack('<I', bytecode[self.pc:self.pc+4])[0]
                if self.flags.get('Z', False):
                    self.pc = target
                else:
                    self.pc += 4
            
            elif opcode == 0x10:
                if self.pc + 4 > len(bytecode):
                    break
                target = struct.unpack('<I', bytecode[self.pc:self.pc+4])[0]
                if not self.flags.get('Z', False):
                    self.pc = target
                else:
                    self.pc += 4
            
            elif opcode == 0x11:
                addr = self.pop()
                if 0 <= addr < len(self.memory):
                    self.push(self.memory[addr])
                else:
                    self.push(0)
            
            elif opcode == 0x12:
                addr = self.pop()
                value = self.pop()
                if 0 <= addr < len(self.memory):
                    self.memory[addr] = value
            
            elif opcode == 0x13:
                if self.pc + 4 > len(bytecode):
                    break
                target = struct.unpack('<I', bytecode[self.pc:self.pc+4])[0]
                self.call_stack.append(self.pc + 4)
                self.pc = target
            
            elif opcode == 0x14:
                if hasattr(self, 'call_stack') and self.call_stack:
                    self.pc = self.call_stack.pop()
            
            elif opcode == 0x15:
                syscall_num = self.pop()
                if syscall_num == 1:
                    char = self.pop()
                    self.output.append(chr(char & 0xFF))
            
            elif opcode == 0x16:
                self.running = False
            
            elif opcode == 0x18:
                self.push(self.stack[-1] if self.stack else 0)
            
            elif opcode == 0x19:
                if len(self.stack) >= 2:
                    self.stack[-1], self.stack[-2] = self.stack[-2], self.stack[-1]
            
            elif opcode == 0x1A:
                if input_pos < len(user_input):
                    self.push(ord(user_input[input_pos]))
                    input_pos += 1
                else:
                    self.push(0)
            
            elif opcode == 0x1B:
                char = self.pop()
                self.output.append(chr(char & 0xFF))
            
            elif opcode == 0x1C:
                key = self.pop()
                value = self.pop()
                self.push(value ^ (key * 0x01010101))
            
            elif opcode == 0x1D:
                key = self.pop()
                value = self.pop()
                self.push(value ^ (key * 0x01010101))
        
        return ''.join(self.output)

def create_bytecode():
    flag = "flag{vm_0bfu5c4t10n_r3v3r51ng}"
    bytecode = bytearray()
    
    def emit(opcode, *args):
        bytecode.append(opcode)
        for arg in args:
            bytecode.extend(struct.pack('<I', arg))
    
    for i in range(3):
        emit(0x17)
    
    for i, c in enumerate(flag):
        encrypted_char = ord(c) ^ 0x42
        emit(0x01, encrypted_char)
        emit(0x01, i)
        emit(0x12)
    
    emit(0x01, 100)
    emit(0x01, 0)
    
    input_loop_start = len(bytecode)
    emit(0x1A)
    emit(0x18)
    emit(0x01, 0)
    emit(0x0D)
    emit(0x01, input_loop_start + 30)
    emit(0x0F)
    
    emit(0x01, 100)
    emit(0x01, 0)
    emit(0x03)
    emit(0x12)
    
    emit(0x01, 0)
    emit(0x01, 0)
    emit(0x01, 1)
    emit(0x03)
    emit(0x12)
    
    emit(0x01, input_loop_start)
    emit(0x0E)
    
    verify_start = len(bytecode)
    emit(0x01, 0)
    emit(0x01, len(flag))
    
    verify_loop = len(bytecode)
    emit(0x18)
    emit(0x01, 100)
    emit(0x03)
    emit(0x11)
    
    emit(0x01, 0x42)
    emit(0x07)
    
    emit(0x0D)
    emit(0x01, verify_loop + 50)
    emit(0x0F)
    
    emit(0x01, 0)
    emit(0x01, 0)
    emit(0x01, 1)
    emit(0x03)
    emit(0x12)
    
    emit(0x01, 0)
    emit(0x01, len(flag))
    emit(0x0D)
    emit(0x01, verify_loop)
    emit(0x0F)
    
    success_msg = "Correct! Flag is valid!"
    for c in success_msg:
        emit(0x01, ord(c))
        emit(0x1B)
    emit(0x16)
    
    failure_msg = "Wrong! Try again."
    for c in failure_msg:
        emit(0x01, ord(c))
        emit(0x1B)
    emit(0x16)
    
    return bytes(bytecode)

def encrypt_bytecode(bytecode, key=0xDEADBEEF):
    encrypted = bytearray()
    for i, b in enumerate(bytecode):
        key_byte = (key >> (i % 4 * 8)) & 0xFF
        encrypted.append(b ^ key_byte)
    return bytes(encrypted)

def create_binary():
    bytecode = create_bytecode()
    encrypted_bytecode = encrypt_bytecode(bytecode)
    
    with open('bytecode.bin', 'wb') as f:
        f.write(encrypted_bytecode)
    
    print(f"[+] Bytecode saved: bytecode.bin")
    print(f"[+] Bytecode size: {len(encrypted_bytecode)} bytes")

def create_solve_script():
    solve_code = '''#!/usr/bin/env python3

import struct

def decrypt_bytecode(encrypted, key=0xDEADBEEF):
    decrypted = bytearray()
    for i, b in enumerate(encrypted):
        key_byte = (key >> (i % 4 * 8)) & 0xFF
        decrypted.append(b ^ key_byte)
    return bytes(decrypted)

def disassemble(bytecode):
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
    with open('bytecode.bin', 'rb') as f:
        encrypted = f.read()
    
    bytecode = decrypt_bytecode(encrypted)
    
    flag_chars = []
    i = 0
    
    while i < len(bytecode) and bytecode[i] == 0x17:
        i += 1
    
    while i < len(bytecode) - 8:
        if bytecode[i] == 0x01 and bytecode[i+5] == 0x01 and bytecode[i+10] == 0x12:
            encrypted_char = struct.unpack('<I', bytecode[i+1:i+5])[0]
            addr = struct.unpack('<I', bytecode[i+6:i+10])[0]
            
            char = encrypted_char ^ 0x42
            flag_chars.append((addr, chr(char)))
            
            i += 11
        else:
            i += 1
    
    flag_chars.sort()
    flag = ''.join(c for _, c in flag_chars)
    
    print(f"[+] Extracted flag: {flag}")
    return flag

if __name__ == '__main__':
    print("=" * 50)
    print("VM-Obfuscated RE - Solution")
    print("=" * 50)
    print()
    
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
    print("[*] Extracting flag from bytecode...")
    flag = extract_flag()
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

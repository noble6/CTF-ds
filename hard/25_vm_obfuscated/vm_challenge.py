#!/usr/bin/env python3

import struct
import sys
import time

OPCODES = {0x01: 'PUSH', 0x02: 'POP', 0x03: 'ADD', 0x07: 'XOR', 0x0D: 'CMP', 0x0E: 'JMP', 0x0F: 'JZ', 0x11: 'LOAD', 0x12: 'STORE', 0x16: 'HALT', 0x17: 'NOP', 0x18: 'DUP', 0x1A: 'INPUT', 0x1B: 'OUTPUT'}

class VM:
    def __init__(self):
        self.stack = []
        self.memory = [0] * 1024
        self.pc = 0
        self.running = False
        self.output = []
        self.flags = {'Z': False}
        self.debugger_detected = False
        self.last_time = time.time()
    
    def check_debug(self):
        current_time = time.time()
        if current_time - self.last_time > 0.1:
            self.debugger_detected = True
        self.last_time = current_time
    
    def push(self, val):
        self.stack.append(val & 0xFFFFFFFF)
    
    def pop(self):
        return self.stack.pop() if self.stack else 0
    
    def execute(self, bytecode, user_input=""):
        self.running = True
        self.pc = 0
        inp_pos = 0
        call_stack = []
        
        while self.running and self.pc < len(bytecode):
            self.check_debug()
            if self.debugger_detected:
                self.stack = [0] * len(self.stack)
            
            op = bytecode[self.pc]
            self.pc += 1
            
            if op == 0x01:
                val = struct.unpack('<I', bytecode[self.pc:self.pc+4])[0]
                self.pc += 4
                self.push(val)
            elif op == 0x02:
                self.pop()
            elif op == 0x03:
                b, a = self.pop(), self.pop()
                self.push(a + b)
            elif op == 0x07:
                b, a = self.pop(), self.pop()
                self.push(a ^ b)
            elif op == 0x0D:
                b, a = self.pop(), self.pop()
                self.flags['Z'] = (a == b)
            elif op == 0x0E:
                self.pc = struct.unpack('<I', bytecode[self.pc:self.pc+4])[0]
            elif op == 0x0F:
                target = struct.unpack('<I', bytecode[self.pc:self.pc+4])[0]
                if self.flags['Z']:
                    self.pc = target
                else:
                    self.pc += 4
            elif op == 0x11:
                addr = self.pop()
                self.push(self.memory[addr] if 0 <= addr < 1024 else 0)
            elif op == 0x12:
                addr = self.pop()
                val = self.pop()
                if 0 <= addr < 1024:
                    self.memory[addr] = val
            elif op == 0x16:
                self.running = False
            elif op == 0x17:
                pass
            elif op == 0x18:
                self.push(self.stack[-1] if self.stack else 0)
            elif op == 0x1A:
                if inp_pos < len(user_input):
                    self.push(ord(user_input[inp_pos]))
                    inp_pos += 1
                else:
                    self.push(0)
            elif op == 0x1B:
                self.output.append(chr(self.pop() & 0xFF))
        
        return ''.join(self.output)

def decrypt_bytecode(encrypted, key=0xDEADBEEF):
    return bytes([b ^ ((key >> (i % 4 * 8)) & 0xFF) for i, b in enumerate(encrypted)])

def main():
    print("=" * 50)
    print("  VM-Obfuscated RE Challenge")
    print("  College CTF 2026")
    print("=" * 50)
    
    with open('bytecode.bin', 'rb') as f:
        encrypted = f.read()
    
    bytecode = decrypt_bytecode(encrypted)
    vm = VM()
    
    flag = input("Enter flag: ")
    result = vm.execute(bytecode, flag)
    
    if result:
        print(result)
    else:
        print("No output produced.")

if __name__ == '__main__':
    main()

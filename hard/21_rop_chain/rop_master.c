/*
 * ROP Chain Master - College CTF 2026
 * Difficulty: HARD (1000 pts)
 *
 * Vulnerability: Stack buffer overflow with ASLR enabled
 * Goal: Get shell by building ROP chain to leak libc and call system()
 *
 * Compile:
 *   gcc -o rop_master rop_master.c -fno-stack-protector -no-pie -z norelro
 *   strip rop_master
 *   echo 2 > /proc/sys/kernel/randomize_va_space  # Ensure ASLR is on
 *
 * Binary is 64-bit, NX enabled, no canary, no PIE, ASLR on
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

// Compiled without PIE, so addresses are fixed
// GOT entries will be at known addresses
// But libc addresses are randomized (ASLR)

void vulnerable() {
    char buffer[64];
    printf("Enter your payload: ");
    fflush(stdout);
    
    // Vulnerable: reads way more than buffer size
    read(0, buffer, 256);  // Can overflow 64 bytes by 192 more!
}

void gadgets() {
    // These are "gadgets" that exist in the binary
    // Players need to find these via ROPgadget or ropper
    asm("pop rdi; ret");      // Gadget 1: pop rdi; ret
    asm("pop rsi; ret");      // Gadget 2: pop rsi; ret  
    asm("pop rdx; ret");      // Gadget 3: pop rdx; ret
    asm("ret");                // Gadget 4: just ret (for alignment)
}

// This function is never called directly, but its address is useful
void win() {
    system("/bin/sh");
}

int main() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    
    puts("========================================");
    puts("  ROP Chain Master - College CTF 2026");
    puts("========================================");
    puts("");
    puts("Goal: Execute system(\"/bin/sh\")");
    puts("Hint: NX is enabled, ASLR is on, no canary");
    puts("Hint: You need to leak a libc address first");
    puts("");
    
    vulnerable();
    
    puts("Goodbye!");
    return 0;
}

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

void vulnerable() {
    char buffer[64];
    printf("Enter your payload: ");
    fflush(stdout);
    read(0, buffer, 256);
}

void gadgets() {
    asm("pop rdi; ret");
    asm("pop rsi; ret");
    asm("pop rdx; ret");
    asm("ret");
}

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

#!/usr/bin/env python3
"""
Buffer Overflow Challenge - C Source Code
Compile: gcc -o challenge challenge.c -fno-stack-protector -no-pie -z execstack
"""

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// Hidden function that prints the flag
void win() {
    printf("flag{buffer_overflow_overwrites_variables}\n");
}

// Vulnerable function
void vulnerable() {
    int authorized = 0;
    char buffer[64];
    
    printf("Enter your name: ");
    gets(buffer);  // VULNERABLE! No bounds checking
    
    printf("Hello, %s!\n", buffer);
    
    if (authorized) {
        printf("Access granted!\n");
        win();
    } else {
        printf("Access denied. authorized = %d\n", authorized);
    }
}

int main() {
    printf("=== Buffer Overflow Challenge ===\n");
    printf("Can you overflow the buffer to change 'authorized'?\n\n");
    vulnerable();
    return 0;
}

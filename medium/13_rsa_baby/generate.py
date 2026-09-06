#!/usr/bin/env python3
"""
RSA Baby Challenge - Generate RSA parameters with small primes
"""

import random
from sympy import isprime, nextprime

def generate_small_rsa():
    """Generate RSA with small primes (factorable)"""
    # Small primes that can be factored
    p = 1000000007  # 10^9 + 7 (well-known prime)
    q = 1000000009  # 10^9 + 9 (well-known prime)
    
    n = p * q
    e = 65537  # Common public exponent
    
    # Calculate phi(n)
    phi = (p - 1) * (q - 1)
    
    # Calculate private key d
    d = pow(e, -1, phi)
    
    # Encrypt flag
    flag = "flag{rsa_with_small_primes_is_weak}"
    flag_int = int.from_bytes(flag.encode(), 'big')
    
    # Ensure flag_int < n
    if flag_int >= n:
        raise ValueError("Flag too large for RSA modulus")
    
    ciphertext = pow(flag_int, e, n)
    
    return {
        'n': n,
        'e': e,
        'ciphertext': ciphertext,
        'p': p,  # Don't reveal this!
        'q': q,  # Don't reveal this!
        'd': d   # Don't reveal this!
    }

if __name__ == '__main__':
    rsa = generate_small_rsa()
    print(f"n = {rsa['n']}")
    print(f"e = {rsa['e']}")
    print(f"ciphertext = {rsa['ciphertext']}")
    print(f"\n--- FOR ADMIN ONLY ---")
    print(f"p = {rsa['p']}")
    print(f"q = {rsa['q']}")
    print(f"d = {rsa['d']}")

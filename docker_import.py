#!/usr/bin/env python3

from CTFd import create_app
from CTFd.models import db, Challenges, Flags, Hints
from CTFd.utils import set_config

CHALLENGES = [
    {"name": "Welcome", "category": "Misc", "description": "Welcome to the College CTF! This is your first challenge.\nSometimes the flag is right in front of you...\n\nHint: Read the description carefully.", "value": 100, "flag": "flag{welcome_to_college_ctf_2026}", "hints": ["Read the challenge description very carefully. Sometimes the answer is hiding in plain sight."]},
    {"name": "Base What?", "category": "Crypto", "description": "I found this encoded message, but I can't read it. Can you decode it?\n\nZmxhZ3tiYXNlNjRfaXNfdGhlX2ZpcnN0X3RoaW5nX3lvdV9sZWFybn0=", "value": 100, "flag": "flag{base64_is_the_first_thing_you_learn}", "hints": ["This encoding is very common on the web. It uses A-Z, a-z, 0-9, +, and / characters.", "Try searching for 'base64 decode' online."]},
    {"name": "Inspect Me", "category": "Web", "description": "There's something hidden on this webpage. Can you find it?\n\nhttp://192.168.31.217:5001", "value": 100, "flag": "flag{inspect_element_is_your_friend}", "hints": ["Right-click on the page and look for 'Inspect' or 'View Page Source'.", "Check the HTML comments. They sometimes hide secrets."]},
    {"name": "Hex Dump", "category": "Crypto", "description": "I intercepted this message, but it looks like gibberish. What format is this?\n\n66 6c 61 67 7b 68 65 78 5f 69 73 5f 63 6f 6f 6c 5f 72 69 67 68 74 7d", "value": 150, "flag": "flag{hex_is_cool_right}", "hints": ["Each pair of characters represents one letter in ASCII.", "66 = 'f', 6c = 'l', 61 = 'a', 67 = 'g'... see the pattern?"]},
    {"name": "Cookie Monster", "category": "Web", "description": "I made a login system, but only admins can see the flag. Can you become an admin?\n\nhttp://192.168.31.217:5002", "value": 150, "flag": "flag{cookies_can_be_modified_by_users}", "hints": ["Open Developer Tools (F12) and look at the Application/Storage tab.", "There's a cookie called 'role'. What happens if you change its value?"]},
    {"name": "Caesar's Secret", "category": "Crypto", "description": "Julius Caesar used to encrypt his messages this way. Can you decrypt it?\n\nsynt{pnpghzr_frpnyr_gjb_gjb_a}", "value": 150, "flag": "flag{caesar_secret_scale_two_two_n}", "hints": ["Julius Caesar used a simple substitution cipher. Each letter is shifted by a fixed amount.", "ROT13 is a Caesar cipher with shift 13. Apply it again to decrypt."]},
    {"name": "File Type", "category": "Forensics", "description": "I have a file, but my computer says it's corrupted. Can you figure out what's wrong?\n\n[Download mystery_file.bin]", "value": 150, "flag": "flag{file_extensions_are_just_labels}", "hints": ["File extensions are just labels. The actual file format is determined by magic bytes.", "Try opening the file in a hex editor or use the 'file' command."]},
    {"name": "Hidden Message", "category": "Forensics", "description": "There's a secret message hidden in this file. Can you find it?\n\n[Download hidden_message.txt]", "value": 200, "flag": "flag{hidden_in_plain_text}", "hints": ["Sometimes secrets are hidden among lots of noise.", "Use the 'strings' command or grep for 'flag{'."]},
    {"name": "ROT13", "category": "Crypto", "description": "Can you decode this message?\n\nsynt{ebg13_vf_n_puvyqref_pvcure}", "value": 100, "flag": "flag{rot13_is_a_childrens_cipher}", "hints": ["ROT13 rotates each letter by 13 positions. A becomes N, B becomes O, etc."]},
    {"name": "SQL Rookie", "category": "Web", "description": "I made a login page. Can you bypass it and get the flag?\n\nhttp://192.168.31.217:5003", "value": 200, "flag": "flag{sql_injection_is_easy_admin}", "hints": ["Think about how SQL queries work. What happens if you add special characters?", "The -- in SQL makes the rest of the line a comment.", "Try: admin' -- as the username with any password."]},
    {"name": "Stego Master", "category": "Forensics", "description": "There are MULTIPLE secrets hidden in this image using different techniques. Can you find ALL of them?\n\n[Download stego_master.png]\n\nHint: LSB, EXIF metadata, file carving, and password-protected layers!", "value": 350, "flag": "flag{multi_layer_steganography_master}", "hints": ["Images can hide data in their pixels or metadata.", "Try using steghide or an online steganography tool.", "The password might be something simple and common."]},
    {"name": "JWT Nightmare", "category": "Web", "description": "I implemented JWT with RS256 algorithm. But I heard algorithm confusion attacks can bypass this...\n\nhttp://192.168.31.217:5004\n\nHint: Change RS256 to HS256 and use the public key as HMAC secret!", "value": 400, "flag": "flag{jwt_algorithm_confusion_attack}", "hints": ["JWT tokens have 3 parts: header.payload.signature", "Decode the JWT at jwt.io. What's in the payload?", "The secret key is very weak. Try common secrets."]},
    {"name": "RSA Evolution", "category": "Crypto", "description": "I encrypted the flag using RSA with unconventional parameters. Can you break it?\n\nVariant A: Wiener's attack (small d)\nVariant B: Multi-prime RSA (N = p*q*r)\nVariant C: Common modulus attack\n\n[Download challenge files]", "value": 400, "flag": "flag{rsa_unconventional_attacks}", "hints": ["RSA security relies on the difficulty of factoring N into p and q.", "This N is small. Try factoring it or searching for the primes.", "p = 1000000007, q = 1000000009. These are well-known primes!"]},
    {"name": "Filter Bypass", "category": "Web", "description": "I added MULTIPLE filters to prevent path traversal. But can you bypass ALL of them?\n\nhttp://192.168.31.217:5005\n\nFilters: ../ blocked, URL encoding blocked, null bytes blocked, normalization applied.\n\nHint: Double encoding, UTF-8 overlong, path truncation!", "value": 400, "flag": "flag{filter_bypass_all_layers}", "hints": ["What happens if you use ../ in the filename?", "Try: ../private/flag.txt"]},
    {"name": "DOM XSS + CSP Bypass", "category": "Web", "description": "This website has Content Security Policy (CSP) protection. But can you still execute DOM-based XSS?\n\nhttp://192.168.31.217:5006\n\nHint: Look for DOM sinks (innerHTML, eval). CSP allows 'unsafe-inline'!", "value": 400, "flag": "flag{dom_xss_csp_bypass}", "hints": ["XSS means injecting JavaScript into a webpage.", "Try putting <script>alert('test')</script> in the search box."]},
    {"name": "Network Forensics", "category": "Forensics", "description": "I captured encrypted network traffic. I also have the TLS key from memory. Can you decrypt and analyze?\n\n[Download traffic.pcap and key.pem]\n\nHint: Use Wireshark TLS decryption, check DNS queries, look for exfiltrated data!", "value": 450, "flag": "flag{network_forensics_encrypted_traffic}", "hints": ["Open the pcap file in Wireshark and look at the HTTP traffic.", "Filter by 'http' and look at the request parameters."]},
    {"name": "Cipher Chain", "category": "Crypto", "description": "I encrypted the flag using MULTIPLE cipher layers: Vigenere -> ROT13 -> Reverse -> Atbash. Can you peel back all the layers?\n\nCiphertext: Jx#5k9@p2m!Qw8^z\n\nHint: Decrypt in REVERSE order. Key for Vigenere: 'college'", "value": 350, "flag": "flag{cipher_chain_multiple_layers}", "hints": ["The Vigenere cipher uses a keyword to shift each letter by different amounts.", "The key is related to this CTF event. What's the venue?"]},
    {"name": "Race Condition + IDOR", "category": "Web", "description": "This API has IDOR AND race condition vulnerabilities. Can you exploit both?\n\nhttp://192.168.31.217:5007\n\nHint: Access admin profile via IDOR, exploit race condition for balance manipulation!", "value": 400, "flag": "flag{race_condition_idor_chain}", "hints": ["IDOR stands for Insecure Direct Object Reference.", "Look at the URL parameters. Can you change the user_id?"]},
    {"name": "Anti-RE", "category": "Reverse", "description": "This binary uses advanced obfuscation: control flow flattening, opaque predicates, string encryption, and anti-debug. Can you reverse it?\n\n[Download anti_re_binary]\n\nHint: Use Ghidra/IDA for static analysis, or dynamic analysis with GDB. Consider angr for symbolic execution!", "value": 450, "flag": "flag{anti_re_obfuscation_bypass}", "hints": ["The flag is obfuscated, not absent. Look for patterns in the binary.", "Try a hex editor. Look for XOR patterns."]},
    {"name": "Hash Cracking", "category": "Crypto", "description": "I stored passwords using SHA-256 with a salt. But my implementation might be flawed...\n\nadmin:5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8\nuser1:a3f8b2e5c1d7a9f4e6b0c2d8a1f3e5b7c9d2a4f6e8b0c1d3a5f7e9b1c3d5a7\n\nHint: Try CrackStation, hashcat, or John the Ripper!", "value": 400, "flag": "flag{sha256_weak_implementation}", "hints": ["MD5 is a hashing algorithm. Try to find what was hashed.", "Use an online MD5 cracker or hashcat.", "The password is something you'd find at this event."]},
    {"name": "ROP Chain Master", "category": "Pwn", "description": "I compiled this binary with security features (NX, ASLR), but no stack canary. Can you build a ROP chain to get a shell?\n\n[Download rop_master binary]\n\nHint: First leak a libc address, then call system('/bin/sh')", "value": 1000, "flag": "flag{rop_chain_aslr_bypass_master}", "hints": ["First, find the buffer overflow vulnerability", "You need to leak a libc address to bypass ASLR", "Use ROP gadgets from the binary to call puts(puts@GOT)", "Calculate libc base from the leak", "Build final ROP chain to call system('/bin/sh')"]},
    {"name": "Heap Roulette", "category": "Pwn", "description": "This heap manager has multiple vulnerabilities. Can you exploit Use-After-Free and tcache poisoning to overwrite __free_hook?\n\nnc 192.168.31.217 1337\n\nHint: View freed chunks to leak addresses, then poison tcache.", "value": 1000, "flag": "flag{tcache_poisoning_free_hook}", "hints": ["Use-After-Free: delete doesn't zero the pointer", "View freed chunks to leak heap/libc addresses", "Tcache poisoning: overwrite fd to target address"]},
    {"name": "Bleichenbacher's Revenge", "category": "Crypto", "description": "I encrypted the flag using RSA PKCS#1 v1.5. The decryption oracle returns detailed error messages. Can you implement Bleichenbacher's attack?\n\nhttp://192.168.31.217:5010\n\nHint: ~1 million queries needed. The oracle distinguishes padding errors.", "value": 1000, "flag": "flag{bleichenbacher_padding_oracle_rsa}", "hints": ["This is PKCS#1 v1.5 padding (not OAEP)", "The oracle gives DETAILED error messages", "Bleichenbacher's 1998 attack uses ~1 million queries", "Implement the adaptive chosen-ciphertext attack", "Key insight: Valid padding starts with 0x00 0x02"]},
    {"name": "Volatility Master", "category": "Forensics", "description": "I captured a memory dump with advanced anti-forensics: process hollowing, XOR encryption, DNS tunneling, and more. Find ALL hidden flags!\n\n[Download memory_dump.raw (50MB)]\n\nHint: Try multiple decoding techniques - plaintext, XOR, Base64, UTF-16.", "value": 900, "flag": "flag{v0l4t1l1ty_m4st3r_4dv4nc3d_f0r3ns1cs}", "hints": ["Start with strings | grep flag - you'll find some immediately", "The XOR key is always a single byte (0-255)", "Look for HTTP requests containing encoded data", "Windows uses UTF-16 for many strings", "Check JSON structures for configuration data"]},
    {"name": "VM-Obfuscated RE", "category": "Reverse", "description": "The flag is protected by a custom virtual machine with encrypted bytecode and anti-debug features. Reverse engineer the VM to extract the flag.\n\n[Download vm_challenge.py and bytecode.bin]\n\nHint: The bytecode is XOR encrypted with 0xDEADBEEF. Flag chars stored with XOR 0x42.", "value": 1000, "flag": "flag{vm_0bfu5c4t10n_r3v3r51ng}", "hints": ["The bytecode is XOR encrypted with a 4-byte key", "The flag is stored character by character, XOR'd with 0x42", "Look for patterns: PUSH, PUSH, STORE (repeated for each char)", "Anti-debug can be bypassed by patching timing checks", "Write a disassembler - it will make the challenge much easier"]}
]

def main():
    app = create_app()
    
    with app.app_context():
        print("[*] Importing challenges...")
        
        for ch_data in CHALLENGES:
            ch = Challenges(
                name=ch_data['name'],
                category=ch_data['category'],
                description=ch_data['description'],
                value=ch_data['value'],
                type='standard',
                state='visible'
            )
            db.session.add(ch)
            db.session.flush()
            
            flag = Flags(
                challenge_id=ch.id,
                content=ch_data['flag'],
                type='static'
            )
            db.session.add(flag)
            
            for i, hint_text in enumerate(ch_data.get('hints', [])):
                cost = 0 if i == 0 else (i * 25)
                hint = Hints(
                    challenge_id=ch.id,
                    content=hint_text,
                    cost=cost
                )
                db.session.add(hint)
            
            print(f"  [+] {ch_data['name']} ({ch_data['value']} pts)")
        
        db.session.commit()
        
        print(f"\n[+] Imported {len(CHALLENGES)} challenges!")
        print("[*] Access at: http://192.168.31.217:8000")

if __name__ == '__main__':
    main()

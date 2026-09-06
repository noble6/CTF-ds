#!/usr/bin/env python3
"""
CTFd Challenge Import Script
Imports all challenges into CTFd via API

Usage: python3 import_challenges.py --url http://localhost:8000 --token YOUR_API_TOKEN
"""

import requests
import json
import os
import sys
import argparse
from pathlib import Path

# Import hint configuration
sys.path.insert(0, str(Path(__file__).parent))
from hint_config import get_hints_for_challenge

# Challenge definitions
CHALLENGES = {
    "easy": [
        {
            "name": "Welcome",
            "category": "Misc",
            "description": "Welcome to the College CTF! This is your first challenge.\nSometimes the flag is right in front of you...\n\nHint: Read the description carefully.",
            "value": 100,
            "flag": "flag{welcome_to_college_ctf_2026}",
            "type": "static"
        },
        {
            "name": "Base What?",
            "category": "Crypto",
            "description": "I found this encoded message, but I can't read it. Can you decode it?\n\nZmxhZ3tiYXNlNjRfaXNfdGhlX2ZpcnN0X3RoaW5nX3lvdV9sZWFybn0=",
            "value": 100,
            "flag": "flag{base64_is_the_first_thing_you_learn}",
            "type": "static"
        },
        {
            "name": "Inspect Me",
            "category": "Web",
            "description": "There's something hidden on this webpage. Can you find it?\n\nhttp://YOUR_SERVER:5001",
            "value": 100,
            "flag": "flag{inspect_element_is_your_friend}",
            "type": "static"
        },
        {
            "name": "Hex Dump",
            "category": "Crypto",
            "description": "I intercepted this message, but it looks like gibberish. What format is this?\n\n66 6c 61 67 7b 68 65 78 5f 69 73 5f 63 6f 6f 6c 5f 72 69 67 68 74 7d",
            "value": 150,
            "flag": "flag{hex_is_cool_right}",
            "type": "static"
        },
        {
            "name": "Cookie Monster",
            "category": "Web",
            "description": "I made a login system, but only admins can see the flag. Can you become an admin?\n\nhttp://YOUR_SERVER:5002",
            "value": 150,
            "flag": "flag{cookies_can_be_modified_by_users}",
            "type": "static"
        },
        {
            "name": "Caesar's Secret",
            "category": "Crypto",
            "description": "Julius Caesar used to encrypt his messages this way. Can you decrypt it?\n\nsynt{pnpghzr_frpnyr_gjb_gjb_a}",
            "value": 150,
            "flag": "flag{caesar_secret_scale_two_two_n}",
            "type": "static"
        },
        {
            "name": "File Type",
            "category": "Forensics",
            "description": "I have a file, but my computer says it's corrupted. Can you figure out what's wrong?\n\n[Download mystery_file.bin]",
            "value": 150,
            "flag": "flag{file_extensions_are_just_labels}",
            "type": "static"
        },
        {
            "name": "Hidden Message",
            "category": "Forensics",
            "description": "There's a secret message hidden in this file. Can you find it?\n\n[Download hidden_message.txt]",
            "value": 200,
            "flag": "flag{hidden_in_plain_text}",
            "type": "static"
        },
        {
            "name": "ROT13",
            "category": "Crypto",
            "description": "Can you decode this message?\n\nsynt{ebg13_vf_n_puvyqref_pvcure}",
            "value": 100,
            "flag": "flag{rot13_is_a_childrens_cipher}",
            "type": "static"
        },
        {
            "name": "SQL Rookie",
            "category": "Web",
            "description": "I made a login page. Can you bypass it and get the flag?\n\nhttp://YOUR_SERVER:5003",
            "value": 200,
            "flag": "flag{sql_injection_is_easy_admin}",
            "type": "static"
        }
    ],
    "medium": [
        {
            "name": "Stego 101",
            "category": "Forensics",
            "description": "There's something hidden in this image. Can you extract the secret?\n\n[Download stego_image.png]",
            "value": 300,
            "flag": "flag{steganography_hides_in_pixels}",
            "type": "static"
        },
        {
            "name": "Broken Auth",
            "category": "Web",
            "description": "I implemented JWT authentication, but something seems off. Can you forge a token and get the flag?\n\nhttp://YOUR_SERVER:5004",
            "value": 350,
            "flag": "flag{jwt_tokens_can_be_decoded_and_modified}",
            "type": "static"
        },
        {
            "name": "RSA Baby",
            "category": "Crypto",
            "description": "I encrypted the flag using RSA, but I think I made a mistake. Can you decrypt it?\n\nn = 1000000016000000063\ne = 65537\nciphertext = 32733159860069353218860496061234567890",
            "value": 350,
            "flag": "flag{rsa_with_small_primes_is_weak}",
            "type": "static"
        },
        {
            "name": "Path Traversal",
            "category": "Web",
            "description": "This file viewer lets you read files from the server. But can you read files you're not supposed to access?\n\nhttp://YOUR_SERVER:5005",
            "value": 350,
            "flag": "flag{path_traversal_reads_sensitive_files}",
            "type": "static"
        },
        {
            "name": "XSS Reflected",
            "category": "Web",
            "description": "This search page seems vulnerable. Can you exploit it to get the flag?\n\nhttp://YOUR_SERVER:5006",
            "value": 300,
            "flag": "flag{xss_can_execute_arbitrary_javascript}",
            "type": "static"
        },
        {
            "name": "Pcap Analysis",
            "category": "Forensics",
            "description": "I captured some network traffic, but I can't find the secret data. Can you analyze this pcap file and extract the flag?\n\n[Download network_traffic.pcap]",
            "value": 400,
            "flag": "flag{network_traffic_reveals_secrets}",
            "type": "static"
        },
        {
            "name": "Vigenere",
            "category": "Crypto",
            "description": "I encrypted the flag using a Vigenere cipher with a key related to this CTF event. Can you decrypt it?\n\nEncrypted: qygv{vieeeme_cipher_vlgc_ieorw_xey}\n\nHint: The key is something you'd find at a college CTF event.",
            "value": 300,
            "flag": "flag{vigenere_cipher_with_known_key}",
            "type": "static"
        },
        {
            "name": "IDOR",
            "category": "Web",
            "description": "This website lets you view user profiles. But can you access other users' private data?\n\nhttp://YOUR_SERVER:5007",
            "value": 350,
            "flag": "flag{idor_exposes_other_users_data}",
            "type": "static"
        },
        {
            "name": "Strings++",
            "category": "Reverse",
            "description": "I found this binary, but `strings` command doesn't show anything useful. Can you reverse engineer it and find the hidden flag?\n\n[Download challenge.bin]",
            "value": 400,
            "flag": "flag{strings_command_wont_find_this}",
            "type": "static"
        },
        {
            "name": "Weak Hash",
            "category": "Crypto",
            "description": "I hashed a password using MD5, but I think it's not secure enough. Can you crack it?\n\nMD5 Hash: d93a5def163fd0788975da8d77626dea\n\nHint: The password is related to this CTF event.",
            "value": 400,
            "flag": "flag{md5_is_not_secure_for_passwords}",
            "type": "static"
        }
    ],
    "hard": [
        {
            "name": "SSRF Master",
            "category": "Web",
            "description": "This URL fetcher service lets you fetch any webpage. But there's a secret internal service running. Can you access it?\n\nhttp://YOUR_SERVER:5008\n\nHint: There's a secret internal service running on localhost:9999",
            "value": 600,
            "flag": "flag{ssrf_can_access_internal_services}",
            "type": "static"
        },
        {
            "name": "Padding Oracle",
            "category": "Crypto",
            "description": "This service encrypts and decrypts messages using AES-CBC. But there's a vulnerability in how it handles padding errors. Can you exploit it to decrypt the flag?\n\nhttp://YOUR_SERVER:5009",
            "value": 700,
            "flag": "flag{padding_oracle_attack_on_cbc}",
            "type": "static"
        },
        {
            "name": "Buffer Overflow",
            "category": "Pwn",
            "description": "This program has a vulnerable function. Can you exploit it to get the flag?\n\n[Download challenge binary]\n\nHint: The 'authorized' variable needs to be changed.",
            "value": 800,
            "flag": "flag{buffer_overflow_overwrites_variables}",
            "type": "static"
        },
        {
            "name": "Memory Forensics",
            "category": "Forensics",
            "description": "I captured a memory dump from a compromised system. Can you analyze it and find the hidden flag?\n\n[Download memory_dump.raw]",
            "value": 600,
            "flag": "flag{memory_forensics_reveals_secrets}",
            "type": "static"
        },
        {
            "name": "Obfuscated RE",
            "category": "Reverse",
            "description": "I found this binary, but it's heavily obfuscated. Can you reverse engineer it and extract the hidden flag?\n\n[Download obfuscated_challenge]",
            "value": 700,
            "flag": "flag{obfuscation_makes_reverse_engineering_hard}",
            "type": "static"
        }
    ]
}

class CTFdImporter:
    def __init__(self, url, token):
        self.url = url.rstrip('/')
        self.headers = {
            'Authorization': f'Token {token}',
            'Content-Type': 'application/json'
        }
    
    def create_challenge(self, challenge_data):
        """Create a challenge in CTFd"""
        payload = {
            'name': challenge_data['name'],
            'category': challenge_data['category'],
            'description': challenge_data['description'],
            'value': challenge_data['value'],
            'type': challenge_data.get('type', 'static'),
            'state': 'visible'
        }
        
        response = requests.post(
            f'{self.url}/api/v1/challenges',
            headers=self.headers,
            json=payload
        )
        
        if response.status_code == 200:
            return response.json()['data']
        else:
            print(f"Error creating challenge {challenge_data['name']}: {response.text}")
            return None
    
    def add_flag(self, challenge_id, flag_content):
        """Add a flag to a challenge"""
        payload = {
            'challenge_id': challenge_id,
            'content': flag_content,
            'type': 'static'
        }
        
        response = requests.post(
            f'{self.url}/api/v1/flags',
            headers=self.headers,
            json=payload
        )
        
        if response.status_code == 200:
            return response.json()['data']
        else:
            print(f"Error adding flag: {response.text}")
            return None
    
    def add_hint(self, challenge_id, hint_content, cost=0):
        """Add a hint to a challenge"""
        payload = {
            'challenge_id': challenge_id,
            'content': hint_content,
            'cost': cost,
            'type': 'standard'
        }
        
        response = requests.post(
            f'{self.url}/api/v1/hints',
            headers=self.headers,
            json=payload
        )
        
        if response.status_code == 200:
            return response.json()['data']
        else:
            print(f"Error adding hint: {response.text}")
            return None
    
    def import_hints(self, challenge_id, challenge_name):
        """Import all hints for a challenge"""
        hints = get_hints_for_challenge(challenge_name)
        
        if not hints:
            return
        
        for hint in hints:
            self.add_hint(challenge_id, hint['content'], hint['cost'])
    
    def import_all(self):
        """Import all challenges"""
        total = sum(len(challenges) for challenges in CHALLENGES.values())
        imported = 0
        hints_added = 0
        
        print(f"Importing {total} challenges...")
        print("=" * 50)
        
        for difficulty, challenges in CHALLENGES.items():
            print(f"\n{difficulty.upper()} CHALLENGES:")
            print("-" * 30)
            
            for challenge in challenges:
                # Create challenge
                result = self.create_challenge(challenge)
                
                if result:
                    # Add flag
                    self.add_flag(result['id'], challenge['flag'])
                    
                    # Add hints
                    hints = get_hints_for_challenge(challenge['name'])
                    if hints:
                        self.import_hints(result['id'], challenge['name'])
                        hints_added += len(hints)
                    
                    imported += 1
                    hint_info = f" + {len(hints)} hints" if hints else ""
                    print(f"✓ {challenge['name']} ({challenge['value']} pts{hint_info})")
                else:
                    print(f"✗ {challenge['name']} - FAILED")
        
        print("\n" + "=" * 50)
        print(f"Imported {imported}/{total} challenges with {hints_added} hints!")
        print("\nScoring Features:")
        print("  • First Blood: +10% bonus for first solver")
        print("  • Critical: +5% bonus for last 30 minutes")
        print("  • Hints: Available with point costs")

def main():
    parser = argparse.ArgumentParser(description='Import CTF challenges into CTFd')
    parser.add_argument('--url', required=True, help='CTFd URL (e.g., http://localhost:8000)')
    parser.add_argument('--token', required=True, help='CTFd API token')
    
    args = parser.parse_args()
    
    importer = CTFdImporter(args.url, args.token)
    importer.import_all()

if __name__ == '__main__':
    main()

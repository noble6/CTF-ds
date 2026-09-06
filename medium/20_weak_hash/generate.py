#!/usr/bin/env python3
"""
Weak Hash Challenge - Generate MD5 hash of common password
"""

import hashlib

def generate_weak_hash():
    """Generate MD5 hash of a common password"""
    
    # Common passwords list
    common_passwords = [
        "password", "123456", "qwerty", "admin", "letmein",
        "welcome", "monkey", "dragon", "master", "college",
        "football", "shadow", "michael", "hello", "charlie"
    ]
    
    # Pick a password (college-related)
    password = "college"
    
    # Generate MD5 hash
    md5_hash = hashlib.md5(password.encode()).hexdigest()
    
    print(f"Password: {password}")
    print(f"MD5 Hash: {md5_hash}")
    
    return password, md5_hash

def crack_hash(hash_to_crack):
    """Crack MD5 hash using dictionary attack"""
    
    common_passwords = [
        "password", "123456", "qwerty", "admin", "letmein",
        "welcome", "monkey", "dragon", "master", "college",
        "football", "shadow", "michael", "hello", "charlie",
        "abc123", "mustang", "access", "superman", "batman",
        "trustno1", "iloveyou", "sunshine", "princess", "starwars"
    ]
    
    for password in common_passwords:
        if hashlib.md5(password.encode()).hexdigest() == hash_to_crack:
            return password
    
    return None

if __name__ == '__main__':
    password, hash_value = generate_weak_hash()
    
    print("\n--- Cracking Demo ---")
    cracked = crack_hash(hash_value)
    if cracked:
        print(f"Cracked! Password: {cracked}")
    else:
        print("Failed to crack")

#!/usr/bin/env python3
"""
Vigenere Cipher Challenge Generator
"""

def vigenere_encrypt(plaintext, key):
    """Encrypt plaintext using Vigenere cipher"""
    encrypted = []
    key_length = len(key)
    key_index = 0
    
    for char in plaintext:
        if char.isalpha():
            # Determine shift based on key character
            key_char = key[key_index % key_length]
            shift = ord(key_char.lower()) - ord('a')
            
            if char.isupper():
                encrypted_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            else:
                encrypted_char = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            
            encrypted.append(encrypted_char)
            key_index += 1
        else:
            encrypted.append(char)
    
    return ''.join(encrypted)

def vigenere_decrypt(ciphertext, key):
    """Decrypt ciphertext using Vigenere cipher"""
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

if __name__ == '__main__':
    flag = "flag{vigenere_cipher_with_known_key}"
    key = "college"
    
    encrypted = vigenere_encrypt(flag, key)
    print(f"Encrypted: {encrypted}")
    print(f"Key (for admin): {key}")
    
    # Verify decryption
    decrypted = vigenere_decrypt(encrypted, key)
    print(f"Decrypted: {decrypted}")

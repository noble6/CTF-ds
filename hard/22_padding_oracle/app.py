#!/usr/bin/env python3
"""
Padding Oracle Attack Challenge
Demonstrates CBC padding oracle vulnerability
"""

import os
import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Generate a random key (in real CTF, this would be fixed)
KEY = os.urandom(16)
IV = os.urandom(16)

HTML = """
<!DOCTYPE html>
<html>
<head><title>Padding Oracle</title></head>
<body>
    <h1>Encrypted Message Service</h1>
    
    <h2>Get Encrypted Flag</h2>
    <form id="encryptForm">
        <button type="submit">Get Encrypted Flag</button>
    </form>
    
    <h2>Decrypt Message</h2>
    <form id="decryptForm">
        <textarea name="ciphertext" rows="3" cols="60" placeholder="Enter hex-encoded ciphertext"></textarea><br>
        <textarea name="iv" rows="2" cols="60" placeholder="Enter hex-encoded IV"></textarea><br>
        <button type="submit">Decrypt</button>
    </form>
    
    <div id="result"></div>
    
    <h3>Hint:</h3>
    <p>The server tells you if padding is valid or not...</p>
    <p>Use this oracle to decrypt the flag!</p>

    <script>
    document.getElementById('encryptForm').onsubmit = async (e) => {
        e.preventDefault();
        const res = await fetch('/encrypt');
        const data = await res.json();
        document.getElementById('result').innerHTML = 
            '<h3>Encrypted Flag:</h3>' +
            '<p><b>Ciphertext:</b> ' + data.ciphertext + '</p>' +
            '<p><b>IV:</b> ' + data.iv + '</p>';
    };
    
    document.getElementById('decryptForm').onsubmit = async (e) => {
        e.preventDefault();
        const form = e.target;
        const ciphertext = form.ciphertext.value;
        const iv = form.iv.value;
        const res = await fetch('/decrypt', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ciphertext, iv})
        });
        const data = await res.json();
        document.getElementById('result').innerHTML = '<p>' + data.message + '</p>';
    };
    </script>
</body>
</html>
"""

def encrypt_flag():
    """Encrypt the flag"""
    flag = b"flag{padding_oracle_attack_on_cbc}"
    
    # Pad the flag
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(flag) + padder.finalize()
    
    # Encrypt
    cipher = Cipher(algorithms.AES(KEY), modes.CBC(IV), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    
    return ciphertext, IV

def decrypt_and_check(ciphertext_bytes, iv_bytes):
    """Decrypt and check padding - VULNERABLE!"""
    try:
        cipher = Cipher(algorithms.AES(KEY), modes.CBC(iv_bytes), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted = decryptor.update(ciphertext_bytes) + decryptor.finalize()
        
        # Try to unpad
        unpadder = padding.PKCS7(128).unpadder()
        unpadded = unpadder.update(decrypted) + unpadder.finalize()
        
        return True, unpadded.decode('utf-8', errors='ignore')
    except Exception as e:
        # Padding error - this is the oracle!
        return False, str(e)

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/encrypt')
def encrypt():
    ciphertext, iv = encrypt_flag()
    return jsonify({
        'ciphertext': ciphertext.hex(),
        'iv': iv.hex()
    })

@app.route('/decrypt', methods=['POST'])
def decrypt():
    data = request.get_json()
    
    try:
        ciphertext = bytes.fromhex(data.get('ciphertext', ''))
        iv = bytes.fromhex(data.get('iv', ''))
        
        valid, result = decrypt_and_check(ciphertext, iv)
        
        if valid:
            return jsonify({
                'status': 'success',
                'message': f'Decryption successful: {result}'
            })
        else:
            # VULNERABLE: Distinguishes between padding error and other errors
            if 'padding' in result.lower() or 'invalid' in result.lower():
                return jsonify({
                    'status': 'error',
                    'message': 'INVALID PADDING - Decryption failed'
                })
            else:
                return jsonify({
                    'status': 'error',
                    'message': 'Decryption failed (other error)'
                })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Invalid input: {str(e)}'
        })

if __name__ == '__main__':
    app.run(port=5008)

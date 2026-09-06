#!/usr/bin/env python3
"""
Bleichenbacher's Revenge - College CTF 2026
Difficulty: HARD (1000 pts)

Implementation of RSA PKCS#1 v1.5 with padding oracle vulnerability.

The server:
1. Encrypts a flag with RSA PKCS#1 v1.5
2. Provides decryption oracle (but with different error messages)
3. Player must implement Bleichenbacher's attack to decrypt

This is NOT just a simple padding oracle - it requires implementing
the actual Bleichenbacher's million-message attack.
"""

from Crypto.PublicKey import RSA
from Crypto.Util.number import bytes_to_long, long_to_bytes
import hashlib
import os
import json
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Generate RSA key (small enough to be factored if desperate, but attack is faster)
KEY_SIZE = 1024

# Use pre-generated keys for consistency
# In production, generate fresh keys
P = 0xf5a5fd42d16a2030291c94b9b86d11da2da5b257f65aec7fa476593db4afb4f3 * 1000000007 % (2**512)
Q = 0xd4749e6ce2b1fe3f4a7d3e65b0df39cd36576e1b3f0e75c2946789abcdef0123 * 1000000009 % (2**512)

# Actually, let's use proper primes
from sympy import nextprime, isprime
import random

random.seed(42)  # Fixed seed for reproducibility
P = nextprime(random.getrandbits(512))
Q = nextprime(random.getrandbits(512))
N = P * Q
E = 65537
PHI = (P - 1) * (Q - 1)
D = pow(E, -1, PHI)

# The flag to encrypt
FLAG = b"flag{bleichenbacher_padding_oracle_rsa}"
FLAG_INT = bytes_to_long(FLAG)

# PKCS#1 v1.5 padding
def pkcs1_v15_pad(message, key_size_bytes):
    """PKCS#1 v1.5 padding"""
    msg_len = len(message)
    padding_len = key_size_bytes - msg_len - 3
    
    if padding_len < 8:
        raise ValueError("Message too long")
    
    # 0x00 0x02 <random non-zero bytes> 0x00 <message>
    padding = b''
    while len(padding) < padding_len:
        byte = random.randint(1, 255)
        padding += bytes([byte])
    
    return b'\x00\x02' + padding + b'\x00' + message

def pkcs1_v15_unpad(padded, key_size_bytes):
    """PKCS#1 v1.5 unpadding with detailed error messages (THE VULNERABILITY)"""
    # Convert to bytes
    padded_bytes = long_to_bytes(padded, key_size_bytes)
    
    # Check format
    if padded_bytes[0] != 0x00:
        return None, "ERROR: Invalid first byte"
    
    if padded_bytes[1] != 0x02:
        return None, "ERROR: Invalid block type (not 0x02)"
    
    # Find separator
    sep_idx = None
    for i in range(2, len(padded_bytes)):
        if padded_bytes[i] == 0x00:
            sep_idx = i
            break
    
    if sep_idx is None:
        return None, "ERROR: No separator byte found"
    
    if sep_idx < 10:
        return None, "ERROR: Padding too short (less than 8 bytes)"
    
    # Extract message
    message = padded_bytes[sep_idx + 1:]
    
    return message, "OK"

# Encrypt flag
FLAG_PADDED = pkcs1_v15_pad(FLAG, KEY_SIZE // 8)
FLAG_INT_PADDED = bytes_to_long(FLAG_PADDED)
CIPHERTEXT = pow(FLAG_INT_PADDED, E, N)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Bleichenbacher's Revenge</title>
    <style>
        body { font-family: monospace; background: #0a0a0a; color: #00ff00; padding: 40px; }
        .container { max-width: 800px; margin: 0 auto; }
        h1 { color: #ff0000; text-shadow: 0 0 10px #ff0000; }
        .box { background: #111; border: 1px solid #333; padding: 20px; margin: 20px 0; border-radius: 5px; }
        .info { color: #00ffff; }
        .warning { color: #ff0000; }
        input, button { font-family: monospace; padding: 10px; margin: 5px 0; }
        input[type="text"] { width: 100%; background: #222; color: #00ff00; border: 1px solid #444; }
        button { background: #333; color: #00ff00; border: 1px solid #00ff00; cursor: pointer; }
        button:hover { background: #00ff00; color: #000; }
        pre { background: #111; padding: 15px; overflow-x: auto; border: 1px dashed #333; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔐 Bleichenbacher's Revenge</h1>
        <p class="info">RSA PKCS#1 v1.5 Padding Oracle Challenge</p>
        
        <div class="box">
            <h2>RSA Public Key</h2>
            <pre>N = {{ n }}
e = {{ e }}</pre>
        </div>
        
        <div class="box">
            <h2>Encrypted Flag (Ciphertext)</h2>
            <pre>c = {{ c }}</pre>
        </div>
        
        <div class="box">
            <h2>Decryption Oracle</h2>
            <p class="warning">⚠️ This oracle tells you if padding is valid or gives detailed errors</p>
            <form id="decryptForm">
                <input type="text" name="c" placeholder="Enter ciphertext (integer)">
                <button type="submit">Decrypt</button>
            </form>
            <div id="result"></div>
        </div>
        
        <div class="box">
            <h2>Hints</h2>
            <ul>
                <li>This is PKCS#1 v1.5 padding (not OAEP)</li>
                <li>The oracle gives DETAILED error messages</li>
                <li>Bleichenbacher's 1998 attack uses ~1 million queries</li>
                <li>Implement the adaptive chosen-ciphertext attack</li>
                <li>Key insight: Valid padding starts with 0x00 0x02</li>
            </ul>
        </div>
        
        <div class="box">
            <h2>Resources</h2>
            <ul>
                <li><a href="https://crypto.stanford.edu/~dabo/pubs2abstracts/ssl-timing.pdf" style="color: #00ffff;">Original Bleichenbacher Paper</a></li>
                <li><a href="https://blog.filippo.io/bleichenbacher-07-tls-attack/" style="color: #00ffff;">Explanation</a></li>
                <li><a href="https://github.com/danieluhrwork/bleichenbacher-attack" style="color: #00ffff;">Reference Implementation</a></li>
            </ul>
        </div>
    </div>
    
    <script>
    document.getElementById('decryptForm').onsubmit = async (e) => {
        e.preventDefault();
        const c = document.getElementById('decryptForm').c.value;
        const res = await fetch('/oracle', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({c: c})
        });
        const data = await res.json();
        document.getElementById('result').innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
    };
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML, n=N, e=E, c=CIPHERTEXT)

@app.route('/oracle', methods=['POST'])
def oracle():
    """The padding oracle - VULNERABLE!"""
    data = request.get_json()
    
    try:
        c = int(data.get('c', '0'))
        
        if c <= 0 or c >= N:
            return jsonify({'status': 'error', 'message': 'Invalid ciphertext'})
        
        # Decrypt
        decrypted = pow(c, D, N)
        
        # Unpad with detailed errors (THIS IS THE VULNERABILITY)
        message, status = pkcs1_v15_unpad(decrypted, KEY_SIZE // 8)
        
        if status == "OK":
            return jsonify({
                'status': 'valid',
                'message': 'Padding is VALID',
                'hint': 'Congratulations! Now extract the message...'
            })
        else:
            # Different error messages leak information!
            return jsonify({
                'status': 'invalid',
                'message': status,
                'detail': 'Padding check failed'
            })
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/flag', methods=['POST'])
def check_flag():
    """Check if the decrypted flag is correct"""
    data = request.get_json()
    flag = data.get('flag', '')
    
    if flag == FLAG.decode():
        return jsonify({'status': 'success', 'message': 'Congratulations! You broke RSA!'})
    else:
        return jsonify({'status': 'wrong', 'message': 'Incorrect flag'})

if __name__ == '__main__':
    print("=" * 60)
    print("Bleichenbacher's Revenge - College CTF 2026")
    print("=" * 60)
    print(f"N = {N}")
    print(f"e = {E}")
    print(f"c = {CIPHERTEXT}")
    print()
    print("Starting server on port 5010...")
    app.run(host='0.0.0.0', port=5010, debug=False)

from flask import Flask, request, render_template_string
import jwt
import json
import time

app = Flask(__name__)
SECRET = "weak_secret_key_123"

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Broken Auth Challenge</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 600px;
            width: 100%;
        }
        h1 {
            color: #333;
            margin-bottom: 10px;
            text-align: center;
        }
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
        }
        .section {
            background: #f8f9fa;
            padding: 25px;
            border-radius: 12px;
            margin-bottom: 20px;
        }
        .section h2 {
            color: #333;
            margin-bottom: 15px;
            font-size: 18px;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            color: #555;
            font-weight: 600;
        }
        input[type="text"], textarea {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 14px;
            font-family: 'Courier New', monospace;
            transition: border-color 0.3s;
        }
        input:focus, textarea:focus {
            outline: none;
            border-color: #6a11cb;
        }
        textarea { resize: vertical; min-height: 80px; }
        button {
            padding: 12px 30px;
            background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
        }
        button:hover { transform: translateY(-2px); }
        .result {
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
            text-align: center;
            word-break: break-all;
        }
        .result-success {
            background: #f0fff4;
            border: 2px solid #51cf66;
        }
        .result-error {
            background: #fff5f5;
            border: 2px solid #ff6b6b;
        }
        .token-display {
            background: #1e1e1e;
            color: #00ff00;
            padding: 15px;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            font-size: 12px;
            word-break: break-all;
            margin: 10px 0;
            max-height: 100px;
            overflow-y: auto;
        }
        .hint {
            background: #e8eaf6;
            padding: 15px;
            border-radius: 10px;
            margin-top: 20px;
            font-size: 14px;
        }
        .hint strong { color: #283593; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔓 Broken Authentication</h1>
        <p class="subtitle">Can you forge a JWT token to become admin?</p>
        
        <div class="section">
            <h2>Step 1: Get Your Token</h2>
            <form id="loginForm">
                <div class="form-group">
                    <label>Username</label>
                    <input type="text" id="username" placeholder="Enter any username" value="player1">
                </div>
                <button type="submit">Get Token</button>
            </form>
            <div id="tokenResult"></div>
        </div>
        
        <div class="section">
            <h2>Step 2: Submit Modified Token</h2>
            <form id="flagForm">
                <div class="form-group">
                    <label>JWT Token</label>
                    <textarea id="token" placeholder="Paste your modified JWT token here..."></textarea>
                </div>
                <button type="submit">Get Flag</button>
            </form>
        </div>
        
        <div id="flagResult"></div>
        
        <div class="hint">
            <strong>💡 Hint:</strong> JWT tokens have 3 parts separated by dots: 
            header.payload.signature. Decode the payload at <a href="https://jwt.io" target="_blank">jwt.io</a>. 
            The secret key is very weak...
        </div>
    </div>

    <script>
    document.getElementById('loginForm').onsubmit = async (e) => {
        e.preventDefault();
        const username = document.getElementById('username').value;
        const res = await fetch('/login', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({username})
        });
        const data = await res.json();
        document.getElementById('token').value = data.token;
        document.getElementById('tokenResult').innerHTML = 
            '<div class="token-display">' + data.token + '</div>';
    };
    
    document.getElementById('flagForm').onsubmit = async (e) => {
        e.preventDefault();
        const token = document.getElementById('token').value;
        const res = await fetch('/flag', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({token})
        });
        const data = await res.json();
        const cls = data.message.includes('flag{') ? 'result-success' : 'result-error';
        document.getElementById('flagResult').innerHTML = 
            '<div class="result ' + cls + '">' + data.message + '</div>';
    };
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username', 'guest')
    token = jwt.encode({
        'username': username, 
        'role': 'user',
        'iat': int(time.time())
    }, SECRET, algorithm='HS256')
    return jsonify({'token': token})

@app.route('/flag', methods=['POST'])
def flag():
    data = request.get_json()
    token = data.get('token', '')
    try:
        payload = jwt.decode(token, SECRET, algorithms=['HS256'])
        if payload.get('role') == 'admin':
            return jsonify({'message': 'flag{jwt_tokens_can_be_decoded_and_modified}'})
        else:
            return jsonify({'message': f'Hello {payload.get("username")}! Role: {payload.get("role")}. You need admin role.'})
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token expired!'})
    except jwt.InvalidTokenError as e:
        return jsonify({'message': f'Invalid token: {str(e)}'})

# Need to import jsonify
from flask import jsonify

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=False)

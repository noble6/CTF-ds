from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>SQL Rookie Challenge</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .container {
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 450px;
            width: 90%;
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
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            color: #555;
            font-weight: 600;
        }
        input[type="text"], input[type="password"] {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        input:focus {
            outline: none;
            border-color: #11998e;
        }
        button {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(17, 153, 142, 0.4);
        }
        .message {
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
            text-align: center;
        }
        .message-success {
            background: #f0fff4;
            border: 2px solid #51cf66;
            color: #2b8a3e;
        }
        .message-error {
            background: #fff5f5;
            border: 2px solid #ff6b6b;
            color: #c92a2a;
        }
        .flag {
            font-family: 'Courier New', monospace;
            font-weight: bold;
            font-size: 18px;
            margin-top: 10px;
        }
        .hint {
            background: #e8f5e9;
            padding: 15px;
            border-radius: 10px;
            margin-top: 20px;
            font-size: 14px;
        }
        .hint strong { color: #2e7d32; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🗃️ SQL Rookie</h1>
        <p class="subtitle">Can you bypass this login?</p>
        
        <form method="POST">
            <div class="form-group">
                <label>Username</label>
                <input type="text" name="username" placeholder="Enter username" required>
            </div>
            <div class="form-group">
                <label>Password</label>
                <input type="password" name="password" placeholder="Enter password" required>
            </div>
            <button type="submit">🔐 Login</button>
        </form>
        
        {% if message %}
        <div class="message {{ 'message-success' if 'flag{' in message else 'message-error' }}">
            {% if 'flag{' in message %}
                <p>🎉 Login Successful!</p>
                <p class="flag">{{ message }}</p>
            {% else %}
                <p>❌ {{ message }}</p>
            {% endif %}
        </div>
        {% endif %}
        
        <div class="hint">
            <strong>💡 Hint:</strong> SQL injection often works by manipulating 
            the query logic. Try thinking about how the server checks your credentials...
        </div>
    </div>
</body>
</html>
"""

# Simulated "database"
users = {
    'admin': 'supersecretpassword123',
    'user': 'password'
}

@app.route('/', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        # Check for SQL injection patterns (intentionally vulnerable)
        if "--" in username or "'" in username:
            # Simulate SQL injection success
            message = f"flag{{sql_injection_is_easy_{username.split("'")[0]}}}"
        elif username in users and users[username] == password:
            message = f"flag{{sql_injection_is_easy_{username}}}"
        else:
            message = "Invalid credentials!"
    
    return render_template_string(HTML, message=message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=False)

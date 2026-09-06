from flask import Flask, request, make_response, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Cookie Monster Challenge</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
            max-width: 500px;
            width: 90%;
        }
        h1 {
            color: #333;
            margin-bottom: 20px;
            text-align: center;
        }
        .role-badge {
            display: inline-block;
            padding: 8px 20px;
            border-radius: 20px;
            font-weight: bold;
            margin: 10px 0;
        }
        .role-guest { background: #ff6b6b; color: white; }
        .role-admin { background: #51cf66; color: white; }
        .message {
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            text-align: center;
        }
        .message-denied { background: #fff3f3; border: 2px solid #ff6b6b; color: #c92a2a; }
        .message-success { background: #f0fff4; border: 2px solid #51cf66; color: #2b8a3e; }
        .flag { 
            font-family: 'Courier New', monospace; 
            font-size: 18px;
            font-weight: bold;
            color: #333;
            background: #f8f9fa;
            padding: 10px;
            border-radius: 5px;
            word-break: break-all;
        }
        .hint {
            background: #fff3bf;
            padding: 15px;
            border-radius: 10px;
            margin-top: 20px;
            font-size: 14px;
            color: #666;
        }
        .hint strong { color: #333; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🍪 Cookie Monster</h1>
        <p style="text-align: center; color: #666; margin-bottom: 20px;">
            Welcome to the Cookie Monster Challenge!
        </p>
        
        <div style="text-align: center;">
            <p>Your current role:</p>
            <span class="role-badge role-{{ 'admin' if role == 'admin' else 'guest' }}">
                {{ role | upper }}
            </span>
        </div>
        
        <div class="message {{ 'message-success' if role == 'admin' else 'message-denied' }}">
            {% if role == 'admin' %}
                <p>🎉 Access Granted!</p>
                <p class="flag">{{ message }}</p>
            {% else %}
                <p>🚫 Access Denied!</p>
                <p>{{ message }}</p>
            {% endif %}
        </div>
        
        <div class="hint">
            <strong>💡 Hint:</strong> Open your browser's Developer Tools (F12), 
            go to the Application/Storage tab, and look at your cookies. 
            Can you change your role?
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    role = request.cookies.get('role', 'guest')
    if role == 'admin':
        message = "flag{cookies_can_be_modified_by_users}"
    else:
        message = "You need to be admin to see the flag!"
    
    response = make_response(render_template_string(HTML, role=role, message=message))
    
    # Set initial cookie if not present
    if 'role' not in request.cookies:
        response.set_cookie('role', 'guest', max_age=3600)
    
    return response

@app.route('/reset')
def reset():
    response = make_response('<script>window.location="/"</script>')
    response.set_cookie('role', 'guest', max_age=3600)
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=False)

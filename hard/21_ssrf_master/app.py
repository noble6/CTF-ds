from flask import Flask, request, render_template_string, jsonify
import requests
import socket

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>SSRF Master Challenge</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #f12711 0%, #f5af19 100%);
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
            max-width: 700px;
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
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            color: #555;
            font-weight: 600;
        }
        input[type="text"] {
            width: 100%;
            padding: 14px 18px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        input:focus {
            outline: none;
            border-color: #f12711;
        }
        button {
            width: 100%;
            padding: 16px;
            background: linear-gradient(135deg, #f12711 0%, #f5af19 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(241, 39, 17, 0.4);
        }
        .result {
            margin-top: 25px;
            padding: 20px;
            border-radius: 10px;
            background: #f8f9fa;
            border: 2px solid #e0e0e0;
        }
        .result h3 {
            color: #333;
            margin-bottom: 10px;
        }
        .result pre {
            background: #1e1e1e;
            color: #00ff00;
            padding: 15px;
            border-radius: 8px;
            overflow-x: auto;
            font-size: 13px;
            max-height: 300px;
            overflow-y: auto;
        }
        .result-flag {
            background: #f0fff4;
            border-color: #51cf66;
        }
        .result-flag pre {
            color: #2b8a3e;
            background: #e8f5e9;
        }
        .hint {
            background: #fff3e0;
            padding: 20px;
            border-radius: 10px;
            margin-top: 25px;
        }
        .hint h3 {
            color: #e65100;
            margin-bottom: 10px;
        }
        .hint ul {
            margin-left: 20px;
            color: #666;
        }
        .hint li { margin-bottom: 5px; }
        .hint code {
            background: #ff572220;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: monospace;
            color: #d84315;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌐 SSRF Master</h1>
        <p class="subtitle">Fetch any URL from the server. But can you access the internal service?</p>
        
        <form method="POST">
            <div class="form-group">
                <label>Enter URL to fetch:</label>
                <input type="text" name="url" placeholder="https://example.com" 
                       value="{{ url }}" required>
            </div>
            <button type="submit">🔍 Fetch URL</button>
        </form>
        
        {% if result %}
        <div class="result {{ 'result-flag' if 'flag{' in result }}">
            <h3>Response:</h3>
            <pre>{{ result }}</pre>
        </div>
        {% endif %}
        
        {% if error %}
        <div class="result" style="border-color: #ff6b6b;">
            <h3 style="color: #c92a2a;">Error:</h3>
            <pre style="color: #c92a2a;">{{ error }}</pre>
        </div>
        {% endif %}
        
        <div class="hint">
            <h3>💡 Hints:</h3>
            <ul>
                <li>There's a secret service running on <code>localhost:9999</code></li>
                <li>The server blocks <code>127.0.0.1</code> and <code>localhost</code></li>
                <li>But there are many ways to represent an IP address...</li>
                <li>Try: decimal, hex, octal, IPv6, DNS rebinding, redirects</li>
            </ul>
        </div>
    </div>
</body>
</html>
"""

FLAG = "flag{ssrf_can_access_internal_services}"

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ''
    error = ''
    url = ''
    
    if request.method == 'POST':
        url = request.form.get('url', '')
        
        # Blocklist (bypassable!)
        blocked = ['127.0.0.1', 'localhost', '0.0.0.0', '::1']
        
        try:
            # Check if URL contains blocked terms
            if any(blocked_word in url.lower() for blocked_word in blocked):
                error = "🚫 Access to internal addresses is blocked!\n\nBlocked patterns: 127.0.0.1, localhost, 0.0.0.0, ::1"
            else:
                # Fetch the URL (vulnerable to SSRF)
                response = requests.get(url, timeout=5, allow_redirects=True)
                result = f"HTTP {response.status_code}\n\n" + response.text[:2000]
        except requests.exceptions.Timeout:
            error = "⏱️ Request timed out (5 seconds)"
        except requests.exceptions.ConnectionError:
            error = "❌ Connection failed - service may not exist"
        except Exception as e:
            error = f"❌ Error: {str(e)}"
    
    return render_template_string(HTML, result=result, error=error, url=url)

@app.route('/internal-secret')
def internal_secret():
    """Internal service - not accessible from outside"""
    return FLAG

if __name__ == '__main__':
    from flask import jsonify
    from threading import Thread
    
    # Internal service
    internal_app = Flask(__name__)
    
    @internal_app.route('/')
    def internal_flag():
        return FLAG
    
    @internal_app.route('/flag')
    def flag_endpoint():
        return FLAG
    
    # Start internal service
    Thread(target=lambda: internal_app.run(port=9999, host='127.0.0.1'), daemon=True).start()
    
    # Start main service
    app.run(host='0.0.0.0', port=5008, debug=False)

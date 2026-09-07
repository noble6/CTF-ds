from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head><title>Path Traversal</title></head>
<body>
    <h1>File Viewer</h1>
    <p>Enter a filename to view:</p>
    <form method="GET">
        <input type="text" name="file" placeholder="filename.txt">
        <button type="submit">View File</button>
    </form>
    {% if content %}
    <h2>File Content:</h2>
    <pre>{{ content }}</pre>
    {% endif %}
    {% if error %}
    <p style="color: red;">{{ error }}</p>
    {% endif %}
</body>
</html>
"""

# Create files directory
os.makedirs('files', exist_ok=True)

# Create some dummy files
with open('files/readme.txt', 'w') as f:
    f.write("Welcome to the file server!")

with open('files/secret.txt', 'w') as f:
    f.write("The secret is... just kidding, try harder!")

# Create flag in a location that requires path traversal
os.makedirs('private', exist_ok=True)
with open('private/flag.txt', 'w') as f:
    f.write("flag{path_traversal_reads_sensitive_files}")

@app.route('/')
def index():
    filename = request.args.get('file', '')
    content = ''
    error = ''
    
    if filename:
        # Vulnerable path handling (intentionally)
        filepath = os.path.join('files', filename)
        try:
            # Check if file exists in files directory
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    content = f.read()
            else:
                error = f"File '{filename}' not found in files directory!"
        except Exception as e:
            error = f"Error reading file: {str(e)}"
    
    return render_template_string(HTML, content=content, error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)

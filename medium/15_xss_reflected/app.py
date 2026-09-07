from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head><title>XSS Reflected</title></head>
<body>
    <h1>Search Page</h1>
    <p>Try searching for something!</p>
    <form method="GET">
        <input type="text" name="q" placeholder="Search..." value="{{ query }}">
        <button type="submit">Search</button>
    </form>
    {% if query %}
    <h2>Search Results for: {{ query }}</h2>
    <p>No results found for "{{ query }}". Try again!</p>
    {% endif %}
    
    <h3>Hint: Can you make the page execute JavaScript?</h3>
    <p>The flag will appear in an alert box when you execute: <code>alert('XSS')</code></p>
</body>
</html>
"""

@app.route('/')
def index():
    query = request.args.get('q', '')
    # Vulnerable: directly inserting user input into HTML
    # In a real app, you'd use escape() or template auto-escaping
    return render_template_string(HTML, query=query)

@app.route('/flag')
def flag():
    # This endpoint returns the flag if accessed via XSS
    return "flag{xss_can_execute_arbitrary_javascript}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006)

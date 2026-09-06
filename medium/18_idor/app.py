from flask import Flask, request, render_template_string, jsonify

app = Flask(__name__)

# Simulated user database
users = {
    1: {'username': 'admin', 'email': 'admin@secret.com', 'secret': 'flag{idor_exposes_other_users_data}'},
    2: {'username': 'user1', 'email': 'user1@example.com', 'secret': 'Nothing interesting here'},
    3: {'username': 'user2', 'email': 'user2@example.com', 'secret': 'Just a regular user'},
}

HTML = """
<!DOCTYPE html>
<html>
<head><title>IDOR Challenge</title></head>
<body>
    <h1>User Profile Lookup</h1>
    <p>You are logged in as: <strong>{{ current_user }}</strong></p>
    
    <h2>Your Profile:</h2>
    <ul>
        <li>Username: {{ user.username }}</li>
        <li>Email: {{ user.email }}</li>
        <li>Secret: {{ user.secret }}</li>
    </ul>
    
    <h2>Other Users:</h2>
    <p>Try changing the user_id parameter in the URL!</p>
    <ul>
        <li><a href="/profile?user_id=1">Profile 1</a></li>
        <li><a href="/profile?user_id=2">Profile 2</a></li>
        <li><a href="/profile?user_id=3">Profile 3</a></li>
    </ul>
    
    <p>Hint: What happens if you try user_id=1?</p>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML, 
                                current_user='user1',
                                user=users[2])

@app.route('/profile')
def profile():
    user_id = request.args.get('user_id', 2)
    
    # Vulnerable: no authorization check
    try:
        user_id = int(user_id)
        if user_id in users:
            user = users[user_id]
            return render_template_string(HTML, 
                                        current_user='user1',
                                        user=user)
        else:
            return "User not found", 404
    except ValueError:
        return "Invalid user_id", 400

if __name__ == '__main__':
    app.run(port=5006)

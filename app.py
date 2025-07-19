from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Enhanced user database with avatars
users = {
    'user1': {
        'password': 'pass1',
        'display_name': 'User One',
        'avatar': '/static/images/user1-avatar.png',
        'color': '#4a6fa5'
    },
    'user2': {
        'password': 'pass2',
        'display_name': 'User Two',
        'avatar': '/static/images/user2-avatar.png',
        'color': '#9c4a9c'
    }
}

# Store messages with reply functionality
messages = []

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('chat'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in users and users[username]['password'] == password:
            session['username'] = username
            session.update(users[username])  # Store all user data in session
            return redirect(url_for('chat'))
        else:
            return render_template('login.html', error='Invalid username or password')
    
    return render_template('login.html')

@app.route('/chat')
def chat():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if session['username'] not in ['user1', 'user2']:
        return redirect(url_for('login'))
    
    return render_template('chat.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/get_messages')
def get_messages():
    if 'username' not in session:
        return jsonify({'status': 'error', 'message': 'Not logged in'}), 401
    
    return jsonify({'status': 'success', 'messages': messages})

@app.route('/send_message', methods=['POST'])
def send_message():
    if 'username' not in session:
        return jsonify({'status': 'error', 'message': 'Not logged in'}), 401
    
    data = request.get_json()
    if not data:
        return jsonify({'status': 'error', 'message': 'Invalid data'}), 400
    
    message = data.get('message')
    reply_to = data.get('reply_to')
    
    if message and message.strip():
        new_message = {
            'id': len(messages) + 1,
            'sender': session['username'],
            'display_name': session['display_name'],
            'avatar': session['avatar'],
            'color': session['color'],
            'message': message.strip(),
            'timestamp': datetime.now().strftime('%H:%M'),
            'reply_to': reply_to
        }
        messages.append(new_message)
        
        if len(messages) > 100:
            messages.pop(0)
        
        return jsonify({'status': 'success', 'message': new_message})
    
    return jsonify({'status': 'error', 'message': 'Empty message'}), 400

if __name__ == '__main__':
    app.run(debug=True)

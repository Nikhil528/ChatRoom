from flask import Flask, render_template, session, redirect, url_for, request, jsonify
import time
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Mock user database (in a real app, use proper authentication and database)
USERS = {
    'user1': {'password': 'pass1', 'name': 'Alex Johnson', 'avatar': '👨‍💻'},
    'user2': {'password': 'pass2', 'name': 'Sam Smith', 'avatar': '👩‍💼'}
}

# Store messages in memory (would use database in production)
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
        
        if username in USERS and USERS[username]['password'] == password:
            session['username'] = username
            session['name'] = USERS[username]['name']
            session['avatar'] = USERS[username]['avatar']
            return redirect(url_for('chat'))
        return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/chat')
def chat():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('chat.html', messages=messages)

@app.route('/send', methods=['POST'])
def send_message():
    if 'username' not in session:
        return jsonify({'status': 'error', 'message': 'Not authenticated'}), 401
    
    message = request.json.get('message')
    if message:
        timestamp = time.strftime('%H:%M')
        new_message = {
            'sender': session['username'],
            'name': session['name'],
            'avatar': session['avatar'],
            'message': message,
            'timestamp': timestamp
        }
        messages.append(new_message)
        return jsonify({'status': 'success', 'message': new_message})
    
    return jsonify({'status': 'error', 'message': 'Empty message'}), 400

@app.route('/get_messages')
def get_messages():
    if 'username' not in session:
        return jsonify({'status': 'error', 'message': 'Not authenticated'}), 401
    
    return jsonify({'status': 'success', 'messages': messages})

if __name__ == '__main__':
    app.run(debug=True)

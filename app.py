# app.py
from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, join_room, leave_room, emit
from datetime import datetime
import os
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
socketio = SocketIO(app)

# In-memory database for users and messages (for demonstration)
users = {
    "user1": {"password": "user1", "name": "User One"},
    "user2": {"password": "user2", "name": "User Two"}
}

# Store messages in memory (in production, use a database)
messages = []

@app.route('/')
def index():
    # If user is logged in, redirect to chat
    if 'username' in session:
        return redirect(url_for('chat'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check credentials
        if username in users and users[username]['password'] == password:
            session['username'] = username
            return redirect(url_for('chat'))
        return render_template('login.html', error="Invalid credentials")
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/chat')
def chat():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Only allow user1 and user2
    if session['username'] not in ['user1', 'user2']:
        return redirect(url_for('logout'))
    
    return render_template('chat.html', 
                           username=session['username'],
                           user_info=users[session['username']],
                           messages=messages)

@socketio.on('connect')
def handle_connect():
    if 'username' in session:
        # Both users join the same room
        join_room('user1_user2_room')
        emit('user_status', {
            'user': session['username'],
            'status': 'online',
            'timestamp': datetime.now().strftime("%H:%M:%S")
        }, room='user1_user2_room')

@socketio.on('disconnect')
def handle_disconnect():
    if 'username' in session:
        leave_room('user1_user2_room')
        emit('user_status', {
            'user': session['username'],
            'status': 'offline',
            'timestamp': datetime.now().strftime("%H:%M:%S")
        }, room='user1_user2_room')

@socketio.on('send_message')
def handle_send_message(data):
    if 'username' not in session:
        return
    
    username = session['username']
    message = data['message']
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Create message object
    message_obj = {
        'sender': username,
        'text': message,
        'timestamp': timestamp,
        'sender_name': users[username]['name']
    }
    
    # Store message
    messages.append(message_obj)
    
    # Broadcast to room
    emit('receive_message', message_obj, room='user1_user2_room')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)

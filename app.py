from flask import Flask, render_template, request, redirect, session, url_for
from flask_socketio import SocketIO, emit, join_room, leave_room
from datetime import datetime
import time

app = Flask(__name__)
app.secret_key = 'supersecretkey'
socketio = SocketIO(app, cors_allowed_origins="*")

# Store chat history
chat_history = []

# User database
users = {
    'user1': {'password': 'pass1', 'name': 'User One', 'avatar': 'U1'},
    'user2': {'password': 'pass2', 'name': 'User Two', 'avatar': 'U2'}
}

# Track online users
online_users = set()

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    if username in users and users[username]['password'] == password:
        session['username'] = username
        session['name'] = users[username]['name']
        session['avatar'] = users[username]['avatar']
        return redirect(url_for('chat'))
    else:
        return redirect(url_for('login_page'))

@app.route('/chat')
def chat():
    if 'username' in session:
        return render_template('chat.html', 
            username=session['username'],
            name=session['name'],
            avatar=session['avatar'])
    else:
        return redirect(url_for('login_page'))

@app.route('/logout')
def logout():
    username = session.get('username')
    if username:
        online_users.discard(username)
        socketio.emit('user_left', username, broadcast=True)
    
    session.pop('username', None)
    session.pop('name', None)
    session.pop('avatar', None)
    return redirect(url_for('login_page'))

# SocketIO event handlers
@socketio.on('join')
def handle_join(username):
    join_room('chat_room')
    online_users.add(username)
    emit('user_joined', username, broadcast=True)
    emit('chat_history', chat_history)

@socketio.on('send_message')
def handle_send_message(data):
    # Store message in history
    message = {
        'text': data['text'],
        'sender': data['sender'],
        'timestamp': data['timestamp']
    }
    chat_history.append(message)
    
    # Broadcast to all clients in the chat room
    emit('receive_message', message, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    username = session.get('username')
    if username and username in online_users:
        online_users.remove(username)
        emit('user_left', username, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')

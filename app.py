from flask import Flask, render_template, request, redirect, session, url_for
from flask_socketio import SocketIO, emit
from datetime import datetime
import time

app = Flask(__name__)
app.secret_key = 'supersecretkey'
socketio = SocketIO(app)

# Store chat history in memory
chat_history = []

# User database
users = {
    'user1': {'password': 'pass1', 'name': 'User One', 'avatar': 'U1'},
    'user2': {'password': 'pass2', 'name': 'User Two', 'avatar': 'U2'}
}

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
    session.pop('username', None)
    session.pop('name', None)
    session.pop('avatar', None)
    return redirect(url_for('login_page'))

# SocketIO event handlers
@socketio.on('send_message')
def handle_send_message(data):
    # Store message in history
    chat_history.append({
        'text': data['text'],
        'sender': data['sender'],
        'timestamp': data['timestamp']
    })
    
    # Broadcast to all clients
    emit('receive_message', {
        'text': data['text'],
        'sender': data['sender'],
        'timestamp': data['timestamp']
    }, broadcast=True)

@socketio.on('request_history')
def handle_request_history():
    # Send chat history to the requesting client
    emit('chat_history', chat_history)

if __name__ == '__main__':
    socketio.run(app, debug=True)

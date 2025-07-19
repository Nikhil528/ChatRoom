from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import eventlet

eventlet.monkey_patch()

app = Flask(__name__)
app.secret_key = 'supersecretkey'
socketio = SocketIO(app, cors_allowed_origins="*")

# Store chat history
chat_history = []

# Track online users
online_users = set()

@socketio.on('join')
def handle_join(username):
    online_users.add(username)
    emit('user_joined', username, broadcast=True)

@socketio.on('leave')
def handle_leave(username):
    if username in online_users:
        online_users.remove(username)
    emit('user_left', username, broadcast=True)

@socketio.on('send_message')
def handle_send_message(data):
    # Store message in history
    chat_history.append(data)
    
    # Broadcast to all clients
    emit('receive_message', data, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    # We'll handle disconnects through explicit leave events
    pass

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)

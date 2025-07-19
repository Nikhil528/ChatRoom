from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(nikhil)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='eventlet')

# Track rooms and users
rooms = {}

@socketio.on('join')
def handle_join(data):
    room_id = data['room_id']
    user_id = data['user_id']
    
    join_room(room_id)
    
    # Initialize room if not exists
    if room_id not in rooms:
        rooms[room_id] = {'users': []}
    
    # Add user to room
    rooms[room_id]['users'].append(user_id)
    
    # Notify others in the room
    emit('user_joined', {'user_id': user_id}, to=room_id, include_self=False)
    
    # Send existing users to the new user
    emit('existing_users', {'users': rooms[room_id]['users']})

@socketio.on('signal')
def handle_signal(data):
    # Relay signaling data to specific user
    emit('signal', data, to=data['target_user_id'])

@socketio.on('chat_message')
def handle_chat(data):
    # Broadcast chat message to room
    emit('chat_message', {
        'user_id': data['user_id'],
        'message': data['message']
    }, to=data['room_id'])

@socketio.on('leave')
def handle_leave(data):
    room_id = data['room_id']
    user_id = data['user_id']
    
    leave_room(room_id)
    rooms[room_id]['users'].remove(user_id)
    
    # Notify room
    emit('user_left', {'user_id': user_id}, to=room_id)

@app.route('/<room_id>')
def index(room_id):
    return render_template('index.html', room_id=room_id)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)

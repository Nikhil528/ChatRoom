from flask import Flask, render_template, request, redirect, session, jsonify
from flask_socketio import SocketIO, join_room, leave_room, emit
import sqlite3
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
socketio = SocketIO(app)

# Initialize DB (users + messages)
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY,
                sender TEXT,
                receiver TEXT,
                message TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    try:
        c.execute("INSERT INTO users (username, password) VALUES ('user1', 'Betu')")
        c.execute("INSERT INTO users (username, password) VALUES ('user2', 'Betu2')")
    except sqlite3.IntegrityError:
        pass
    conn.commit()
    conn.close()

if not os.path.exists('database.db'):
    init_db()

# === HTTP Routes ===

@app.route('/')
def login_page():
    if 'username' in session:
        return redirect('/chat')
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()

    if user:
        session['username'] = username
        return redirect('/chat')
    return "Invalid credentials", 401

@app.route('/chat')
def chat():
    if 'username' not in session:
        return redirect('/')
    return render_template('chat.html', username=session['username'])

@app.route('/send', methods=['POST'])
def send_message():
    if 'username' not in session:
        return jsonify(success=False, error='Not logged in'), 401

    sender = session['username']
    receiver = 'user2' if sender == 'user1' else 'user1'
    message = request.json.get('message')

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO messages (sender, receiver, message) VALUES (?, ?, ?)",
              (sender, receiver, message))
    conn.commit()
    conn.close()
    return jsonify(success=True)

@app.route('/get_messages')
def get_messages():
    if 'username' not in session:
        return jsonify([])

    username = session['username']
    other_user = 'user2' if username == 'user1' else 'user1'

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM messages WHERE (sender=? AND receiver=?) OR (sender=? AND receiver=?) ORDER BY timestamp",
              (username, other_user, other_user, username))
    messages = c.fetchall()
    conn.close()

    return jsonify([{
        'id': msg[0],
        'sender': msg[1],
        'text': msg[3],
        'time': msg[4]
    } for msg in messages])

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

# === SocketIO Events ===

@socketio.on('join')
def handle_join(data):
    if 'username' not in session:
        return False  # Reject if not logged in

    room = data.get('room')
    username = session['username']

    join_room(room)
    emit('user-joined', {'username': username}, room=room)
    print(f"{username} joined room {room}")

@socketio.on('offer')
def handle_offer(data):
    room = data.get('room')
    offer = data.get('offer')
    emit('offer', {'offer': offer}, room=room, include_self=False)

@socketio.on('answer')
def handle_answer(data):
    room = data.get('room')
    answer = data.get('answer')
    emit('answer', {'answer': answer}, room=room, include_self=False)

@socketio.on('candidate')
def handle_candidate(data):
    room = data.get('room')
    candidate = data.get('candidate')
    emit('candidate', {'candidate': candidate}, room=room, include_self=False)

if __name__ == '__main__':
    socketio.run(app, debug=True)

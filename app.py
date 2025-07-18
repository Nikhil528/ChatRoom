from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit, join_room
import os
import sqlite3

app = Flask(__name__)
app.secret_key = "secret"
socketio = SocketIO(app)

# --- Create SQLite DB ---
def init_db():
    if not os.path.exists('database.db'):
        conn = sqlite3.connect('database.db')
        conn.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT)')
        conn.close()

init_db()

# --- Routes ---
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form.get("username")
        session["username"] = username
        return redirect(url_for("chat"))
    return render_template("index.html")

@app.route("/chat")
def chat():
    if "username" not in session:
        return redirect(url_for("index"))
    return render_template("chat.html", username=session["username"])

# --- Socket.IO Events ---
@socketio.on("join")
def handle_join(data):
    username = data["username"]
    room = "global"
    join_room(room)
    emit("user_joined", {"username": username}, room=room)

@socketio.on("offer")
def handle_offer(data):
    emit("offer", data, broadcast=True, include_self=False)

@socketio.on("answer")
def handle_answer(data):
    emit("answer", data, broadcast=True, include_self=False)

@socketio.on("candidate")
def handle_candidate(data):
    emit("candidate", data, broadcast=True, include_self=False)

if __name__ == "__main__":
    socketio.run(app, debug=True)

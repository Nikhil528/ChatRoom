from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.permanent_session_lifetime = timedelta(minutes=60)

chat_history = []

USERS = {
    'user1': 'password1',
    'user2': 'password2'
}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in USERS and USERS[username] == password:
            session['username'] = username
            return redirect(url_for('chat'))
        return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/chat')
def chat():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('chat.html', username=session['username'])

@app.route('/send_message', methods=['POST'])
def send_message():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json()
    message = data.get('message')
    reply_to = data.get('reply_to')
    chat_history.append({
        'sender': session['username'],
        'message': message,
        'reply_to': reply_to
    })
    return jsonify({'success': True})

@app.route('/get_messages')
def get_messages():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 403
    return jsonify(chat_history)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

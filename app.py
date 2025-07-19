from flask import Flask, render_template, request, redirect, session, jsonify
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Hardcoded users for simplicity
USERS = {
    'user1': 'password1',
    'user2': 'password2'
}

# Store messages in memory (for demo purposes)
messages = []

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in USERS and USERS[username] == password:
            session['username'] = username
            return redirect('/chat')
        else:
            return render_template('login.html', error="Invalid credentials")
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

@app.route('/chat')
def chat():
    if 'username' not in session:
        return redirect('/login')
    
    return render_template('chat.html', username=session['username'])

@app.route('/send_message', methods=['POST'])
def send_message():
    if 'username' not in session:
        return jsonify({'status': 'error', 'message': 'Not logged in'}), 401
    
    data = request.json
    message = data.get('message')
    
    if not message:
        return jsonify({'status': 'error', 'message': 'Empty message'}), 400
    
    # Store message with timestamp
    messages.append({
        'sender': session['username'],
        'message': message,
        'timestamp': datetime.now().strftime('%H:%M:%S')
    })
    
    # Keep only the last 100 messages
    if len(messages) > 100:
        messages.pop(0)
    
    return jsonify({'status': 'success'})

@app.route('/get_messages')
def get_messages():
    if 'username' not in session:
        return jsonify({'status': 'error', 'message': 'Not logged in'}), 401
    
    return jsonify({'status': 'success', 'messages': messages})

if __name__ == '__main__':
    app.run(debug=True)

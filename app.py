from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-123'  # Change this for production

# Mock database (replace with real database in production)
users = {
    'betu1': generate_password_hash('betu'),
    'betu2': generate_password_hash('betu2')
}

messages = []
active_users = set()

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username or not password:
            return jsonify({'success': False, 'message': 'Both fields are required'}), 400
            
        if username not in users or not check_password_hash(users[username], password):
            return jsonify({'success': False, 'message': 'Invalid username or password'}), 401
            
        session['username'] = username
        active_users.add(username)
        return jsonify({'success': True, 'redirect': url_for('chat')})
    
    return render_template('login.html')

@app.route('/chat')
def chat():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('chat.html', username=session['username'])

@app.route('/logout')
def logout():
    if 'username' in session:
        active_users.discard(session['username'])
        session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/send', methods=['POST'])
def send_message():
    if 'username' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'}), 401
        
    data = request.get_json()
    message = data.get('message', '').strip()
    
    if not message:
        return jsonify({'success': False, 'message': 'Message cannot be empty'}), 400
    
    messages.append({
        'sender': session['username'],
        'text': message,
        'time': datetime.now().strftime('%H:%M:%S')
    })
    return jsonify({'success': True})

@app.route('/get_messages')
def get_messages():
    if 'username' not in session:
        return jsonify({'success': False}), 401
    return jsonify(messages)

@app.route('/get_users')
def get_users():
    if 'username' not in session:
        return jsonify({'success': False}), 401
    return jsonify({'users': list(active_users)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)

from flask import Flask, render_template, request, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Simple user database (in real app, use proper database)
users = {
    'user1': {'password': 'pass1', 'display_name': 'User One'},
    'user2': {'password': 'pass2', 'display_name': 'User Two'}
}

# Store messages in memory (in real app, use database)
messages = []

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('chat'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in users and users[username]['password'] == password:
            session['username'] = username
            session['display_name'] = users[username]['display_name']
            return redirect(url_for('chat'))
        else:
            return render_template('login.html', error='Invalid username or password')
    
    return render_template('login.html')

@app.route('/chat')
def chat():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Only allow user1 and user2 to chat
    if session['username'] not in ['user1', 'user2']:
        return redirect(url_for('login'))
    
    return render_template('chat.html', 
                         username=session['username'],
                         display_name=session['display_name'])

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('display_name', None)
    return redirect(url_for('login'))

@app.route('/get_messages')
def get_messages():
    if 'username' not in session:
        return jsonify({'status': 'error', 'message': 'Not logged in'})
    
    return jsonify({'status': 'success', 'messages': messages})

@app.route('/send_message', methods=['POST'])
def send_message():
    if 'username' not in session:
        return jsonify({'status': 'error', 'message': 'Not logged in'})
    
    message = request.json.get('message')
    if message:
        messages.append({
            'sender': session['username'],
            'display_name': session['display_name'],
            'message': message,
            'timestamp': datetime.now().strftime('%H:%M')
        })
        # Keep only the last 100 messages
        if len(messages) > 100:
            messages.pop(0)
        
        return jsonify({'status': 'success'})
    
    return jsonify({'status': 'error', 'message': 'Empty message'})

if __name__ == '__main__':
    app.run(debug=True)

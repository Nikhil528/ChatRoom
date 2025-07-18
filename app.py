from flask import Flask, request, jsonify, render_template, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Store messages in memory
messages = []
# Store active users (for demonstration)
active_users = set()

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        if username and username.strip():
            session['username'] = username.strip()
            active_users.add(username.strip())
            return redirect(url_for('chat'))
        return render_template('login.html', error='Please enter a username')
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
        return jsonify({'error': 'Not authenticated'}), 401
        
    data = request.json
    if not data or 'message' not in data:
        return jsonify({'error': 'Invalid data'}), 400
    
    messages.append({
        'sender': session['username'],
        'text': data['message'],
        'time': datetime.now().strftime('%H:%M:%S')
    })
    return jsonify({'status': 'success'})

@app.route('/get_messages', methods=['GET'])
def get_messages():
    return jsonify(messages)

@app.route('/get_users', methods=['GET'])
def get_users():
    return jsonify(list(active_users))

if __name__ == '__main__':
    app.run(debug=True, port=5000)

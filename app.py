from flask import Flask, request, jsonify, render_template, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Needed for session

# Store messages in memory (for demo)
messages = []

# Simple CORS headers (alternative to flask-cors)
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.route('/')
def index():
    # Store username in session
    session['username'] = request.args.get('username', 'default_user')
    return render_template('chat.html')

@app.route('/send', methods=['POST'])
def send_message():
    data = request.json
    if not data or 'message' not in data:
        return jsonify({'error': 'Invalid data'}), 400
    
    messages.append({
        'sender': session.get('username', 'anonymous'),
        'text': data['message'],
        'time': datetime.now().strftime('%H:%M:%S')
    })
    return jsonify({'status': 'success'})

@app.route('/get_messages', methods=['GET'])
def get_messages():
    return jsonify(messages)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

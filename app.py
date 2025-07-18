from flask import Flask, request, jsonify, render_template, session
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Needed for session
CORS(app)  # Enable CORS if needed

# Store messages in memory (for demo)
messages = []

@app.route('/')
def index():
    # Store username in session (simplified)
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

# WebRTC signaling endpoints (simplified)
@app.route('/offer', methods=['POST'])
def handle_offer():
    # In a real app, you'd process WebRTC offer here
    return jsonify({'status': 'offer_received'})

@app.route('/answer', methods=['POST'])
def handle_answer():
    # In a real app, you'd process WebRTC answer here
    return jsonify({'status': 'answer_received'})

@app.route('/ice-candidate', methods=['POST'])
def handle_ice_candidate():
    # In a real app, you'd process ICE candidates here
    return jsonify({'status': 'candidate_received'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)

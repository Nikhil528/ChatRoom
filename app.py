from flask import Flask, render_template, request, session, redirect, url_for
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.permanent_session_lifetime = timedelta(minutes=30)

# Valid users with emoji avatars
users = {
    "user1": {
        "password": "pass1",
        "name": "User One",
        "avatar": "👩",  # Female emoji
        "color": "#4a6fa5"
    },
    "user2": {
        "password": "pass2",
        "name": "User Two",
        "avatar": "👨",  # Male emoji
        "color": "#9c4a9c"
    }
}

# Store messages and reply information
messages = []

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in users and users[username]['password'] == password:
            session.permanent = True
            session['username'] = username
            session['name'] = users[username]['name']
            session['avatar'] = users[username]['avatar']
            session['color'] = users[username]['color']
            return redirect(url_for('chat'))
        else:
            return render_template('login.html', error="Invalid username or password")
    
    if 'username' in session:
        return redirect(url_for('chat'))
    
    return render_template('login.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        message = request.form.get('message')
        reply_to = request.form.get('reply_to', '')
        if message:
            replied_message = None
            if reply_to:
                for msg in messages:
                    if str(msg['id']) == reply_to:
                        replied_message = msg
                        break
            
            messages.append({
                'id': len(messages),
                'sender': session['username'],
                'name': session['name'],
                'avatar': session['avatar'],
                'color': session['color'],
                'message': message,
                'time': datetime.now().strftime('%H:%M'),
                'reply_to': replied_message
            })
    
    return render_template('chat.html', 
                         username=session['username'],
                         name=session['name'],
                         avatar=session['avatar'],
                         color=session['color'],
                         messages=messages,
                         other_user=get_other_user(session['username']))

def get_other_user(current_user):
    return "user2" if current_user == "user1" else "user1"

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('name', None)
    session.pop('avatar', None)
    session.pop('color', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, session, redirect, url_for
from datetime import datetime, timedelta  # Added datetime import

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.permanent_session_lifetime = timedelta(minutes=30)

# Valid users
users = {
    "user1": {"password": "pass1", "name": "User One"},
    "user2": {"password": "pass2", "name": "User Two"}
}

# Store messages (in a real app, use a database)
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
        if message and message.strip():
            messages.append({
                'sender': session['username'],
                'name': session['name'],
                'message': message.strip(),
                'time': datetime.now().strftime('%H:%M')
            })
            return redirect(url_for('chat'))  # Redirect to avoid form resubmission
    
    other_user = "user2" if session['username'] == "user1" else "user1"
    other_user_name = users[other_user]['name']
    
    return render_template('chat.html', 
                         username=session['username'],
                         name=session['name'],
                         messages=messages,
                         other_user=other_user,
                         other_user_name=other_user_name)

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('name', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

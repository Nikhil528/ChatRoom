from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = 'supersecretkey'

users = {
    'user1': {'password': 'pass1', 'name': 'User One', 'avatar': 'U1'},
    'user2': {'password': 'pass2', 'name': 'User Two', 'avatar': 'U2'}
}

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    if username in users and users[username]['password'] == password:
        session['username'] = username
        session['name'] = users[username]['name']
        session['avatar'] = users[username]['avatar']
        return redirect(url_for('chat'))
    else:
        return redirect(url_for('login_page'))

@app.route('/chat')
def chat():
    if 'username' in session:
        return render_template('chat.html', 
            username=session['username'],
            name=session['name'],
            avatar=session['avatar'])
    else:
        return redirect(url_for('login_page'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('name', None)
    session.pop('avatar', None)
    return redirect(url_for('login_page'))

if __name__ == '__main__':
    app.run(debug=True)

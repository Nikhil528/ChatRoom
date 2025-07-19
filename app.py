from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        if username:
            session['username'] = username
            return redirect(url_for("chat"))
    return render_template("login.html")

@app.route("/chat")
def chat():
    if 'username' not in session:
        return redirect(url_for("login"))
    return render_template("chat.html", username=session['username'])

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)


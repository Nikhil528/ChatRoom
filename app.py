from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/<room_id>')
def video_chat(room_id):
    return render_template('index.html', room_id=room_id)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

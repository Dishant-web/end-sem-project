from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)
messages = []

@app.route('/')
def home():
    return render_template('index.html', messages=messages)

@app.route('/send/<username>/<message>')
def send_message(username, message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    messages.append({
        'username': username,
        'message': message,
        'timestamp': timestamp
    })
    return {'status': 'success'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
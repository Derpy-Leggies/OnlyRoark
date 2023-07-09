from flask import Flask, render_template
from roark.events import socketio


app = Flask(__name__)
app.config.from_pyfile('config.py')
socketio.init_app(app)


@app.route('/')
def hello_world():
    return render_template('views/chatroom.html')


if __name__ == '__main__':
    socketio.run(app, async_mode='eventlet')

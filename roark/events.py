from flask import request
from flask_socketio import emit
from roark.extensions import socketio


users = {}


@socketio.on('connect')
def handle_connect():
    print('Client connected!')
    emit('server_response', {'data': 'Connected!'})


@socketio.on('user_joined')
def handle_user_joined(username):
    users[request.sid] = username
    emit('user_joined', {'username': username}, broadcast=True)


@socketio.on('new_message')
def handle_new_message(message):
    username = 'Server'
    if request.sid in users:
        username = users[request.sid]

    emit('chat_message', {'message': message, 'username': username}, broadcast=True)

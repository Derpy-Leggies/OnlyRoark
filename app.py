from roark import app, socketio

if __name__ == '__main__':
    socketio.run(app, async_mode='eventlet')

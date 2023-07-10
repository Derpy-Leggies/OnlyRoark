from flask_login import current_user
from flask_socketio import emit
from models import Users
from extensions import db
from extensions import socketio


@socketio.on('connect')
def handle_connect():
    if not current_user.is_authenticated:
        return False

    set_status = Users.query.filter_by(id=current_user.id).first()
    set_status.status = True
    db.session.add(set_status)
    db.session.commit()

    emit('status', {'status': True, 'id': current_user.id})


@socketio.on('disconnect')
def handle_disconnect():
    if not current_user.is_authenticated:
        return False

    set_status = Users.query.filter_by(id=current_user.id).first()
    set_status.status = False
    db.session.add(set_status)
    db.session.commit()

    emit('status', {'status': False, 'id': current_user.id})

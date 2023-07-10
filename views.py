from flask import Blueprint, render_template, request, jsonify, abort
from flask_login import login_required, current_user
from extensions import db
from models import Messages, Users
from events import socketio
from werkzeug.utils import secure_filename


blueprint = Blueprint('views', __name__)


@blueprint.route('/', methods=['GET'])
@login_required
def index():
    users = Users.query.all()
    return render_template('views/chatroom.html', users=users)


@blueprint.route('/message', methods=['GET', 'POST'])
@login_required
def message_list():
    if request.method == 'POST':
        message_content = request.form.get('message').strip()
        file_content = request.files.get('file')

        if file_content:
            file_name = secure_filename(file_content.filename)

            new_message = Messages(content=file_name, user_id=current_user.id, type='image')
            db.session.add(new_message)
            db.session.commit()

            if file_name.split('.')[-1] in ['png', 'jpg', 'jpeg', 'gif']:
                file_content.save(f'static/uploads/{file_name}')
            else:
                abort(400)

            content = {
                'id': new_message.id,
                'username': current_user.username,
                'type': 'image',
                'content': new_message.content,
                'created_at': new_message.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            }

            socketio.emit('new_message', content, broadcast=True)

            return ':3'
        elif message_content:
            new_message = Messages(content=message_content, user_id=current_user.id, type='text')
            db.session.add(new_message)
            db.session.commit()

            content = {
                'id': new_message.id,
                'username': current_user.username,
                'type': 'text',
                'content': new_message.content,
                'created_at': new_message.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            }

            socketio.emit('new_message', content, broadcast=True)

            return ':3'

    message_list = Messages.query.order_by(Messages.created_at.desc()).limit(100).all()
    messages = []
    for message in message_list:
        messages.append({
            'id': message.id,
            'username': message.users.username,
            'type': message.type,
            'content': message.content,
            'created_at': message.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        })
    return jsonify(messages)

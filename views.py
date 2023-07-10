from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from extensions import db
from models import Messages, Users
from events import socketio


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

        if not message_content:
            return jsonify({'error': 'Invalid message'}), 400

        new_message = Messages(content=message_content, user_id=current_user.id)
        db.session.add(new_message)
        db.session.commit()

        content = {
            'id': new_message.id,
            'content': new_message.content,
            'username': current_user.username,
            'created_at': new_message.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

        socketio.emit('new_message', content, broadcast=True)

        return ':3'
    else:
        messages = Messages.query.order_by(Messages.created_at.desc()).limit(100).all()

        messages_json = []

        for message in messages:
            messages_json.append({
                'id': message.id,
                'content': message.content,
                'username': message.users.username,
                'created_at': message.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })
        return jsonify(messages_json)

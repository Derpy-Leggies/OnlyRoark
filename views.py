from flask import Blueprint, render_template, request, jsonify, send_from_directory, abort
from flask_login import login_required, current_user
from extensions import db
from models import Messages, Users, Attachments
from events import socketio
from werkzeug.utils import secure_filename
from uuid import uuid4
import os
from config import UPLOADS_FOLDER
from utils.generate_image import generate_thumbnail


blueprint = Blueprint('views', __name__)


def format_response(data):
    message_content = {
        'id': data.id,
        'username': data.users.username,
        'message': data.message,
        'created_at': data.created_at.strftime('%Y-%m-%d %H:%M:%S'),
    }

    attachment_content = []
    for attachment in data.attachment:
        attachment_content.append({
            'file_name': attachment.file_name,
            'file_type': attachment.file_type,
        })

    return {'message': message_content, 'attachment': attachment_content}


@blueprint.route('/', methods=['GET'])
@login_required
def index():
    users = Users.query.all()
    return render_template('views/chatroom.html', users=users)


@blueprint.route('/uploads/<path:file_name>', methods=['GET'])
@login_required
def uploads(file_name):
    res = request.args.get("r", default=None, type=str)
    ext = request.args.get("e", default=None, type=str)

    # if no args are passed, return the raw file
    if not res and not ext:
        if not os.path.exists(os.path.join(UPLOADS_FOLDER, file_name)):
            abort(404)
        return send_from_directory(UPLOADS_FOLDER, file_name)

    # Generate thumbnail, if None is returned a server error occured
    thumb = generate_thumbnail(file_name, res, ext)
    if not thumb:
        abort(500)

    return send_from_directory(os.path.dirname(thumb), os.path.basename(thumb))


@blueprint.route('/message', methods=['GET', 'POST'])
@login_required
def message_list():
    if request.method == 'POST':
        message_form = request.form.get('message', '').strip()
        file_form = request.files.getlist('file[]')

        new_message = Messages(
            user_id=current_user.id,
            message=message_form,
        )

        print(new_message.message)

        db.session.add(new_message)
        db.session.commit()

        for file in file_form:
            file_extension = file.filename.split('.')[-1]

            if file_extension.lower() == "jpg":
                file_extension = "jpeg"

            file_name = uuid4().hex + '.' + file_extension
            original_file_name = secure_filename(file.filename)

            db.session.add(Attachments(
                message_id=new_message.id,
                original_file_name=original_file_name,
                file_name=file_name,
                file_type='image',
            ))

            file.save(f'uploads/{file_name}')

        db.session.commit()
        socketio.emit('new_message', format_response(new_message), broadcast=True)
        return ':3'

    offset = int(request.args.get('offset', 0))
    message_list = Messages.query.order_by(Messages.created_at.desc()).offset(offset).limit(50).all()

    messages = []
    for message in message_list:
        messages.append(format_response(message))

    return jsonify(messages)

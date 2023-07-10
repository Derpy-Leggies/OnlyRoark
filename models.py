from flask_login import UserMixin
from extensions import db


class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.String)
    attachment = db.relationship('Attachments', backref='messages', lazy=True)
    formatting = db.Column(db.String)

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.now(),
    )


class Attachments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(db.Integer, db.ForeignKey('messages.id'), nullable=False)

    original_file_name = db.Column(db.String)
    file_name = db.Column(db.String)
    file_type = db.Column(db.String)

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.now(),
    )


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    joined_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.now(),
    )

    messages = db.relationship('Messages', backref='users', lazy=True)

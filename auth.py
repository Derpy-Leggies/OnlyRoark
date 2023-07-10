from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from models import Users
from extensions import db
import re

blueprint = Blueprint('auth', __name__, url_prefix='/auth')


@blueprint.route('/', methods=['GET'])
def index():
    return render_template('views/auth.html')


@blueprint.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()
    errors = []

    user = Users.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        errors.append("Username or Password is incorrect!")

    if errors:
        for error in errors:
            flash(error)

    login_user(user, remember=True)

    flash("Welcome back!")
    return redirect(url_for('views.index'))


@blueprint.route("/register", methods=["POST"])
def register():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()
    confirm = request.form.get("confirm", "").strip()
    errors = []

    username_regex = re.compile(r"\b[A-Za-z0-9._-]+\b")

    # Validate the form
    if not username or not username_regex.match(username):
        errors.append("Username is invalid!")

    if not password:
        errors.append("Password is empty!")
    elif len(password) < 8:
        errors.append("Password is too short! Longer than 8 characters pls")

    if not confirm:
        errors.append("Enter password again!")
    elif confirm != password:
        errors.append("Passwords do not match!")

    user_exists = Users.query.filter_by(username=username).first()
    if user_exists:
        errors.append("User already exists!")

    if errors:
        for error in errors:
            flash(error)

    register_user = Users(
        username=username,
        password=generate_password_hash(password, method="scrypt"),
    )
    db.session.add(register_user)
    db.session.commit()

    return redirect(url_for("auth.index"))


@blueprint.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    flash("You have been logged out!")
    return redirect(url_for("views.index"))

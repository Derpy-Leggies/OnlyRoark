from flask_socketio import SocketIO
from flask_assets import Environment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


socketio = SocketIO()
assets = Environment()
db = SQLAlchemy()
migration = Migrate()
login_manager = LoginManager()

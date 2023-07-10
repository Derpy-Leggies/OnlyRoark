from flask import Flask
from extensions import assets, db, migration, login_manager
from views import blueprint as views_blueprint
from auth import blueprint as auth_blueprint
from flask_assets import Bundle
from models import Users
from events import socketio


app = Flask(__name__)
app.config.from_pyfile("config.py")


db.init_app(app)
migration.init_app(app, db)
login_manager.init_app(app)
assets.init_app(app)
socketio.init_app(app)

login_manager.login_view = 'auth.index'

js = Bundle(
    "js/*.js",
    filters="jsmin",
    output="gen/main.js",
    depends="js/*.js",
)
styles = Bundle(
    "sass/styles.sass",
    filters="libsass, cssmin",
    output="gen/styles.css",
    depends="sass/*.sass",
)
assets.register("js", js)
assets.register("styles", styles)

app.register_blueprint(views_blueprint)
app.register_blueprint(auth_blueprint)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.filter_by(id=user_id).first()


if __name__ == '__main__':
    socketio.run(app, async_mode='eventlet')

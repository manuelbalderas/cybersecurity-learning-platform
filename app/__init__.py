from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO, emit

from config import config

db = SQLAlchemy()
bcrypt = Bcrypt()
login = LoginManager()
socket = SocketIO()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    login.init_app(app)
    bcrypt.init_app(app)
    socket.init_app(app, cors_allowed_origins='*')

    login.login_view = 'auth.login'

    from .routes import auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .routes import challenges_blueprint
    app.register_blueprint(challenges_blueprint, url_prefix='/challenges')

    from .routes import courses_blueprint 
    app.register_blueprint(courses_blueprint, url_prefix='/courses')

    from .routes import chat_blueprint
    app.register_blueprint(chat_blueprint, url_prefix='/chat')

    from .routes import main_blueprint
    app.register_blueprint(main_blueprint)

    return app
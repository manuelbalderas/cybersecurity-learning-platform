from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO, emit

from config import config

db = SQLAlchemy()
bcrypt = Bcrypt()
login = LoginManager()
socket = SocketIO(cors_allowed_origins='*')

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    login.init_app(app)
    bcrypt.init_app(app)
    socket.init_app(app)

    login.login_view = 'auth_frontend_bp.login'

    from .routes.api import auth_api_bp
    app.register_blueprint(auth_api_bp, url_prefix='/api/auth')
    
    from .routes.frontend import auth_frontend_bp
    app.register_blueprint(auth_frontend_bp, url_prefix='/')

    from .routes.api import challenges_api_bp
    app.register_blueprint(challenges_api_bp, url_prefix='/api/challenges')
    
    from .routes.frontend import challenges_frontend_bp
    app.register_blueprint(challenges_frontend_bp, url_prefix='/challenges')
    
    from .routes.api import courses_api_bp
    app.register_blueprint(courses_api_bp, url_prefix='/api/courses')
    
    from .routes.frontend import courses_frontend_bp
    app.register_blueprint(courses_frontend_bp, url_prefix='/courses')
    
    from .routes.frontend import chat_frontend_bp
    app.register_blueprint(chat_frontend_bp, url_prefix='/chat')
    
    from .routes.frontend import main_frontend_bp
    app.register_blueprint(main_frontend_bp, url_prefix='/')
    
    return app
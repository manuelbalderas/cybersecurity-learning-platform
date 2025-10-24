from flask import flash
from flask_login import login_user, logout_user
from app import db, bcrypt
from app.models import User

class NotificationManager:
    @staticmethod
    def send_login_success():
        flash('¡Inicio de sesión exitoso!', 'success')
    
    @staticmethod
    def send_login_error():
        flash('Credenciales incorrectas', 'error')
    
    @staticmethod
    def send_logout_success():
        flash('Sesión cerrada correctamente', 'info')
    
    @staticmethod
    def send_already_logged_in():
        flash('Ya tienes una sesión activa', 'warning')
    
    @staticmethod
    def send_registration_success():
        flash('¡Usuario creado con éxito!', 'success')
    
    @staticmethod
    def send_registration_error():
        flash('El correo ya está registrado', 'error')
        
def process_login(email, password):
    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        login_user(user)
        user.check_and_reset_streak()
        db.session.commit()
        NotificationManager.send_login_success()
        return True
    NotificationManager.send_login_error()
    return False

def process_logout():
    logout_user()
    NotificationManager.send_logout_success()

def process_register(username, email, password):
    existing = User.query.filter_by(email=email).first()
    if existing:
        NotificationManager.send_registration_error()
        return False
        
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(username=username, email=email, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    login_user(user)
    NotificationManager.send_registration_success()
    return True
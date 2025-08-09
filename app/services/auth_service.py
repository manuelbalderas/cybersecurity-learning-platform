from flask_login import login_user, logout_user
from app import db, bcrypt
from app.models import User

def process_login(email, password):
    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        login_user(user)
        user.check_and_reset_streak()
        db.session.commit()
        return True, "Inicio de sesión exitoso"
    return False, "Inicio de sesión erroneo"

def process_logout():
    logout_user()

def process_register(username, email, password):
    existing = User.query.filter_by(email=email).first()
    if existing:
        return False, "El correo ya está registrado"
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(username=username, email=email, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return True, "Usuario creado con éxito"
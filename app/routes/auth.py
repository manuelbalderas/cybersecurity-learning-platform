from flask import Blueprint, render_template, redirect, flash, url_for
from flask_login import current_user, login_user, logout_user, login_required

from app import db, bcrypt
from app.models import User
from app.forms import LoginForm, RegisterForm


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email = email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            user.check_and_reset_streak()
            db.session.commit()
            flash("Inicio de sesión exitoso")
        else:
            flash("Inicio de sesión erroneo")
    
    return render_template('auth/login.html', form = form, page_title="Iniciar Sesión")

@auth.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email = email).first()
        if user is None:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            user = User(username=username, email=email, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash("Usuario creado con éxito.")
    our_users = User.query.order_by(User.date_added)
        
    return render_template('auth/register.html',
    our_users = our_users,
    form = form,
    page_title="Registro")

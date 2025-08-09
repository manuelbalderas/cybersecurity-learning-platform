from flask import Blueprint, render_template, redirect, flash, url_for
from flask_login import current_user, login_user, logout_user, login_required

from app.forms import LoginForm, RegisterForm
from app.services.auth_service import process_login, process_register, process_logout

auth_frontend_bp = Blueprint('auth_frontend', __name__)

@auth_frontend_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main_frontend.index'))

    form = LoginForm()
    if form.validate_on_submit():
        success, message = process_login(form.email.data, form.password.data)
        flash(message)
        if success:
            return redirect(url_for('main_frontend.index'))
    return render_template('auth/login.html', form=form, page_title="Iniciar Sesión")

@auth_frontend_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    process_logout()
    return redirect(url_for('main_frontend.index'))

@auth_frontend_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main_frontend.index'))

    form = RegisterForm()
    if form.validate_on_submit():
        sucess, message = process_register(
            form.username.data,
            form.email.data,
            form.password.data
        )
        flash(message)
        if sucess:
            return redirect(url_for('auth_frontend_bp.login'))
        
    return render_template('auth/register.html', form=form, page_title="Registro")
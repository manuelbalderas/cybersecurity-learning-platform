from flask import Blueprint, render_template

main_frontend_bp = Blueprint('main_frontend', __name__)

import pickle


@main_frontend_bp.route('/')
def index():
    return render_template('index.html', page_title='Potencia tus habilidades en ciberseguridad')

@main_frontend_bp.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy_policy.html', page_title="Política de Privacidad")
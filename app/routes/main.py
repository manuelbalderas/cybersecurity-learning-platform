from flask import Blueprint, render_template

main = Blueprint('main', __name__)

import pickle


@main.route('/')
def index():
    return render_template('index.html', page_title='Potencia tus habilidades en ciberseguridad')

@main.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy_policy.html', page_title="Política de Privacidad")
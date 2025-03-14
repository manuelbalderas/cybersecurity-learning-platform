from flask import Blueprint, render_template

from app.forms import PhishingValidatorForm

main = Blueprint('main', __name__)

import pickle


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy_policy.html')
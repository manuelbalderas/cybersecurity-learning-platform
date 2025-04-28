from flask import Blueprint, render_template, abort

from app.models import Challenge

challenges = Blueprint('challenges', __name__)

@challenges.route('/')
def index():
    return render_template('challenges/index.html', page_title="Retos")

@challenges.route('/<challenge_title>')
def get_challenges(challenge_title):
    challenge = Challenge.query.filter_by(alias=challenge_title).first()
    
    if challenge is None:
        abort(404)
    
    print(challenge.description)
    print(challenge.files)
    print(challenge.resources)
    print(challenge.flag)

    return render_template('challenges/challenge_detail.html', challenge=challenge, page_title=f"{challenge.title}")
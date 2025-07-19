from flask import Blueprint, render_template, abort, flash
from flask_login import current_user, login_required

from app.forms import FlagForm

from app.models import Challenge, UserChallenge
from app.models import Category

from app import db

challenges = Blueprint('challenges', __name__)

@challenges.route('/')
def index():
    challenges = Category.query.all()
    return render_template('challenges/index.html', challenges=challenges, page_title="Retos")

@challenges.route('overview/<category_alias>', methods=['GET'])
@login_required
def get_category(category_alias):
    category = Category.query.filter_by(alias=category_alias).first()
    
    if category is None:
        abort(404)
    
    challenges = Challenge.query.filter_by(category_id=category.id).all()
    
    return render_template('challenges/category.html', 
                           category=category, 
                           challenges=challenges, 
                           page_title=category.name)

@challenges.route('<challenge_title>', methods=['GET', 'POST'])
@login_required
def get_challenges(challenge_title):
    challenge = Challenge.query.filter_by(alias=challenge_title).first()
    
    user_challenge = UserChallenge.query.filter_by(user_id=current_user.id, challenge_id=challenge.id).first()
    
    if user_challenge:
        user_has_completed_challenge = True
        user_challenge_data = user_challenge  # To access score and completed_at
    else:
        user_has_completed_challenge = False
        user_challenge_data = None

    
    if challenge is None:
        abort(404)
    
    form = FlagForm()
    if form.validate_on_submit() and not user_has_completed_challenge:
        flag = form.flag.data
        print(flag)
        if flag == challenge.flag:
            user_challenge = UserChallenge(
                user_id=current_user.id,
                challenge_id=challenge.id,
                # score=100  # Or whatever score the user achieved
            )
            db.session.add(user_challenge)
            db.session.commit()
            flash("Correcto")
            
        else: 
            flash("Error! los sandwitches eran de huevo")
            print("Try again")
            
    return render_template('challenges/challenge_detail.html', 
                           challenge=challenge,
                           form=form,
                           user_has_completed_challenge=user_has_completed_challenge,
                           user_challenge=user_challenge_data,
                           page_title=challenge.title)

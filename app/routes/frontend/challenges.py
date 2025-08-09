from flask import Blueprint, render_template, abort, flash
from flask_login import current_user, login_required
from app.forms import FlagForm
from app.services.challenge_service import get_challenge_by_alias, get_user_challenge, submit_flag

challenges_frontend_bp = Blueprint('challenges_frontend', __name__)

@challenges_frontend_bp.route('<challenge_title>', methods=['GET', 'POST'])
@login_required
def get_challenges(challenge_title):
    challenge = get_challenge_by_alias(challenge_title)
    if challenge is None:
        abort(404)
    
    user_challenge = get_user_challenge(current_user.id, challenge.id)
    user_has_completed_challenge = user_challenge is not None
    
    form = FlagForm()
    if form.validate_on_submit() and not user_has_completed_challenge:
        success, message = submit_flag(current_user, challenge, form.flag.data)
        print(success, message)
        flash(message)
        if success:
            user_has_completed_challenge = True
            user_challenge = get_user_challenge(current_user.id, challenge.id)
    
    return render_template(
        "challenges/challenge_detail.html",
        challenge=challenge,
        form=form,
        user_has_completed_challenge=user_has_completed_challenge,
        user_challenge=user_challenge,
        page_title=challenge.title
    )
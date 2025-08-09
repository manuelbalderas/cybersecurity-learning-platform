from app import db
from app.models import Challenge, UserChallenge 

def get_challenge_by_alias(alias):
    return Challenge.query.filter_by(alias=alias).first()

def get_user_challenge(user_id, challenge_id):
    return UserChallenge.query.filter_by(
        user_id=user_id,
        challenge_id=challenge_id
    ).first()
    
def submit_flag(user, challenge, flag):
    print(flag)
    print(challenge.flag)
    if flag == challenge.flag:
        user_challenge = UserChallenge(
            user_id=user.id,
            challenge_id=challenge.id,
        )
        db.session.add(user_challenge)
        if not user.has_done_streak_today:
            user.update_streak()
        db.session.commit()
        return True, "Correcto"
    else:
        return False, "Error! los sandwitches eran de huevo"
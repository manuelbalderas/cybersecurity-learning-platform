from app import db
from flask import flash
from app.models import Challenge, UserChallenge 

def get_challenge_by_alias(alias):
    return Challenge.query.filter_by(alias=alias).first()

def get_user_challenge(user_id, challenge_id):
    return UserChallenge.query.filter_by(
        user_id=user_id,
        challenge_id=challenge_id
    ).first()
    
def submit_flag(user, challenge, flag):
    # Verificar si el flag no es None
    if flag is None:
        flash('Flag no puede estar vacía', 'error')
        return False
    
    print(f"Flag enviada: {flag}")
    print(f"Flag correcta: {challenge.flag}")
    
    if flag.strip().lower() == challenge.flag.strip().lower():
        user_challenge = UserChallenge(
            user_id=user.id,
            challenge_id=challenge.id,
        )
        db.session.add(user_challenge)
        if not user.has_done_streak_today:
            user.update_streak()
        db.session.commit()
        flash('¡Reto completado correctamente!', 'success')
        return True
    else:
        flash('Flag incorrecta', 'error')
        return False
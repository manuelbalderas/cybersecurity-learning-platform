from flask import Blueprint, request, jsonify, abort
from flask_login import login_required, current_user
from app.services.challenge_service import get_challenge_by_alias, get_user_challenge, submit_flag

challenges_api_bp = Blueprint("challenges_api", __name__)

@challenges_api_bp.route("/<challenge_title>", methods=["GET"])
@login_required
def api_get_challenge(challenge_title):
    challenge = get_challenge_by_alias(challenge_title)
    if challenge is None:
        abort(404)

    user_challenge = get_user_challenge(current_user.id, challenge.id)
    return jsonify({
        "id": challenge.id,
        "title": challenge.title,
        "alias": challenge.alias,
        "completed": bool(user_challenge),
        "score": getattr(user_challenge, "score", None)
    })

@challenges_api_bp.route("/<challenge_title>/submit", methods=["POST"])
@login_required
def api_submit_flag(challenge_title):
    data = request.json
    challenge = get_challenge_by_alias(challenge_title)
    if challenge is None:
        abort(404)

    success, message = submit_flag(current_user, challenge, data.get("flag"))
    return jsonify({"success": success, "message": message})

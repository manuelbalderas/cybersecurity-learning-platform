from flask import Blueprint, render_template
from flask_login import login_required

chat_frontend_bp = Blueprint("chat_frontend", __name__)

@chat_frontend_bp.route("/")
@login_required
def index():
    return render_template('chat/index.html', page_title="Chat con Pwnie")
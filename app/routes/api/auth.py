from flask import Blueprint, request, jsonify
from flask_login import login_required
from app.services.auth_service import process_login, process_register, process_logout

auth_api_bp = Blueprint('auth_api', __name__)

@auth_api_bp.route('/login', methods=['POST'])
def api_login():
    data = request.get_json()
    success, message = process_login(data.get('email'), data.get('password'))
    return jsonify({'success': success, 'message': message})

@auth_api_bp.route('/logout', methods=['POST'])
@login_required
def api_logout():
    process_logout()
    return jsonify({'success': True, 'message': 'Sesión cerrada con éxito.'})

@auth_api_bp.route('/register', methods=['POST'])
def api_register():
    data = request.get_json()
    success, message = process_register(
        data.get('username'),
        data.get('email'),
        data.get('password')
    )
    return jsonify({'success': success, 'message': message})
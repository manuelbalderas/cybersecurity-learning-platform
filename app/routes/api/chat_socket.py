from flask_login import current_user
from flask_socketio import emit
from flask import request, flash
from app import socket, db
from app.services.chat_service import process_chat_message, is_message_educational
from app.models import User

print("Chat socket initialized!")

@socket.on('connect')
def handle_connect():
    print(f'Client connected on worker {id(socket)}!')

@socket.on('disconnect')
def handle_disconnect():
    print('Client disconnected!')

@socket.on('message')
def handle_message(data):
    message = data.get('message')
    user_id = data.get('user_id')

    print(f"[Socket] Received message: {message}")

    user = User.query.get(user_id) if user_id else None

    if user and not user.has_done_streak_today and is_message_educational(message):
        user.update_streak()
        db.session.commit()
        flash("¡Has completado tu racha diaria! 🎉", "success")
        emit('streak_update', {'user_id': user_id, 'new_streak': user.current_streak})

    response = process_chat_message(user_id, message)
    emit("response", response, broadcast=True)#, namespace='/chat')
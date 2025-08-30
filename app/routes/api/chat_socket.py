from flask_login import current_user
from flask_socketio import emit
from flask import request, flash
from app import socket, db
from app.services.chat_service import process_chat_message, is_message_educational

print("Chat socket initialized!")

@socket.on('connect')
def handle_connect():
    print(f'Client connected on worker {id(socket)}!')

@socket.on('disconnect')
def handle_disconnect():
    print('Client disconnected!')

@socket.on('message')
def handle_message(message):
    user_id = str(current_user.id) if current_user.is_authenticated else None

    if not current_user.has_done_streak_today and is_message_educational(message):
        current_user.update_streak()
        db.session.commit()
        
        flash("¡Has completado tu racha diaria! 🎉", "success")
        # emit('streak_update', {'has_done_streak_today': current_user.has_done_streak_today}, room=request.sid)
        # print(f"User {current_user.username} has done their streak today! Streak: {current_user.has_done_streak_today}")

    response = process_chat_message(user_id, message)
    emit("response", response, broadcast=True)#, namespace='/chat')
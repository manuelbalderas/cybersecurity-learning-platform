from flask_login import current_user
from flask_socketio import emit
from app import socket, db
from app.services.chat_service import process_chat_message, predict_flag_relevance

print("Chat socket initialized!")

@socket.on('connect')
def handle_connect():
    print('Client connected!')

@socket.on('disconnect')
def handle_disconnect():
    print('Client disconnected!')

@socket.on('message')
def handle_message(message):
    user_id = str(current_user.id) if current_user.is_authenticated else None

    if not current_user.has_done_streak_today and predict_flag_relevance(message):
        current_user.update_streak()
        db.session.commit()

    response = process_chat_message(user_id, message)
    emit("response", response)

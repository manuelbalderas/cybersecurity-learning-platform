from flask import Blueprint, request, jsonify, render_template
from flask_socketio import emit, join_room

import ollama

from app import socket

chat = Blueprint('chat', __name__)

@socket.on('connect')
def handle_connect():
    print('Client connected!')

@socket.on('disconnect')
def handle_disconnect():
    print('Client disconnected!')

@socket.on("message")
def handle_message(message):
    print(f"User: {message}")

    # Generate a response using Ollama
    response = ollama.chat(model="llama3.1:8b", messages=[{"role": "user", "content": f'your name is Pwnie, you are an artificial intelligence developed for helping in solving cibersecurity questions for ethical alumnees. Answer the follow message: {message}'}])
    bot_reply = response["message"]["content"]

    emit("response", bot_reply)  # Send response back to the frontend
    print(f"Bot: {bot_reply}")

@chat.route('/')
def index():
    return render_template('chat/index.html')
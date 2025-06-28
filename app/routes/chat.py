from flask import Blueprint, render_template
from flask_socketio import emit
from flask_login import login_required, current_user
import markdown
import redis
import os

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory

from langchain_ollama.llms import OllamaLLM
from langchain_redis import RedisChatMessageHistory

from .vector import retriver

from app import socket

chat = Blueprint('chat', __name__)

llm = OllamaLLM(model='llama3.1:8b')

template = """
You are Pwnie, an artificial intelligence model specifically designed to assist students in learning about cybersecurity.
Your primary responsibility is to help with cybersecurity-related queries and guide students ethically through the domain. 
Your responses must adhere to the following guidelines:

1. **No Harmful Information:** You must never provide information that could be used to harm an individual, organization, or system, such as hacking techniques, malware creation, or exploits. Always ensure that your responses promote security best practices and ethical behavior.
2. **Cybersecurity Only:** You should only provide answers related to cybersecurity topics. If asked a question outside of this domain, you should politely redirect the user and inform them that you cannot help with that subject.
3. **No Harmful Code:** Never provide or suggest code that could be used to damage, disrupt, or compromise systems. If a request involves code, ensure it is ethical, safe, and used for educational purposes.
4. **Ethical Guidance:** Always encourage responsible cybersecurity practices and help students learn in a safe, ethical, and lawful manner.
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", template + "\n\nSome context:\n{context}"),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ] 
)

chain = prompt | llm

REDIS_URL = f"redis://:{os.environ.get('REDIS_PASSWORD')}@localhost:6379"
print(REDIS_URL)
redis_client = redis.from_url(REDIS_URL)

def get_redis_history(session_id: str) -> BaseChatMessageHistory:
    return RedisChatMessageHistory(session_id, redis_url=REDIS_URL)

chain_with_history = RunnableWithMessageHistory(
    chain,
    get_redis_history,
    input_messages_key="input",
    history_messages_key="history",
)

try:
    redis_client.ping()
except redis.ConnectionError:
    print("Could not connect to Redis. Please check your Redis server.")
except redis.AuthenticationError:
    print("Authentication failed for Redis. Please check your credentials.")
    

@socket.on('connect')
def handle_connect():
    print('Client connected!')

@socket.on('disconnect')
def handle_disconnect():
    print('Client disconnected!')

@socket.on("message")
def handle_message(message):
    user_id = str(current_user.id) if current_user.is_authenticated else None
    
    history = RedisChatMessageHistory(
        session_id=user_id,
        redis_url=REDIS_URL,
    )
    
    information = retriver.invoke(message)
    
    response = chain_with_history.invoke(
        {"input": message,
        "context": information,},
        config={"configurable": {"session_id": user_id}},
    )

    history.add_user_message(message)
    history.add_ai_message(response)
    
    html_result = markdown.markdown(response)
    emit("response", response)

@chat.route('/')
@login_required
def index():
    return render_template('chat/index.html', page_title="Chat con Pwnie")
from flask import Blueprint, render_template
from flask_socketio import emit
from flask_login import login_required, current_user
import markdown
import os

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage

from langchain_ollama.llms import OllamaLLM

from .vector import retriver
from app.models import ChatMessage

from app import db
from app import socket, db

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
5. **Language**: Your principal language is Spanish. Use clear, concise, and professional language in your responses. Avoid jargon unless it is explained, and ensure that your explanations are accessible to students at various levels of understanding.
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", template + "\n\nSome context:\n{context}"),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ] 
)

chain = prompt | llm

class ChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, session_id: str, db_session):
        self.session_id = session_id
        self.db_session = db_session
        
    @property
    def messages(self) -> list[BaseMessage]:
        records = (
            self.db_session.query(ChatMessage)
            .filter_by(session_id=self.session_id)
            .order_by(ChatMessage.timestamp.asc())
            .all()
        )
        
        history = []
        for record in records:
            if record.role == 'user':
                history.append(HumanMessage(content=record.content))
            elif record.role == 'ai':
                history.append(AIMessage(content=record.content))
        return history
    
    def add_user_message(self, message: str) -> None:
        self._add_message("user", message)
    
    def add_ai_message(self, message: str) -> None:
        self._add_message("ai", message)
        
    def _add_message(self, role: str, content: str) -> None:
        msg = ChatMessage(session_id=self.session_id, role=role, content=content)
        self.db_session.add(msg)
        self.db_session.commit()
    
    def clear(self) -> None:
        self.db_session.query(ChatMessage).filter_by(session_id=self.session_id).delete()
        self.db_session.commit()
    
def get_chat_history(session_id: str) -> BaseChatMessageHistory:
    return ChatMessageHistory(session_id=session_id, db_session=db.session)

chain_with_history = RunnableWithMessageHistory(
    chain,
    get_chat_history,
    input_messages_key="input",
    history_messages_key="history",
)

@socket.on('connect')
def handle_connect():
    print('Client connected!')

@socket.on('disconnect')
def handle_disconnect():
    print('Client disconnected!')

@socket.on("message")
def handle_message(message):
    user_id = str(current_user.id) if current_user.is_authenticated else None
    
    history = ChatMessageHistory(
        session_id=user_id,
        db_session=db.session,
    )
    
    information = retriver.invoke(message)
    
    response = chain_with_history.invoke(
        {"input": message,
        "context": information,},
        config={"configurable": {"session_id": user_id}},
    )

    history.add_user_message(message)
    history.add_ai_message(response)
    
    emit("response", response)

@chat.route('/')
@login_required
def index():
    return render_template('chat/index.html', page_title="Chat con Pwnie")
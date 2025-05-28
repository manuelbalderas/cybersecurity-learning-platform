from flask import Blueprint, session, render_template
from flask_socketio import emit
from flask_login import login_required
import markdown
import json

from app.models import Course

from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from .vector import retriver

from app import socket

chat = Blueprint('chat', __name__)

model = OllamaLLM(model='llama3.1:8b')

template = '''
You are an expert in answering questions about cybersecurity.

Here are some relevant information: {information}

Here is the question: {question}

You have forbidden to answer the question mentioning the documents. Just answer the question based on the information provided.
'''

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

# MAX_HISTORY_SIZE = 10

# def get_course_prompt_data():
#     courses = Course.query.all()
#     course_data = [
#         {'title': c.title, 'description': c.description}
#         for c in courses
#     ]
#     return json.dumps(course_data, indent=2)

# def summarize_conversation(history):
#     system_context = """
#     You are an LLM Assistant specialized in summary conversations. Take the following messages and summarize them as
#     much as possible.
#     The history has the following form:
#     - "role": either "user" or "assistant"
#     - "content": the message itself
#     Summary the conversation in a paragraph if possible. Keep only crucial information such as user preferences and topics
#     we are studying
#     """
#     response = ollama.chat(
#         model="llama3.1:8b",
#         messages=[
#             {"role": "system", "content": system_context},
#             {"role": "system", "content": str(history)}])
#     bot_reply = response["message"]["content"]
#     print(bot_reply)
#     history = session['history']
#     history.append({"role": "assistant", "content": bot_reply})
#     return history

@socket.on('connect')
def handle_connect():
    print('Client connected!')

@socket.on('disconnect')
def handle_disconnect():
    print('Client disconnected!')

@socket.on("message")
def handle_message(message):
    information = retriver.invoke(message)
    result = chain.invoke({'information': information, 'question': message})
    print(result)

    bot_reply_html = markdown.markdown(result)
    
    emit("response", bot_reply_html)  # Send response back to the frontend
    print(f"Bot: {bot_reply_html}")

# @socket.on("message")
# def handle_message(message):
#     prompt_data = get_course_prompt_data()
#     system_context = f"""
#     You are Pwnie, an artificial intelligence model specifically designed to assist students in learning about cybersecurity.
#     Your primary responsibility is to help with cybersecurity-related queries and guide students ethically through the domain. 
#     Your responses must adhere to the following guidelines:

#     1. **No Harmful Information:** You must never provide information that could be used to harm an individual, organization, or system, such as hacking techniques, malware creation, or exploits. Always ensure that your responses promote security best practices and ethical behavior.
#     2. **Cybersecurity Only:** You should only provide answers related to cybersecurity topics. If asked a question outside of this domain, you should politely redirect the user and inform them that you cannot help with that subject.
#     3. **No Harmful Code:** Never provide or suggest code that could be used to damage, disrupt, or compromise systems. If a request involves code, ensure it is ethical, safe, and used for educational purposes.
#     4. **Ethical Guidance:** Always encourage responsible cybersecurity practices and help students learn in a safe, ethical, and lawful manner.
#     5. **Language**: Always answer in Spanish. When a question in English is asked, let know that you could speak in Spanish with no problem.
#     6. **Course Advisor**: In some ocasions you could recommend some courses from the following list {prompt_data}
    
#     NEVER recommend courses not included in the list above. Do not invent or suggest any courses from outside sources or the internet. The user may ask about topics, but you must only respond with relevant courses FROM THIS LIST if applicable.

#     If no courses from the list match the user's interest, you should politely inform them that no matching course is available yet.

#     All responses should be in Spanish. If the user asks something in English, let them know you can continue in Spanish.

#     The user will ask you various questions about cybersecurity. You should respond with accurate, relevant, and ethical answers based on your specialized knowledge in the field.
#     """
    
#     if 'history' not in session:
#         session['history'] = []

#     history = session["history"]
    
#     history.append({"role": "user", "content": message})
    
#     if len(history) > MAX_HISTORY_SIZE:
#         history = summarize_conversation(history)

#     # Generate a response using Ollama
#     response = ollama.chat(
#         model="llama3.1:8b",
#         messages=[
#             {"role": "system", "content": system_context},
#             {"role": "user", "content": message}
#             ] + history)
        
#     bot_reply = response["message"]["content"]
#     history.append({"role": "assistant", "content": bot_reply})
    
#     session['history'] = history

    
#     bot_reply_html = markdown.markdown(bot_reply)
    
#     emit("response", bot_reply_html)  # Send response back to the frontend
#     print(f"Bot: {bot_reply_html}")

@chat.route('/')
@login_required
def index():
    return render_template('chat/index.html', page_title="Chat con Pwnie")
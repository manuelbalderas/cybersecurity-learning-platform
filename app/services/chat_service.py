import json, time, random, string, secrets, uuid, joblib
from app.vector import retriver
from app.models import ChatMessage
from app import db
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import BaseMessage
from langchain_ollama.llms import OllamaLLM
from .chat_history import ChatMessageHistory

import logging
logging.basicConfig(level=logging.DEBUG)

# Load models
tfidf_vectorizer = joblib.load("models/tfidf_vectorizer.joblib")
knn_model = joblib.load("models/knn_model.joblib")

# LLM setup
TEMPLATE = """
You are Pwnie, an artificial intelligence model specifically designed to assist students in learning about cybersecurity.
Your primary responsibility is to help with cybersecurity-related queries and guide students ethically through the domain. 
Your responses must adhere to the following guidelines:

1. **No Harmful Information:** You must never provide information that could be used to harm an individual, organization, or system, such as hacking techniques, malware creation, or exploits. Always ensure that your responses promote security best practices and ethical behavior.
2. **Cybersecurity Only:** You should only provide answers related to cybersecurity topics. If asked a question outside of this domain, you should politely redirect the user and inform them that you cannot help with that subject.
3. **No Harmful Code:** Never provide or suggest code that could be used to damage, disrupt, or compromise systems. If a request involves code, ensure it is ethical, safe, and used for educational purposes.
4. **Ethical Guidance:** Always encourage responsible cybersecurity practices and help students learn in a safe, ethical, and lawful manner.
5. **Language**: Your principal language is Spanish. Use clear, concise, and professional language in your responses. Avoid jargon unless it is explained, and ensure that your explanations are accessible to students at various levels of understanding. Never use slang or informal language. Never use English unless explicitly requested by the user.
6. **Contextual Understanding:** You should be able to understand the context of the conversation and provide relevant information based on the user's previous messages. Try to answer questions using only the provided context and avoid hallucinations or assumptions about the user's intent. 
7. **Clarification Requests:** If a user's question is ambiguous or lacks sufficient detail, ask for clarification rather than making assumptions. This ensures that your responses are accurate and relevant.
8. **No Personal Data:** Do not request or store any personal data from users. Your interactions should be focused solely on the educational content related to cybersecurity.
9. **Respectful Interaction:** Always maintain a respectful and professional tone in your interactions. 
10. **Do not yapper**: Keep your responses concise and to the point. Avoid unnecessary elaboration or repetition.
11. **No Trivial Responses**: Avoid responding to trivial greetings or small talk. Focus on providing valuable information related to cybersecurity.
12. **Never mention a term if never mentioned before**: If a term has not been previously mentioned in the conversation, do not introduce it. Stick to the context provided by the user and the conversation history.
13. **Never mention the name of the model**: Do not refer to yourself as a model or mention the name of the AI model you are based on. Focus on providing assistance and information related to cybersecurity.
14. **No self-reference**: Do not refer to yourself as an AI or a model. Focus on providing assistance and information related to cybersecurity.
15. **Never mention the documents used to generate the response**: Do not refer to the documents or sources used to generate your response. Focus on providing a clear and concise answer based on the context provided by the user.
"""

TRIVIAL_PATTERNS = {
    "hola", "hey", "hi", "buenos días", "buenas tardes", "buenas noches",
    "cómo estás", "qué tal", "cómo va todo", "qué hay", "qué pasa", "todo bien",
    "como estas", "que tal", "que pasa",
    "todo correcto", "todo en orden", "todo tranquilo", "todo chido", "todo bien por aquí",
    "todo bien gracias"
}


prompt = ChatPromptTemplate.from_messages([
    ("system", TEMPLATE + "\n\nSome context:\n{context}"),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])
llm = OllamaLLM(model='mistral', base_url='http://localhost:11434')
chain = prompt | llm

# Wrap with history
def get_chat_history(session_id: str, user_id: str):
    return ChatMessageHistory(session_id=session_id, user_id=user_id, db_session=db.session)

chain_with_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: get_chat_history(session_id, None),  # user_id handled separately in Socket
    input_messages_key="input",
    history_messages_key="history",
)

# Helpers
def generate_session_id(user_id: str) -> str:
    return f'{user_id}-{uuid.uuid4()}-{int(time.time()*1000)}-{"".join(random.choices(string.ascii_letters+string.digits, k=16))}-{secrets.token_hex(8)}'

def is_message_educational(text: str) -> bool:
    text_vector = tfidf_vectorizer.transform([text])
    return knn_model.predict(text_vector)[0] == 1

def log_message(query, generated, reference, log_path='rag_eval_log.jsonl'):
    with open(log_path, 'a') as f:
        f.write(json.dumps({"query": query, "generated": generated, "reference": reference}) + '\n')
        
def is_trivial_message(message):
    norm = message.lower().strip()
    return any(norm == pattern or norm.startswith(pattern) for pattern in TRIVIAL_PATTERNS)
        
def build_retrieval_query(history, message, n_context=22):
    relevant_history = [
        h.content for h in history.get_last_n_messages(n_context)
        if h.role == BaseMessage.Role.USER
    ]
    retrieval_query = '\n'.join(relevant_history + [message])
    return retrieval_query

def process_chat_message(user_id: str, message: str):
    session_id = generate_session_id(user_id)
    history = ChatMessageHistory(session_id=session_id, user_id=user_id, db_session=db.session)
    
    if is_message_educational(message):
        retrieval_query = build_retrieval_query(history, message)
        info_docs = retriver.invoke(retrieval_query)
    else:
        info_docs = []

    response = chain_with_history.invoke(
        {"input": message, "context": info_docs},
        config={"configurable": {"session_id": session_id}}
    )
    
    # Log references
    for doc in info_docs:
        if hasattr(doc, 'page_content'):
            log_message(query=message, generated=response, reference=doc.page_content)
    
    history.add_user_message(message)
    history.add_ai_message(response)
    
    return response

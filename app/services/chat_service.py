import json, time, random, string, secrets, uuid, joblib
from app.vector import retriver
from app.models import ChatMessage
from app import db
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import BaseMessage
from langchain_ollama.llms import OllamaLLM
from .chat_history import ChatMessageHistory

# Load models
tfidf_vectorizer = joblib.load("models/tfidf_vectorizer.joblib")
knn_model = joblib.load("models/knn_model.joblib")

# LLM setup
TEMPLATE = """
You are Pwnie, an artificial intelligence model specifically designed to assist students in learning about cybersecurity.
[... your guidelines here ...]
"""
prompt = ChatPromptTemplate.from_messages([
    ("system", TEMPLATE + "\n\nSome context:\n{context}"),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])
llm = OllamaLLM(model='mistral')
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

def predict_flag_relevance(text: str) -> bool:
    text_vector = tfidf_vectorizer.transform([text])
    return knn_model.predict(text_vector)[0] == 1

def log_message(query, generated, reference, log_path='rag_eval_log.jsonl'):
    with open(log_path, 'a') as f:
        f.write(json.dumps({"query": query, "generated": generated, "reference": reference}) + '\n')

def process_chat_message(user_id: str, message: str):
    session_id = generate_session_id(user_id)
    history = ChatMessageHistory(session_id=session_id, user_id=user_id, db_session=db.session)
    
    info_docs = retriver.invoke(message)
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

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
from app.models import ChatMessage

class ChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, session_id: str, user_id: str, db_session):
        self.session_id = session_id
        self.user_id = user_id
        self.db_session = db_session

    @property
    def messages(self):
        records = (self.db_session.query(ChatMessage)
                   .filter_by(session_id=self.session_id)
                   .order_by(ChatMessage.timestamp.asc())
                   .all())
        history = []
        for r in records:
            if r.role == 'user':
                history.append(HumanMessage(content=r.content))
            elif r.role == 'ai':
                history.append(AIMessage(content=r.content))
        return history
    
    def get_last_n_messages(self, n: int):
        records = (self.db_session.query(ChatMessage)
                   .filter_by(session_id=self.session_id)
                   .order_by(ChatMessage.timestamp.desc())
                   .limit(n)
                   .all())
        history = []
        for r in reversed(records):
            if r.role == 'user':
                history.append(HumanMessage(content=r.content))
            elif r.role == 'ai':
                history.append(AIMessage(content=r.content))
        return history

    def add_user_message(self, message: str):
        self._add_message("user", message)

    def add_ai_message(self, message: str):
        self._add_message("ai", message)

    def _add_message(self, role, content):
        msg = ChatMessage(user_id=self.user_id, session_id=self.session_id, role=role, content=content)
        self.db_session.add(msg)
        self.db_session.commit()

    def clear(self):
        self.db_session.query(ChatMessage).filter_by(session_id=self.session_id).delete()
        self.db_session.commit()
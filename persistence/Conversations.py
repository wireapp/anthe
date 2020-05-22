from sqlalchemy import Column, String

from persistence.Db import db


class Conversation(db.Model):
    __tablename__ = 'conversations'

    conversation_id = Column(String(255), primary_key=True, nullable=False)
    bot_id = Column(String(255), nullable=False)
    token = Column(String(255), nullable=False)

    def __init__(self, conversation_id: str, bot_id: str, token: str):
        self.conversation_id = conversation_id
        self.bot_id = bot_id
        self.token = token

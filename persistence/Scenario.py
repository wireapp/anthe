from typing import List

from sqlalchemy import Column, Integer, String, Table, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from persistence.Conversations import Conversation
from persistence.Db import db

Base = declarative_base()
association_table = Table(
    'scenario_conversation', Base.metadata,
    Column('scenarios_id', Integer, ForeignKey('scenarios.id')),
    Column('conversation_id', Integer, ForeignKey('conversations.conversation_id'))
)


class Scenario(db.Model):
    __tablename__ = 'scenarios'

    id = Column(Integer, primary_key=True, autoincrement=True)
    scenario_name = Column(String, nullable=False)
    bot_under_test = Column(String, nullable=False)
    conversations = relationship("Conversation", secondary=association_table)
    __table_args__ = (
        UniqueConstraint('scenario_name', 'bot_under_test', name='_name_bot_uc'),
    )

    def __init__(self, scenario_name: str, bot_under_test: str, conversations: List[Conversation] = None):
        self.scenario_name = scenario_name
        self.bot_under_test = bot_under_test
        self.conversations = conversations if conversations else []

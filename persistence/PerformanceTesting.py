from flask_sqlalchemy import Model
from sqlalchemy import func, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship


class PerformanceTesting(Model):
    __tablename__ = 'performance_testing'

    id = Column(Integer, primary_key=True, autoincrement=True)
    bot_under_test = Column(String(255), nullable=False)
    start = Column(DateTime(timezone=True), server_default=func.now())
    end = Column(DateTime(timezone=True), nullable=True)

    records = relationship('PerformanceRecord')

    def __init__(self, bot_under_test: str):
        self.bot_under_test = bot_under_test

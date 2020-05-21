from flask_sqlalchemy import Model
from sqlalchemy import ForeignKey, Integer, Column, String, DateTime


class PerformanceRecord(Model):
    __tablename__ = 'performance_record'

    id = Column(Integer, primary_key=True, autoincrement=True)
    performance_testing_id = Column(Integer, ForeignKey('performance_testing.id'), nullable=False)

    message = Column(String(255), nullable=False)
    start = Column(DateTime(timezone=True), nullable=False)
    end = Column(DateTime(timezone=True), nullable=True)

    def __init__(self, message: str, start):
        self.message = message
        self.start = start

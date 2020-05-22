from sqlalchemy import ForeignKey, Integer, Column, String, Boolean, Float

from persistence.Db import db


class PerformanceRecord(db.Model):
    __tablename__ = 'performance_record'

    id = Column(Integer, primary_key=True, autoincrement=True)
    performance_testing_id = Column(Integer, ForeignKey('performance_testing.id'), nullable=False)

    message = Column(String(255), nullable=False)
    received_valid = Column(Boolean, nullable=False)
    response_time = Column(Float, nullable=False)

    def __init__(self, message: str, valid: bool, response_time: float):
        self.message = message
        self.received_valid = valid
        self.response_time = response_time

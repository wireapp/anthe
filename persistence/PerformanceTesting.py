from datetime import datetime
from typing import List

from sqlalchemy import func, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from persistence.Db import db
from persistence.PerformanceRecord import PerformanceRecord


class PerformanceTesting(db.Model):
    __tablename__ = 'performance_testing'

    id = Column(Integer, primary_key=True, autoincrement=True)
    bot_under_test = Column(String(255), nullable=False)
    start = Column(DateTime(timezone=True), server_default=func.now())
    end = Column(DateTime(timezone=True), nullable=True)

    records = relationship('PerformanceRecord')

    def __init__(self, bot_under_test: str, start: datetime, end: datetime, records: List[PerformanceRecord] = None):
        self.bot_under_test = bot_under_test
        self.start, self.end = start, end
        if records:
            self.records.extend(records)

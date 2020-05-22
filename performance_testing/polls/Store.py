import logging
from datetime import datetime
from typing import Optional, List

from extensions.AtomicCounter import AtomicCounter
from performance_testing.polls.Storage import Storage
from persistence.Db import db
from persistence.PerformanceRecord import PerformanceRecord
from persistence.PerformanceTesting import PerformanceTesting

logger = logging.getLogger(__name__)

store: Optional[Storage] = None
"""
Stores current instance of testing
"""

timestamp = Optional[datetime] = None
"""
Timestamp when this started.
"""

counter = AtomicCounter(0)
"""
Count of processes using this store.
"""


def poll_received(name: str, buttons: List[str]):
    """
    Registers received poll.
    """
    if store:
        logger.info(f'Poll {name} received')
        store.poll_received(name, buttons)
    else:
        logger.info(f'No execution is running right now. Ignoring received poll.')


def new_poll(name: str, buttons: List[str]):
    """
    Inserts new poll to store.
    """
    if store:
        store.new_poll(name, buttons)
    else:
        raise Exception('It is not possible to insert poll before executing init_storage.')


def init_store():
    """
    Create new storage
    """
    counter.increment()
    if counter.compare(1):
        global store, timestamp
        store, timestamp = Storage(), datetime.utcnow()


# noinspection PyTypeChecker
def release_store() -> Optional[Storage]:
    """
    Sets storage to None and returns it past value
    """
    counter.decrement()
    global store, timestamp
    if counter.compare(0):
        s, t = store, timestamp
        store, timestamp = None, None
        move_to_db(s, t, datetime.utcnow())
        return s
    else:
        return store


def move_to_db(store: Storage, start: datetime, end: datetime):
    """
    Stores store in the database.
    """
    logger.info('Saving store to database')

    records = [PerformanceRecord(
        message=poll.name,
        valid=poll.received_valid,
        response_time=(poll.request_sent - poll.poll_received).total_seconds()
    ) for poll in store.storage.values()]
    testing = PerformanceTesting(bot_under_test='polls', start=start, end=end, records=records)

    db.session.add(testing)
    db.session.commit()
    logger.info('Performance testing saved')

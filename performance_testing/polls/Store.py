import logging
from typing import Optional, List

from performance_testing.polls.Storage import Storage

logger = logging.getLogger(__name__)

store: Optional[Storage] = None
"""
Stores current instance of testing
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


def init_storage():
    """
    Create new storage
    """
    global store
    store = Storage()


def destroy_storage() -> Optional[Storage]:
    """
    Sets storage to None and returns it past value
    """
    global store
    s = store
    store = None
    return s

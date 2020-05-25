import logging
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Dict

logger = logging.getLogger(__name__)


@dataclass
class Poll:
    """
    One poll record.
    """

    name: str
    buttons: List[str]
    """
    Sorted list of buttons that should be created
    """
    request_sent: datetime

    poll_received: Optional[datetime] = None
    received_valid: bool = False


class Storage:
    """"
    Class temporary storing data in memory during the performance testing.
    """

    def __init__(self):
        self.storage: Dict[str, Poll] = {}

    def new_poll(self, name: str, buttons: List[str]):
        """
        Register new poll request that was sent
        """
        self.storage[name] = Poll(name, sorted(buttons), datetime.utcnow())

    def poll_received(self, name: str, buttons: List[str]):
        """
        Registers receiving new poll
        """
        poll = self.storage.get(name)
        if not poll:
            logger.warning(f'Received poll {name} that was not sent! Ignoring.')
            return

        poll.poll_received = datetime.utcnow()
        logger.info(f'Received poll {name}')
        poll.received_valid = poll.buttons == sorted(buttons)
        if not poll.received_valid:
            logger.warning(f'Poll {name} was not valid! Some buttons were missing or were different!')
            logger.warning(f'Sent: {poll.buttons}, received: {sorted(buttons)}')

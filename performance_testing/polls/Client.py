import logging
import uuid
from dataclasses import dataclass

from client.RomanClient import RomanClient
from performance_testing.polls.Store import new_poll

logger = logging.getLogger(__name__)


@dataclass
class NewPollConfiguration:
    """
    Configuration for new poll sending
    """
    roman_url: str
    token: str
    buttons_count: int = 3


def send_new_poll(config: NewPollConfiguration):
    """
    Sends poll creation request to Roman and to poll bot
    """
    name = str(uuid.uuid4())
    buttons = [str(uuid.uuid4()) for _ in range(config.buttons_count)]
    # send poll request to Roman
    creation_query = f'/poll \"{name}\"' + ' '.join(f'\"{x}\"' for x in buttons)
    RomanClient(config.roman_url).send_text(token=config.token, text=creation_query)
    # store poll
    new_poll(name, buttons)

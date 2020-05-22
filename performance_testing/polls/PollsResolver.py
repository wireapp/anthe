import logging

from performance_testing.Resolver import Resolver, Command
from performance_testing.polls.Store import poll_received

logger = logging.getLogger(__name__)


def build_polls_resolver() -> Resolver:
    """
    Creates resolver for poll bot
    """
    return Resolver('PollsResolver', {
        is_new_poll: Command(False, resolve_new_poll),
        is_execute_new_command: Command(True, resolve_new_execute_command),
        is_join_execution_command: Command(True, resolve_join_execution_command)
    })


# -------- new poll received

def is_new_poll(data: dict) -> bool:
    return data.get('type') == 'conversation.poll.new' and data.get('poll') and data.get('text')


def resolve_new_poll(data: dict):
    """
    Handles receiving new poll - registers it in the store.
    """
    if not is_new_poll(data):
        logger.warning(f'Can not resolve new poll when no new poll is present. {data}')
        return
    message = data['text']
    buttons = data['poll'].get('buttons')
    poll_received(message, buttons)


# --------- create new performance execution

def is_execute_new_command(data: dict) -> bool:
    return data.get('type') == 'conversation.new_text' and \
           data.get('text') and \
           data.get('text').startswith('/execute polls new')


def resolve_new_execute_command(data: dict):
    """
    Starts completely new execution plan
    """
    pass


# -------- join current execution scheme

def is_join_execution_command(data: dict) -> bool:
    return data.get('type') == 'conversation.new_text' and \
           data.get('text') and \
           data.get('text').startswith('/execute polls join')


def resolve_join_execution_command(data: dict):
    """
    Joins current execution.
    """
    pass

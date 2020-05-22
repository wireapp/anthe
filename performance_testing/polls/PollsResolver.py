import logging

from performance_testing.Resolver import Resolver

logger = logging.getLogger(__name__)


def build_polls_resolver() -> Resolver:
    """
    Creates resolver for poll bot
    """
    return Resolver('PollsResolver', {
        is_new_poll: resolve_new_poll,
        is_execute_command: resolve_execute_command
    })


def is_new_poll(data: dict) -> bool:
    return data.get('type') == 'conversation.poll.new'


def resolve_new_poll(data: dict):
    pass


def is_execute_command(data: dict) -> bool:
    return data.get('type') == 'conversation.new_text' and \
           data.get('text') and \
           data.get('text').startswith('/execute polls')


def resolve_execute_command(data: dict):
    pass

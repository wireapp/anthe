import logging

from performance_testing.Resolver import Resolver

logger = logging.getLogger(__name__)


def build_echo_roman_resolver() -> Resolver:
    return Resolver("EchoRomanResolver", {
        is_new_you_said: resolve_you_said,
        is_execute_command: resolve_execute_command
    })


def is_execute_command(data: dict) -> bool:
    return data.get('type') == 'conversation.new_text' and \
           data.get('text') and \
           data.get('text').startswith('/execute echo-roman')


def resolve_execute_command(data: dict):
    pass


def is_new_you_said(data: dict) -> bool:
    return data.get('type') == 'conversation.new_text' and \
           data.get('text') and \
           data.get('text').startswith('You said: ')


def resolve_you_said(data: dict):
    pass

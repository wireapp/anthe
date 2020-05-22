import logging

from performance_testing.echo_roman.EchoRomanResolver import build_echo_roman_resolver
from performance_testing.polls.PollsResolver import build_polls_resolver

logger = logging.getLogger(__name__)

resolvers = [
    build_polls_resolver(),
    build_echo_roman_resolver()
]


def resolve_json(data: dict):
    """
    Executes all resolvers that can resolve given json.
    """
    for r in resolvers:
        if r.can_resolve(data):
            r.resolve(data)

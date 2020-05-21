from performance_testing.echo_roman.EchoRomanResolver import EchoRomanResolver
from performance_testing.polls.PollsResolver import PollsResolver

resolvers = [PollsResolver, EchoRomanResolver]


def resolve_json(data: dict):
    """
    Executes all resolvers that can resolve given json.
    """
    for r in resolvers:
        if r.can_resolve(data):
            r.resolve(data)

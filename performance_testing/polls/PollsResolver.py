import logging

from performance_testing.polls.ExecuteCommand import is_execute_command, resolve_execute_command
from performance_testing.polls.NewPoll import is_new_poll, resolve_new_poll

logger = logging.getLogger(__name__)


class PollsResolver:
    __resolvers = {is_new_poll: resolve_new_poll, is_execute_command: resolve_execute_command}

    @staticmethod
    def can_resolve(data: dict) -> bool:
        res = False
        for can in PollsResolver.__resolvers:
            res = res or can(data)
        logger.debug(f'PollsResolver: {res}')
        return res

    @staticmethod
    def resolve(data: dict):
        for (can, command) in PollsResolver.__resolvers.items():
            if can(data):
                logger.debug(f'Can resolve..')
                command(data)

import logging
from threading import Thread
from typing import Callable, Dict

from flask import current_app

from wire_flask.Config import Config, get_config

logger = logging.getLogger(__name__)


class Resolver:
    def __init__(self, name: str, resolvers: Dict[Callable[[dict], bool], 'Command']):
        self.name = name
        self.resolvers = resolvers

    def can_resolve(self, data: dict) -> bool:
        """
        Returns true if current instance of resolver
        can be used to resolve request.
        """
        res = any(can(data) for can in self.resolvers)
        logger.debug(f'{self.name}: {res}')
        return res

    def resolve(self, data: dict):
        """
        Passes given data to corresponding resolvers
        and executes them in the new thread with Flask context.
        """
        commands = [command for (can, command) in self.resolvers.items() if can(data)]
        for command in commands:
            logger.debug(f'{self.name} - resolving')
            command.execute(data)


class Command:
    """
    Class wrapping commands for resolvers.
    """

    def __init__(self, in_new_thread: bool, func: Callable[[dict, Config], None]):
        self.in_new_thread = in_new_thread
        self.func = func

    def execute(self, data: dict):
        """
        Executes new command.
        """
        config = get_config()
        if self.in_new_thread:
            # unpack the object to use context inside the different thread
            # noinspection PyProtectedMember
            Thread(
                target=execute_with_context,
                args=(current_app._get_current_object(), self.func, data, config,)
            ).start()
        else:
            self.func(data, config)


def execute_with_context(app, command: Callable[[dict, Config], None], data: dict, config: Config):
    with app.app_context():
        command(data, config)

import logging
from threading import Thread
from typing import Callable

from flask import current_app

logger = logging.getLogger(__name__)


class Resolver:
    def __init__(self, name: str, resolvers: dict):
        self.name = name
        self.resolvers = resolvers

    def can_resolve(self, data: dict) -> bool:
        """
        Returns true if current instance of resolver
        can be used to resolve request.
        """
        res = False
        for can in self.resolvers:
            res = res or can(data)
        logger.debug(f'{self.name}: {res}')
        return res

    def resolve(self, data: dict):
        """
        Passes given data to corresponding resolvers
        and executes them in the new thread with Flask context.
        """
        for (can, command) in self.resolvers.items():
            if can(data):
                logger.debug(f'{self.name} - resolving')
                # unpack the object to use context inside the different thread
                # noinspection PyProtectedMember
                Thread(
                    target=execute,
                    args=(current_app._get_current_object(), command, data,)
                ).start()


def execute(app, command: Callable, data: dict):
    with app.app_context():
        command(data)

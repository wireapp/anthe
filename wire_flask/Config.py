import logging
import os
from dataclasses import dataclass

from flask import current_app as app, g

logger = logging.getLogger(__name__)


@dataclass
class Config:
    """"
    Configuration class for the application.
    """
    roman_url: str
    roman_token: str


def get_config() -> Config:
    """
    Obtains configuration from the application context.
    """
    if 'config' not in g:
        g.version = build_configuration()
    return g.config


def build_configuration() -> Config:
    """
    Builds configuration from environment or from the Flask properties
    """
    logger.debug('Building configuration.')
    config = Config(roman_url=sanitize_url(get_prop('ROMAN_URL')),
                    roman_token=get_prop('ROMAN_TOKEN'))
    logger.debug(f'Used configuration: {config}')
    return config


def sanitize_url(url: str, protocol: str = 'https://') -> str:
    """
    Takes URL, removes last / and prepends protocol.

    >>> sanitize_url('charon.com/something/')
    'https://charon.com/something'
    """
    sanitized = url[0:-1] if url[-1] == '/' else url
    with_protocol = sanitized if sanitized.startswith('http') else f'{protocol}{sanitized}'
    return with_protocol


def get_prop(name: str, optional: bool = False) -> str:
    """
    Gets property from environment or from the flask env.
    """
    config = os.environ.get(name, app.config.get(name))
    if not optional and not config:
        logger.error(f'It was not possible to retrieve configuration for property "{name}"!')
        raise EnvironmentError(f'No existing configuration for "{name}" found!')
    return config

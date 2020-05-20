import logging

from client.RomanClient import RomanClient
from wire_flask.Config import get_config

logger = logging.getLogger(__name__)


class ResponseHandler:

    def __init__(self):
        self.client = RomanClient(get_config())

    def handle_json(self, json: dict):
        """
        Handle message received from the Roman
        """
        message_type = json.get('type')
        logger.debug(f'Handling message type: {message_type}')
        try:
            {
                'conversation.bot_request': lambda x: logger.info('Bot added to new conversation.'),
                'conversation.init': self.__init,
                'conversation.new_text': self.__new_message,
                'conversation.poll.new': self.__new_poll,
                None: lambda x: logger.error(f'No type received for json: {x}')
            }[message_type](json)
        except KeyError:
            # type is different
            logger.warning(f'Unhandled type: {message_type}')
        except Exception as ex:
            logger.exception(ex)

    def __init(self, json: dict):
        logger.debug('init received')
        self.__send_text("Hello! I'm Echo Bot!", [], json['token'])

    def __new_message(self, json: dict):
        logger.debug('New text message received.')
        self.__send_text('Understood', [], json['token'])

    def __new_poll(self, json: dict):
        pass

    def __send_text(self, message: str, mentions: list, token: str):
        text = {'data': message, 'mentions': mentions}
        msg = {'type': 'text', 'text': text}
        self.client.send_message(token, msg)

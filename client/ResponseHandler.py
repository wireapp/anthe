import logging

from client.RomanClient import RomanClient
from performance_testing.DataResolver import resolve_json
from persistence.Conversations import Conversation
from persistence.Db import db
from wire_flask.Config import get_config

logger = logging.getLogger(__name__)


class ResponseHandler:

    def __init__(self):
        self.client = RomanClient(get_config().roman_url)

    def handle_json(self, json: dict):
        """
        Handle message received from the Roman
        """
        message_type = json.get('type')
        logger.debug(f'Handling message type: {message_type}')

        try:
            {
                'conversation.bot_request': self.__bot_request,
                'conversation.init': self.__init,
                'conversation.bot_removed': self.__bot_removed,
                None: lambda x: logger.error(f'No type received for json: {x}')
            }.get(message_type, resolve_json)(json)
        except Exception as ex:
            logger.error(f'Exception during json handling: {json}')
            logger.exception(ex)

    def __init(self, json: dict):
        logger.debug('Init received')
        self.client.send_text(token=json['token'], text="Hello! I'm Performance testing bot!")

    @staticmethod
    def __bot_request(json: dict):
        conversation_id = json.get('conversationId')
        bot_id = json.get('botId')
        token = json.get('token')

        if not conversation_id or not token or not bot_id:
            logger.warning(f'Invalid init data received - id or token missing. {json}')
            return

        conversation = Conversation(conversation_id=conversation_id, token=token, bot_id=bot_id)
        logger.debug(f'New conversation initiated.')
        db.session.add(conversation)
        db.session.commit()

    @staticmethod
    def __bot_removed(json: dict):
        logger.debug(f'Bot removed from the conversation.')
        bot_id = json.get('botId')
        if not bot_id:
            logger.warning(f'Invalid json for bot removed - no id set - {json}')
            return
        logger.info(f'Removing bot {bot_id} from the database.')
        Conversation.query.filter(Conversation.bot_id == bot_id).delete()
        db.session.commit()

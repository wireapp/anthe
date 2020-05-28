import logging
from typing import Optional

from performance_testing.Resolver import Resolver, Command
from performance_testing.polls.Client import NewPollConfiguration
from performance_testing.polls.Store import poll_received
from performance_testing.polls.TestExecutor import execute_test
from persistence.Conversations import Conversation
from persistence.Db import db
from persistence.Scenario import Scenario
from wire_flask.Config import Config

logger = logging.getLogger(__name__)


def build_polls_resolver() -> Resolver:
    """
    Creates resolver for poll bot
    """
    return Resolver('PollsResolver', {
        is_new_poll: Command(False, resolve_new_poll),
        is_execute_new_command: Command(True, resolve_new_execute_command),
        is_new_scenario: Command(False, resolve_new_scenario),
        is_join_scenario: Command(False, resolve_join_scenario)
    })


# -------- new poll received

def is_new_poll(data: dict) -> bool:
    return data.get('type') == 'conversation.poll.new' and data.get('poll') and data.get('text')


def resolve_new_poll(data: dict, _: Config):
    """
    Handles receiving new poll - registers it in the store.
    """
    if not is_new_poll(data):
        logger.warning(f'Can not resolve new poll when no new poll is present. {data}')
        return
    message = data['text']
    buttons = data['poll']['buttons']
    poll_received(message, buttons)


# --------- create new scenario

def is_new_scenario(data: dict) -> bool:
    return data.get('type') == 'conversation.new_text' and \
           data.get('text') and \
           data.get('text').startswith('/execute polls scenario new')


def resolve_new_scenario(data: dict, _: Config):
    """
    Handles receiving new poll - registers it in the store.
    """
    try:
        name = data['text'].replace('/execute polls scenario new', '').strip()
        sc = Scenario(
            scenario_name=name,
            bot_under_test='polls',
            conversations=[Conversation.query.filter(Conversation.conversation_id == data['conversationId']).all()]
        )
        db.add(sc)
        db.commit()
    except Exception as ex:
        logger.error(f'Exception during handling new scenario creation.')
        logger.exception(ex)


# --------- join scenario

def is_join_scenario(data: dict) -> bool:
    return data.get('type') == 'conversation.new_text' and \
           data.get('text') and \
           data.get('text').startswith('/execute polls scenario join')


def resolve_join_scenario(data: dict, _: Config):
    """
    Handles receiving new poll - registers it in the store.
    """
    try:
        name = data['text'].replace('/execute polls scenario join', '').strip()
        sc = Scenario.query.filter(Scenario.scenario_name == name)
        sc.conversations.extend(
            Conversation.query.filter(Conversation.conversation_id == data['conversationId']).all()
        )
        db.commit()
    except Exception as ex:
        logger.error(f'Exception during handling joining scenario. {data}')
        logger.exception(ex)


# --------- create new performance execution

def is_execute_new_command(data: dict) -> bool:
    return data.get('type') == 'conversation.new_text' and \
           data.get('text') and \
           data.get('text').startswith('/execute polls new')


def resolve_new_execute_command(data: dict, config: Config):
    """
    Starts completely new execution plan
    """
    try:
        count = int(data['text'].replace('/execute polls new', ''))
        poll_config = get_poll_config(data, config)
        if not poll_config:
            logger.error('Could not build poll configuration, exiting.')
            return
    except Exception as ex:
        logger.error(f'It was not possible to parse count. {data}')
        logger.exception(ex)
        return

    execute_test(poll_config, count)


def get_poll_config(data: dict, config: Config) -> Optional[NewPollConfiguration]:
    conversation_id = data.get('conversationId')
    if not conversation_id:
        logger.error(f'No Conversation Id specified in json. Could not execute {data}')
        return None
    conversation = Conversation.query.filter(Conversation.conversation_id == conversation_id).first()
    if not conversation:
        logger.error(f'Could not find conversation with id {conversation_id}')
        return None

    poll_config = NewPollConfiguration(roman_url=config.roman_url, token=conversation.token)
    return poll_config

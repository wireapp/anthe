import logging
import math
import time
from concurrent import futures
from concurrent.futures import ThreadPoolExecutor
from typing import Optional

from client.RomanClient import RomanClient
from performance_testing.Resolver import Resolver, Command
from performance_testing.polls.Client import NewPollConfiguration, send_new_poll
from performance_testing.polls.Store import poll_received, init_store, release_store
from persistence.Conversations import Conversation
from wire_flask.Config import Config

logger = logging.getLogger(__name__)


def build_polls_resolver() -> Resolver:
    """
    Creates resolver for poll bot
    """
    return Resolver('PollsResolver', {
        is_new_poll: Command(False, resolve_new_poll),
        is_execute_new_command: Command(True, resolve_new_execute_command)
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
        logger.error(f'It was not possible to parse count.')
        logger.exception(ex)
        return

    execute_test(poll_config, count)


def execute_test(poll_config: NewPollConfiguration, count: int):
    logger.info('Starting execution New Execute')
    logger.debug(f'With config {poll_config}')
    init_store()
    # startup the pool
    workers = round(max(math.log(count), 1))
    logger.debug(f'Creating poll with {workers}')
    executor = ThreadPoolExecutor(workers)
    fs = []
    # TODO maybe add some sleep between each send?
    for i in range(count):
        logger.debug(f'Executing {i} request from {count}')
        fs.append(executor.submit(send_new_poll, poll_config))

    logger.debug('Waiting on tasks to finish')
    # wait for all remaining polls to be delivered
    futures.wait(fs, timeout=count * 1.5)

    logger.debug('Waiting on polls to be received')
    # wait for all remaining polls to be delivered
    sleep_trash_hold = min(int(count * 1), 60)

    logger.info(f'New Execute Execution stopped - waiting max threshold {sleep_trash_hold}.')
    time.sleep(sleep_trash_hold)

    logger.info('Finalizing test.')
    release_store()
    # maybe send some more meaningful results
    RomanClient(poll_config.roman_url).send_text(token=poll_config.token, text='Execution finished.')

    # delete pool
    executor.shutdown()


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

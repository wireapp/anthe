import logging
import math
import time
from concurrent import futures
from concurrent.futures.thread import ThreadPoolExecutor

from client.RomanClient import RomanClient
from performance_testing.polls.Client import NewPollConfiguration, send_new_poll
from performance_testing.polls.Store import init_store, release_store

logger = logging.getLogger(__name__)


def execute_test(poll_config: NewPollConfiguration, count: int):
    logger.info('Starting execution New Execute')
    logger.debug(f'With config {poll_config}')
    init_store()
    # startup the pool
    workers = round(max(math.log(count), 1))
    logger.debug(f'Creating poll with {workers}')
    executor = ThreadPoolExecutor(workers)

    # TODO maybe add some sleep between each send?
    fs = [executor.submit(send_new_poll, poll_config) for _ in range(count)]

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

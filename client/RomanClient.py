import json
import logging

import requests

from wire_flask.Config import Config

logger = logging.getLogger(__name__)


class RomanClient:
    def __init__(self, config: Config):
        self.url = config.roman_url

    def send_message(self, token: str, payload: dict) -> str:
        logger.debug('Sending payload to Roman')
        data = json.dumps(payload)
        logger.debug(f'{data}')
        r = requests.post(f"{self.url}/conversation", data=data,
                          headers={"content-type": "application/json", "Authorization": f"Bearer {token}"})
        logger.debug('Data sent.')
        return r.json()['messageId']

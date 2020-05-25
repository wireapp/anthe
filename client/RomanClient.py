import json
import logging

import requests

logger = logging.getLogger(__name__)


class RomanClient:
    def __init__(self, roman_url: str):
        self.url = roman_url

    def send_message(self, token: str, payload: dict) -> str:
        """
        Sends data to Roman
        """
        logger.debug('Sending payload to Roman')
        data = json.dumps(payload)
        logger.debug(f'{data}')
        r = requests.post(f"{self.url}/conversation", data=data,
                          headers={"content-type": "application/json", "Authorization": f"Bearer {token}"})
        response = r.json()
        logger.debug(f'Data sent - {r.status_code} - {response}')
        return response.get('messageId')

    def send_text(self, token: str, text: str):
        """
        Creates and formats text message.
        """
        text = {'data': text, 'mentions': []}
        msg = {'type': 'text', 'text': text}
        logger.debug('Sending message')
        self.send_message(token, msg)

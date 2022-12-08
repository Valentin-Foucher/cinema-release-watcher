from typing import Union

import requests

import config
from alerts.interface import Client


class TelegramClient(Client):
    def __init__(self, config_: dict[str, Union[str, int]]):
        self._config = config_

    def send(self, text: str):
        requests.post(f'https://api.telegram.org/bot{self._config["token"]}'
                      f'/sendMessage?chat_id={self._config["channel"]}&text={text}', {})


if __name__ == '__main__':
    TelegramClient(config.get('alerts.telegram')) \
        .send('hello its me')

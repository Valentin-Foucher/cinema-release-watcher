from typing import Union

import requests

from cinema_release_watcher import config
from cinema_release_watcher.api_clients.alerts.interface import Client


class TelegramClient(Client):
    def send(self, text: str):
        self.post(f'/bot{self._config["token"]}/sendMessage', {},
                  query_parameters=dict(chat_id=self._config['channel'], text=text))


if __name__ == '__main__':
    TelegramClient(config.get('alerts.telegram')) \
        .send('hello its me')

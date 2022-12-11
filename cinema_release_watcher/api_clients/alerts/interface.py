from abc import ABC, abstractmethod

from cinema_release_watcher.api_clients.base import BaseJsonRestClient


class Client(BaseJsonRestClient, ABC):
    @abstractmethod
    def send(self, data: str) -> None:
        raise NotImplementedError

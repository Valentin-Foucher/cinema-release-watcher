from abc import ABC, abstractmethod

from cinema_release_watcher.api_clients.base import BaseJsonRestClient


class Client(BaseJsonRestClient, ABC):
    @abstractmethod
    def send(self, text: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def send_document(self, path: str) -> None:
        raise NotImplementedError

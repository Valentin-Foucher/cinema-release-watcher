from abc import ABC, abstractmethod


class Client(ABC):
    @abstractmethod
    def send(self, data: str) -> None:
        raise NotImplementedError

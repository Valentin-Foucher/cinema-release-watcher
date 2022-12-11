from abc import ABC, abstractmethod
from datetime import date

from cinema_release_watcher.api_clients.base import BaseJsonRestClient
from cinema_release_watcher.domain.movies import Movie, Genre


class Client(BaseJsonRestClient, ABC):
    @abstractmethod
    def retrieve_movies(self, min_date: date, max_date: date, genres: list[Genre]) -> list[Movie]:
        raise NotImplementedError

    @abstractmethod
    def retrieve_genres(self) -> list[Genre]:
        raise NotImplementedError

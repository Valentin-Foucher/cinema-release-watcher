from abc import ABC, abstractmethod
from datetime import date
from typing import Optional, Tuple

from cinema_release_watcher.api_clients.base import BaseJsonRestClient
from cinema_release_watcher.domain.movies import Movie, Genre


class Client(BaseJsonRestClient, ABC):
    @abstractmethod
    def retrieve_movies(self, min_date: date, max_date: date) -> list[Movie]:
        raise NotImplementedError

    @abstractmethod
    def retrieve_genres(self) -> list[Genre]:
        raise NotImplementedError

    @abstractmethod
    def get_movie_director(self, movie_id: int) -> Optional[str]:
        raise NotImplementedError

    @abstractmethod
    def get_image(self, movie_id: int) -> Tuple[Optional[bytes], Optional[str]]:
        raise NotImplementedError

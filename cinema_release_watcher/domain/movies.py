from copy import deepcopy
from dataclasses import dataclass

from dataclasses_json import dataclass_json, Undefined


@dataclass_json
@dataclass
class Genre:
    id: int
    name: str


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Movie:
    id: int
    genre_ids: list[int]
    genres: list[str]
    original_title: str
    vote_average: float
    release_date: str

    def with_genres(self, genres_list: list[Genre]) -> 'Movie':
        exposed_movie = deepcopy(self)
        exposed_movie.genre_ids = None

        genres_id = self.genre_ids
        exposed_movie.genres = [genre.name for genre in genres_list if genre.id in genres_id]
        return exposed_movie

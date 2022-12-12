from dataclasses import dataclass
from typing import Optional

from dataclasses_json import dataclass_json, Undefined


@dataclass_json
@dataclass
class Genre:
    id: int
    name: str


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass(repr=False)
class Movie:
    id: int
    genre_ids: Optional[list[int]]
    title: str
    original_title: str
    overview: str
    vote_average: float
    release_date: str
    genres: Optional[list[str]] = None

    def with_genres(self, genres_list: list[Genre]) -> 'Movie':
        self.genres = [genre.name for genre in genres_list if genre.id in self.genre_ids]
        del self.genre_ids
        return self

    def __str__(self):
        return f'{self.title} ({self.original_title}) - {", ".join(self.genres)} - {self.vote_average}/10'

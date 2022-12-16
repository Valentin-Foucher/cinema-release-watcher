import re
import sys
from datetime import date
from typing import Optional, Tuple

from requests import JSONDecodeError

from cinema_release_watcher.api_clients.movies.interface import Client
from cinema_release_watcher.constants import DIRECTOR
from cinema_release_watcher.domain.movies import Genre, Movie


class TMdBClient(Client):
    def retrieve_genres(self) -> list[Genre]:
        response = self._get('3/genre/movie/list',
                             query_parameters=dict(api_key=self._config['api_key'],
                                                   language=self._config['language']),
                             status_code=[304, 200])

        try:
            json_response = response.json()
        except JSONDecodeError:
            raise RuntimeError(f'Could not decode response: {response.text}')

        return [Genre.from_dict(genre) for genre in json_response['genres']]

    def retrieve_movies(self, min_date: date, max_date: date) -> list[Movie]:
        page_number = 1
        total_pages = sys.maxsize
        parsed_movies = []

        while page_number <= total_pages:
            response = self._get('3/discover/movie',
                                 query_parameters={
                                     'api_key': self._config['api_key'],
                                     'region': self._config['region'],
                                     'sort_by': 'vote_average.desc',
                                     'include_adult': False,
                                     'with_release_type': '3|2',  # released in theatres
                                     'release_date.gte': min_date.isoformat(),
                                     'release_date.lte': max_date.isoformat(),
                                     'page': page_number
                                 },
                                 status_code=[304, 200])

            try:
                json_response = response.json()
            except JSONDecodeError:
                raise RuntimeError(f'Could not decode response: {response.text}')

            for retrieved_movie in json_response.get('results'):
                parsed_movies.append(Movie.from_dict(retrieved_movie))

            page_number += 1
            total_pages = int(json_response['total_pages'])

        return parsed_movies

    def get_movie_director(self, movie_id: int) -> Optional[str]:
        response = self._get(f'3/movie/{movie_id}/credits',
                             query_parameters={'api_key': self._config['api_key']},
                             status_code=[304, 200])

        try:
            json_response = response.json()
        except JSONDecodeError:
            raise RuntimeError(f'Could not decode response: {response.text}')

        try:
            return next(person.get('name') for person in json_response.get('crew') if person.get('job') == DIRECTOR)
        except StopIteration:
            return

    def get_image(self, movie_id: int) -> Tuple[Optional[bytes], Optional[str]]:
        response = self._get(f'3/movie/{movie_id}',
                             query_parameters={'api_key': self._config['api_key']},
                             status_code=[304, 200])

        try:
            json_response = response.json()
        except JSONDecodeError:
            raise RuntimeError(f'Could not decode response: {response.text}')

        poster_path = json_response.get('poster_path')
        if not poster_path:
            return None, None

        response = self._get(f't/p/original{poster_path}',
                             client_type='images',
                             query_parameters={'api_key': self._config['api_key']},
                             status_code=200)

        return response.content, re.sub(r'^[^.]+', '', poster_path)[1:]



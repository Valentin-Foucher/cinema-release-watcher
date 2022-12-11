import sys
from datetime import date

from requests import JSONDecodeError

from cinema_release_watcher.api_clients.movies.interface import Client
from cinema_release_watcher.domain.movies import Genre, Movie


class TMdBClient(Client):
    def retrieve_movies(self, min_date: date, max_date: date, genres: list[Genre]) -> list[Movie]:
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
                                     'with_release_type': '3|2',
                                     'release_date.gte': min_date.isoformat(),
                                     'release_date.lte': max_date.isoformat(),
                                     'page': page_number
                                 })  # released in theatres

            try:
                json_response = response.json()
            except JSONDecodeError:
                raise RuntimeError(f'Could not decode response: {response.text}')

            for retrieved_movie in json_response.get('results'):
                parsed_movies.append(Movie.from_dict(retrieved_movie).with_genres(genres))

            page_number += 1
            total_pages = int(json_response['total_pages'])

        return parsed_movies

    def retrieve_genres(self) -> list[Genre]:
        response = self._get('3/genre/movie/list',
                             query_parameters=dict(api_key=self._config['api_key'],
                                                   language=self._config['language']))

        try:
            json_response = response.json()
        except JSONDecodeError:
            raise RuntimeError(f'Could not decode response: {response.text}')

        return [Genre.from_dict(genre) for genre in json_response['genres']]

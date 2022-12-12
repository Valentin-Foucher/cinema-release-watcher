import os
import uuid

import pdfkit
from jinja2 import Environment, FileSystemLoader

from cinema_release_watcher.domain.movies import Movie


class PdfResource:
    def __init__(self, starred_movies: list[Movie], relevant_movies: list[Movie]):
        self._starred_movies = starred_movies
        self._relevant_movies = relevant_movies

    def __enter__(self):
        self.file_name = self._generate()
        return self.file_name

    def __exit__(self, exc_type, exc_value, tb):
        os.remove(self.file_name)

    def _generate(self) -> str:
        template = Environment(loader=FileSystemLoader("templates/")).get_template('alert.html')
        html = template.render(starred_movies=self._starred_movies,
                               relevant_movies=self._relevant_movies)
        pdfkit.from_string(html, file_name := f'{str(uuid.uuid4())}.pdf')
        return file_name



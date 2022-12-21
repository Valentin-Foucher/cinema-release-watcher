import argparse
from datetime import timedelta, timezone, datetime

from cinema_release_watcher import config
from cinema_release_watcher.api_clients.alerts.telegram import TelegramClient
from cinema_release_watcher.api_clients.movies.tmdb import TMdBClient
from cinema_release_watcher.constants import PresentationStrategies
from cinema_release_watcher.domain.movies import Movie
from cinema_release_watcher.messages import text, pdf
from cinema_release_watcher.utils.image_utils import build_src_for_html


def prepare_movie_for_rendering(movie: Movie, tmdb_client):
    movie.director = tmdb_client.get_movie_director(movie.id)
    image, extension = tmdb_client.get_image(movie.id)
    movie.image = build_src_for_html(image, extension)


def main(strategy: str):
    this_week = datetime.now(timezone.utc).date()
    last_week = this_week - timedelta(days=6)

    tmdb_client = TMdBClient(config.get('TMdB'))
    genres = tmdb_client.retrieve_genres()
    movies = tmdb_client.retrieve_movies(last_week, this_week)

    preferred_genres = config.get('TMdB.preferences.genres')
    excluded_genres = config.get('TMdB.preferences.excluded_genres')
    relevant_movies = []
    starred_movies = []

    for movie in movies:
        movie = movie.with_genres(genres)

        if any(genre in excluded_genres for genre in movie.genres):
            continue
        if movie.vote_average >= config.get('TMdB.preferences.premium_note'):
            prepare_movie_for_rendering(movie, tmdb_client)
            starred_movies.append(movie)
        elif any(genre in preferred_genres for genre in movie.genres) \
                and movie.vote_average >= config.get('TMdB.preferences.minimal_note'):
            prepare_movie_for_rendering(movie, tmdb_client)
            relevant_movies.append(movie)

    telegram_client = TelegramClient(config.get('telegram'))

    if strategy == PresentationStrategies.TEXT:
        telegram_client.send(text.get_message(starred_movies, relevant_movies))
    elif strategy == PresentationStrategies.PDF:
        with pdf.PdfResource(starred_movies, relevant_movies) as file_name:
            telegram_client.send_document(file_name)
    else:
        raise RuntimeError(f'Invalid strategy: {strategy}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Script allowing to alert of recent releases in theatres through'
                                                 'a Telegram bot')
    parser.add_argument(
        '-s', '--strategy',
        required=True,
        type=PresentationStrategies,
        choices=list(PresentationStrategies),
        help='Strategy to employ to expose info. Value should be among "pdf" and "text"'
    )
    main(parser.parse_args().strategy)

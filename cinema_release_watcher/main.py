import argparse
from datetime import timedelta, timezone, datetime

from cinema_release_watcher import config
from cinema_release_watcher.api_clients.alerts.telegram import TelegramClient
from cinema_release_watcher.api_clients.movies.tmdb import TMdBClient
from cinema_release_watcher.constants import PresentationStrategies
from cinema_release_watcher.messages import text, pdf


def main(strategy: str):
    this_week = datetime.now(timezone.utc).date()
    last_week = this_week - timedelta(days=7)

    tmdb_client = TMdBClient(config.get('TMdB'))
    genres = tmdb_client.retrieve_genres()
    movies = tmdb_client.retrieve_movies(last_week, this_week, genres)

    preferred_genres = config.get('TMdB.preferences.genres')
    relevant_movies = []
    starred_movies = []

    for movie in movies:
        if movie.vote_average >= config.get('TMdB.preferences.premium_note'):
            starred_movies.append(movie)
        elif any(genre in preferred_genres for genre in movie.genres) \
                and movie.vote_average >= config.get('TMdB.preferences.minimal_note'):
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

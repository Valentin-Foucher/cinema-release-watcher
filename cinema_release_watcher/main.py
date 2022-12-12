import argparse
from datetime import date, timedelta

from cinema_release_watcher import config
from cinema_release_watcher.api_clients.alerts.telegram import TelegramClient
from cinema_release_watcher.api_clients.movies.tmdb import TMdBClient
from cinema_release_watcher.constants import PresentationStrategies


def main(strategy: str):
    this_week = date.today()
    last_week = this_week - timedelta(days=7)

    tmdb_client = TMdBClient(config.get('TMdB'))
    genres = tmdb_client.retrieve_genres()
    movies = tmdb_client.retrieve_movies(last_week, this_week, genres)

    preferred_genres = config.get('TMdB.preferences.genres')
    relevant_movies = []
    starred_movies = []

    for movie in movies:
        if movie.vote_average >= config.get('TMdB.preferences.premium_note'):
            starred_movies.append(str(movie))
        elif any(genre in preferred_genres for genre in movie.genres) \
                and movie.vote_average >= config.get('TMdB.preferences.minimal_note'):
            relevant_movies.append(str(movie))

    telegram_client = TelegramClient(config.get('telegram'))

    if strategy == PresentationStrategies.TEXT:
        message = 'Hello! 👋\n\n'
        line_separator = '\n• '
        if starred_movies and relevant_movies:
            message += 'Here are movies that many people like:' \
                       f'{line_separator}{line_separator.join(starred_movies)}\n\n' \
                       'And these are movies that you might like according to your preferences:' \
                       f'{line_separator}{line_separator.join(relevant_movies)}'
        elif starred_movies:
            message += 'Here are movies that many people like:' \
                       f'{line_separator}{line_separator.join(starred_movies)}'
        elif relevant_movies:
            message += 'Here are movies that you might like according to your preferences:' \
                       f'{line_separator}{line_separator.join(relevant_movies)}'
        else:
            message += 'Unfortunately, there does not seem to be any movie that you would like that were recently ' \
                       'released 😔'

        telegram_client.send(message)
    elif strategy == PresentationStrategies.PDF:
        # TODO
        telegram_client.send_document('')
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

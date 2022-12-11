from datetime import date, timedelta

from cinema_release_watcher import config
from cinema_release_watcher.api_clients.alerts.telegram import TelegramClient
from cinema_release_watcher.api_clients.movies.tmdb import TMdBClient


def main():
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
            starred_movies.append(movie)
        elif any(genre in preferred_genres for genre in movie.genres) \
                and movie.vote_average >= config.get('TMdB.preferences.minimal_note'):
            relevant_movies.append(movie)

    print(len(starred_movies))
    print(len(relevant_movies))

    telegram_client = TelegramClient(config.get('telegram'))
    telegram_client.send(f'starred_movies={starred_movies}, relevant_movies={relevant_movies}')


if __name__ == '__main__':
    main()

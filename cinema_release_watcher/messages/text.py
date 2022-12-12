from cinema_release_watcher.constants import LINE_SEPARATOR
from cinema_release_watcher.domain.movies import Movie


def get_message(starred_movies: list[Movie], relevant_movies: list[Movie]) -> str:
    message = "Hello! 👋\n\n"
    if starred_movies and relevant_movies:
        message += "Here are movies that many people like:" \
                   f"{LINE_SEPARATOR}{LINE_SEPARATOR.join(str(movie) for movie in starred_movies)}\n\n" \
                   "And these are movies that you might like according to your preferences:" \
                   f"{LINE_SEPARATOR}{LINE_SEPARATOR.join(str(movie) for movie in relevant_movies)}"
    elif starred_movies:
        message += "Here are movies that many people like:" \
                   f"{LINE_SEPARATOR}{LINE_SEPARATOR.join(str(movie) for movie in starred_movies)}"
    elif relevant_movies:
        message += "Here are movies that you might like according to your preferences:" \
                   f"{LINE_SEPARATOR}{LINE_SEPARATOR.join(str(movie) for movie in relevant_movies)}"
    else:
        message += "Unfortunately, there does not seem to be any movie that you would like that were recently " \
                   "released 😔"

    return message

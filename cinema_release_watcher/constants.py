from enum import Enum


class PresentationStrategies(Enum):
    TEXT = 'text'
    PDF = 'pdf'

    def __str__(self):
        return self.value

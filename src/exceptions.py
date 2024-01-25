class UserNotFound(Exception):
    """User was not found"""


class GameNotFound(Exception):
    """Game was not found"""


class DuplicateWord(Exception):
    """Wordle word already exists"""


class InvalidWordleWord(Exception):
    """The attempted answer is an invalid wordle word"""
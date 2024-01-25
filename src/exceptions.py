class UserNotFound(Exception):
    """User was not found"""


class GameNotFound(Exception):
    """Game was not found"""


class DuplicateWord(Exception):
    """Wordle word already exists"""


class InvalidAttempt(Exception):
    """The attempted answer is an invalid wordle word"""


class ExceededAttempts(Exception):
    """User has exceeded attempts for game"""
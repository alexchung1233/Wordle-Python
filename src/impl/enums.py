import enum

class LetterAnswer(enum.Enum):
    CORRECT = 0 
    WRONG_SPOT = 1
    INCORRECT = 2

class Difficulty(enum.Enum):
    EASY = 0
    HARD = 1

LETTER_ANSWER_NAMES = [la.name for la in LetterAnswer]
DIFFICULTY_NAMES = [d.name for d in Difficulty]
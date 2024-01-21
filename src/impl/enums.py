import enum

class LetterAnswer(enum.Enum):
    CORRECT = 0 
    WRONG_SPOT = 1
    INCORRECT = 2

LETTER_ANSWER_NAMES = (la.name for la in LetterAnswer)
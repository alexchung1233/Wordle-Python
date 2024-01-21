"""World game class"""
import uuid

class Wordle:
    """Worlde game class used to intialize a game"""
    def __init__(self, user_name) -> None:
        self.game_id: str = uuid.uuid4()
        self.user_name: str = user_name
        self.max_attempts: int
        self.answer: str = ''
        self.current_attempts: int = 0
    

    @classmethod
    def create_game(cls, user_name: str, answer_letters: int):
        new_game = cls(user_name)
        new_game.max_attempts = answer_letters+1
        
        




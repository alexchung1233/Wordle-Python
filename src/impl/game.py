"""World game class"""
import uuid
import impl.user as user

class GameImpl:
    """Wordle game class used to intialize a game"""
    def __init__(self, user_name) -> None:
        self.game_id: str = uuid.uuid4()
        self.user_name: user.UserImpl = None
        self.max_attempts: int
        self.answer: str = ''
        self.current_attempts: int = 0
    

    @classmethod
    def create_game(cls, user_name: str, answer_letters: int):
        new_game = cls(user_name)
        new_game.max_attempts = answer_letters+1
        return new_game

        # Add new game to Dynamo

    @classmethod
    def get_game(cls, game_id: str):
        pass
    
    def to_dict(self):
        pass
    
    def add_attempt(self, attempt_word: str):
        if self.current_attempts < self.max_attempts:
            self.current_attempts += 1




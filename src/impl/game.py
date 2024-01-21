"""World game class"""
import uuid
import impl.user as user

class GameImpl:
    """Wordle game class used to intialize a game"""
    def __init__(self, user_name) -> None:
        self.game_id: str = uuid.uuid4()
        self.user: user.UserImpl = None
        self.max_attempts: int
        self.answer: str = ''
        self.current_attempts: int = 0
    

    @classmethod
    def create_game(cls, user_name: str, answer_length: int, user_id: str = ''):
        """Must provide either user id or user name."""
        new_game = cls(user_name)
        if not user_id:
            new_game.user = user.UserImpl(user_name)
        else:
            new_game.user = user.UserImpl.get_user_info(user_id)
        new_game.max_attempts = answer_length+1
        return new_game

        # Add new game to Dynamo

    @classmethod
    def get_game(cls, game_id: str):
        pass
    
    def to_dict(self):
        return {'game_id': self.game_id,
                'user_name': self.user.user_name,
                'max_attempts': self.max_attempts,
                'answer': self.answer,
                'current_attempts': self.current_attempts}
    
    def add_attempt(self, attempt_word: str):
        if self.current_attempts < self.max_attempts:
            self.current_attempts += 1
        
        # Update game in dynamodb
    
    @classmethod
    def games_by_user_id(user_id: str):
        # Fetch list of games in dynamodb by user id

        pass


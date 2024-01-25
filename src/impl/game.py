"""World game class"""
import uuid
import impl.user as user
import impl.db_impl as db_impl
import exceptions
import random
import boto3
import boto3.dynamodb.conditions as conditions


DBImpl = db_impl.DBImpl

class GameImpl:
    """Wordle game class used to intialize a game"""
    def __init__(self) -> None:
        self.game_id: str = str(uuid.uuid4())
        self.user: user.UserImpl = None
        self.max_attempts: int
        self.answer: str = ''
        self.current_attempts: int = 0
        self.attempts: list = []
    

    @classmethod
    def create_game(cls, user_name: str, answer_length: int, user_id: str = ''):
        """Must provide either user id or user name."""
        new_game = cls()
        if not user_id:
            new_game.user = user.UserImpl.create_user(user_name)
        else:
            new_game.user = user.UserImpl.get_user_info(user_id)
        new_game.max_attempts = answer_length+1
        new_game.answer = cls._get_rand_answer(answer_length)

        # Write the game to the DynamoDB
        new_game._write_new_game()
        return new_game

        # Add new game to Dynamo

    @classmethod
    def get_game(cls, game_id: str):
        """Get game by game id"""
        table = DBImpl.get_data_table()

        response = table.scan(FilterExpression=conditions.Attr('GameID').eq(game_id))
        if response['Items']:
            data = response['Items'][0]
            game = cls._convert_db_to_object(data)
            return game

        raise exceptions.GameNotFound
    
    def to_dict(self):
        return {'game_id': self.game_id,
                'user_name': self.user.user_name,
                'user_id': self.user.user_id,
                'max_attempts': self.max_attempts,
                'answer': self.answer,
                'current_attempts': self.current_attempts,
                'attempts': self.attempts}
    
    def add_attempt(self, attempt_word: str):
        if self.current_attempts < self.max_attempts:
            self.current_attempts += 1
        else:
            raise exceptions.ExceededAttempts
        self._update_attempt_db()
    
        # Update game in dynamodb
    
    @classmethod
    def games_by_user_id(cls, user_id: str):
        """Fetch list of games by user id"""

        table = DBImpl.get_data_table()

        response = table.scan(FilterExpression=conditions.Attr('UserID').eq(user_id))
        records = response['Items']
        games = []
        for record in records:
            if record.get('GameID') == 'UserInfo':
                break
            game = cls._convert_db_to_object(record)
            games.append(game)

        return games
    
    def _update_attempt_db(self):
        table = DBImpl.get_data_table()
        expression = "set CurrentAttempts = :n"
        attr_values = {":n": self.current_attempts}

        table.update_item( Key={'UserID': self.user.user_id,
                                'GameID': self.game_id},
                            UpdateExpression=expression,
                            ExpressionAttributeValues=attr_values)
        
    @classmethod
    def _get_rand_answer(cls, answer_length: int):
        """Get a random answer"""
        table = DBImpl.get_dict_table()
        response = table.scan(
            FilterExpression=conditions.Attr('WordLength').eq(answer_length),
            ProjectionExpression='Word'
        )
        words = response['Items']
        rand_indx = random.randint(0,len(words)+1)
        answer = words[rand_indx]['Word']
        return answer


    def _write_new_game(self):
        table = DBImpl.get_data_table()
        table.put_item(Item={'UserID': self.user.user_id,
                             'GameID': self.game_id, 
                             'UserName': self.user.user_name,
                             'MaxAttempts': self.max_attempts,
                             'Answer': self.answer,
                             'CurrentAttempts': self.current_attempts,
                             'Attempts': self.attempts})


    @classmethod
    def _convert_db_to_object(cls, data: dict):
            rtr_game = cls()
            rtr_game.game_id = data.get('GameID')
            rtr_game.user = user.UserImpl(user_name=data.get('UserName'), user_id=data.get('UserID'))
            rtr_game.max_attempts = data.get('MaxAttempts')
            rtr_game.answer = data.get('Answer')
            rtr_game.current_attempts = data.get('CurrentAttempts')
            rtr_game.attempts = data.get('Attempts')

            return rtr_game


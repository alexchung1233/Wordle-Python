"""World game class"""
import uuid
import impl.user as user
import impl.dictionary as dictionary
import impl.db_impl as db_impl
import impl.enums as enums
import exceptions
import random
import boto3
import boto3.dynamodb.conditions as conditions
import logging


logger = logging.getLogger()
DictionaryImpl = dictionary.DictionaryImpl
DBImpl = db_impl.DBImpl

class GameImpl:
    """Wordle game class used to intialize a game"""
    def __init__(self) -> None:
        self.game_id: str = str(uuid.uuid4())
        self.user: user.UserImpl = None
        self.max_attempts: int
        self.answer: str = ''
        self.current_attempts: int = 0
        self.difficulty: str = ''

        # All the user attempts in a list formatted
        self.attempts: list = []
        self.has_won: bool = False

        # Correct letters user has gotten
        self.correct_letters: set = set()
    

    @classmethod
    def create_game(cls, 
                    user_name: str,
                    answer_length: int,
                    user_id: str = '', 
                    difficulty: str = ''):
        """Must provide either user id or user name."""
        new_game = cls()
        if not user_id:
            new_game.user = user.UserImpl.create_user(user_name)
        else:
            new_game.user = user.UserImpl.get_user_info(user_id)
        new_game.max_attempts = answer_length+1
        new_game.difficulty = difficulty
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
                'attempts': self.attempts,
                'has_won': self.has_won,
                'difficulty': self.difficulty}
    
    def add_attempt(self, attempt_word: str):
        """Add a user attempt for the game.

        :param str attempt_word: 
        :raises InvalidWordleWord
        :raises ExceededAttempts
        """

        if len(attempt_word) !=  len(self.answer):
            logger.info("Word is not the right length")
            raise exceptions.InvalidAttempt("Word is not the right length")
        
        
        if not DictionaryImpl.check_if_exists(attempt_word):
            logger.info("Word is not valid")
            raise exceptions.InvalidAttempt("Not found in the wordle dictionary")
        
        if self.current_attempts < self.max_attempts:
            self.current_attempts += 1
        else:
            raise exceptions.ExceededAttempts
        

        # hard must include correct letters
        self._difficulty_handler(attempt_word)

        # processed answer with correct or incorrect letters
        attempt_answer = self._build_attempt_answer(attempt_word)

        self.attempts.append(attempt_answer)

        self._update_attempt_db()

        return attempt_answer
    
        # Update game in dynamodb
    
    def _build_attempt_answer(self, attempt_word: str):
        """Build attempt answer list. Assumes same length as answer"""
        attempt_answer = []

        for i in range(len(attempt_word)):
            letter_map = {}
            ltr = attempt_word[i]
            if  ltr == self.answer[i]:
                self.correct_letters.add(ltr)
                letter_map['letter'] = ltr
                letter_map['letter_answer'] = enums.LetterAnswer.CORRECT.name
            elif ltr in self.answer:
                letter_map['letter'] = ltr
                letter_map['letter_answer'] = enums.LetterAnswer.WRONG_SPOT.name
            else:
                letter_map['letter'] = ltr
                letter_map['letter_answer'] = enums.LetterAnswer.INCORRECT.name
            attempt_answer.append(letter_map)


        if attempt_word == self.answer:
            self.has_won = True

        return attempt_answer
    
    def _difficulty_handler(self, attempt_word) -> bool:
        """Difficulty handler. If hard mode then check if all correct letters included"""

        if self.difficulty == enums.Difficulty.HARD.name:
            attempt_ltrs = set(attempt_word)
            correct_ltrs = set(self.correct_letters)
            inter = attempt_ltrs.intersection(correct_ltrs)
            if inter != correct_ltrs:
                raise exceptions.InvalidAttempt("Must include all the correct letters in attempt for HARD.")

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
        expression = "set CurrentAttempts = :ca, Attempts = :a, CorrectLetters = :cl, HasWon = :hw"
        attr_values = {":ca": self.current_attempts, 
                       ":a": self.attempts, 
                       ":cl": list(self.correct_letters),
                       ":hw": self.has_won}

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
                             'Attempts': self.attempts,
                             'HasWon': self.has_won,
                             'Difficulty': self.difficulty,
                             'CorrectLetters': list(self.correct_letters)})


    @classmethod
    def _convert_db_to_object(cls, data: dict):
            rtr_game = cls()
            rtr_game.game_id = data.get('GameID')
            rtr_game.user = user.UserImpl(user_name=data.get('UserName'), user_id=data.get('UserID'))
            rtr_game.max_attempts = data.get('MaxAttempts')
            rtr_game.answer = data.get('Answer')
            rtr_game.current_attempts = data.get('CurrentAttempts')
            rtr_game.attempts = data.get('Attempts')
            rtr_game.difficulty = data.get('Difficulty')
            rtr_game.has_won = data.get('HasWon')
            rtr_game.correct_letters = set(data.get('CorrectLetters'))

            return rtr_game


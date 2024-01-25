import marshmallow
import marshmallow.validate as validate

import impl.enums as enums

_fields = marshmallow.fields


class CreateGameRequestSchema(marshmallow.Schema):
    user_name = _fields.String(required=True)
    answer_length = _fields.Int(default=5, validate=validate.Range(5,8))
    user_id = _fields.String()
    difficulty = _fields.String(
        validate=validate.OneOf(enums.DIFFICULTY_NAMES), 
        load_default=enums.Difficulty.EASY.name)


class PostAnswerRequestSchema(marshmallow.Schema):
    attempt_word = _fields.String(required=True)

    @marshmallow.post_load
    def process(self, data, **kwargs):
        data['attempt_word'] = data['attempt_word'].lower()
        return data

class LetterAnswer(marshmallow.Schema):
    letter = _fields.String()
    letter_answer = _fields.String(
        validate=validate.OneOf(enums.LETTER_ANSWER_NAMES)
    )
        
class PostAnswerResponseSchema(marshmallow.Schema):
    attempt_answer = _fields.List(_fields.Nested(LetterAnswer))


class CreateGameResponseSchema(marshmallow.Schema):
    game_id = _fields.String()
    user_name = _fields.String()
    user_id = _fields.String()
    answer = _fields.String()
    max_attempts = _fields.Int()
    has_won = _fields.Bool()
    difficulty = _fields.String()
    attempts = _fields.List(_fields.List(_fields.Nested(LetterAnswer)))


class GetGameResponseSchema(marshmallow.Schema):
    game_id = _fields.String()
    user_id = _fields.String()
    user_name = _fields.String()
    answer = _fields.String()
    max_attempts = _fields.Int()
    current_attempts = _fields.Int()
    has_won = _fields.Bool()
    difficulty = _fields.String()
    attempts = _fields.List(_fields.List(_fields.Nested(LetterAnswer)))


class GetUserResponseSchema(marshmallow.Schema):
    user_id = _fields.String()
    user_name = _fields.String()


class GetGamesByUser(marshmallow.Schema):
    games = _fields.List(_fields.Nested(GetGameResponseSchema), many=True)


class NewWordRequest(marshmallow.Schema):
    word = _fields.String()

    @marshmallow.post_load(pass_many=True)
    def check_length(self, data, many, **kwargs):
        if data:
            if len(data['word']) < 5 or len(data['word']) > 9:
                raise marshmallow.ValidationError("New wordle word must be at least 5 and less than 9 characters long.")
        return data
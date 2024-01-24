import marshmallow
import marshmallow.validate as validate

import impl.enums as enums

_fields = marshmallow.fields


class CreateGameRequestSchema(marshmallow.Schema):
    user_name = _fields.String(required=True)
    answer_length = _fields.Int(default=5, min=5, max=8)
    user_id = _fields.String()


class PostAnswerRequestSchema(marshmallow.Schema):
    attempt_word = _fields.String(required=True)


class AttemptAnswer(marshmallow.Schema):
    letter = _fields.String()
    letter_answer = _fields.String(
        validate=validate.OneOf(enums.LETTER_ANSWER_NAMES)
    )

class PostAnswerResponseSchema(marshmallow.Schema):
    attempt_answers = _fields.List(_fields.Nested(AttemptAnswer))


class CreateGameResponseSchema(marshmallow.Schema):
    game_id = _fields.String()
    user_name = _fields.String()
    user_id = _fields.String()
    answer = _fields.String()
    max_attempts = _fields.Int()


class GetGameResponseSchema(marshmallow.Schema):
    game_id = _fields.String()
    user_id = _fields.String()
    user_name = _fields.String()
    answer = _fields.String()
    max_attempts = _fields.Int()
    current_attempts = _fields.Int()


class GetUserResponseSchema(marshmallow.Schema):
    user_id = _fields.String()
    user_name = _fields.String()

class GetGamesByUser(marshmallow.Schema):
    games = _fields.List(_fields.Nested(GetGameResponseSchema))
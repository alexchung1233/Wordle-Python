import marshmallow
import marshmallow.validate as validate

import impl.enums as enums

_fields = marshmallow.fields


class AttemptAnswer(marshmallow.Schema):
    letter = _fields.String()
    letter_answer = _fields.String(
        validate=validate.OneOf(enums.LETTER_ANSWER_NAMES)
    )


class CreateGameRequestSchema(marshmallow.Schema):
    user_name = _fields.String(required=True)
    answer_letters = _fields.Int(default=5, min=5, max=8)



class PostAnswerRequestSchema(marshmallow.Schema):
    attempt_word = _fields.String(required=True)


class PostAnswerResponseSchema(marshmallow.Schema):
    attempt_answers = _fields.List(_fields.Nested(AttemptAnswer))



class CreateGameResponseSchema(marshmallow.Schema):
    game_id = _fields.String()
    user_id = _fields.String()
    answer = _fields.String()
    max_attempts = _fields.Int()

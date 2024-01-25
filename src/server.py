"""Wordle server logic"""
import logging 

import flask as flask
import marshmallow

import impl.game as game
import impl.user as user
import schemas as schemas
import exceptions as exceptions

logger = logging.getLogger(__name__)
request = flask.request

GameImpl = game.GameImpl
UserImpl = user.UserImpl

CreateGameRequestSchema = schemas.CreateGameRequestSchema
CreateGameResponseSchema = schemas.CreateGameResponseSchema
PostAnswerRequestSchema = schemas.PostAnswerRequestSchema
PostAnswerResponseSchema = schemas.PostAnswerResponseSchema
GetGameResponseSchema = schemas.GetGameResponseSchema
GetUserResponseSchema = schemas.GetUserResponseSchema

Flask = flask.Flask

app = Flask(__name__)

@app.route('/v1/wordle/game/<game_id>', methods=['GET'])
def get_game(game_id: str):
   logger.info("Request made to GET 'wordle/%s'", game_id)

   retrieved_game = GameImpl.get_game(game_id=game_id)

   payload = retrieved_game.to_dict()

   response = GetGameResponseSchema().dumps(payload)
   return response, 200


@app.route('/v1/wordle/user/<user_id>', methods=['GET'])
def get_user_info(user_id: str):
   logger.info("Request made to GET 'wordle/%s'", user_id)
   try:
      user_info = UserImpl.get_user_info(user_id)
   except exceptions.UserNotFound:
      return 'User was not found with user_id', 409
   
   payload = user_info.to_dict()

   response = GetUserResponseSchema().dumps(payload)

   return response, 200

@app.route('/v1/wordle/user/<user_id>', methods=['GET'])
def get_games_by_user(user_id: str):
   logger.info("Request made to GET 'wordle/%s'", user_id)
   user_info = UserImpl.get_user_info(user_id)

   payload = user_info.to_dict()

   response = GetUserResponseSchema.dumps(payload)

   return response, 200

@app.route('/v1/wordle/game', methods=['POST'])
def create_game():
   """POST to create a new Wordle Game"""

   logger.info("Request made to POST 'wordle/")
   # Validate the request during deserialization 
   try:
      data = CreateGameRequestSchema().loads(request.data)
   except marshmallow.ValidationError as exc:
      logger.error("invalid payload %s", exc)
      return f"Invalid request payload: {exc}", 400 

   user_name = data.get('user_name')
   answer_length = data.get('answer_length')
   user_id = data.get('user_id')

   try:
      new_game = GameImpl.create_game(
         user_name=user_name,
         user_id=user_id,
         answer_length=answer_length)
   except exceptions.UserNotFound:
      return 'User was not found with user_id', 409
   
   payload = new_game.to_dict()

   # serialize the response
   response = CreateGameResponseSchema().dumps(payload)

   return response, 201

@app.route('/v1/wordle/game/<game_id>/attempt', methods=['POST'])
def post_answer(game_id):
   """POST endpoint to attempt an answer for the game id"""

   logger.info("Request made to GET 'wordle/<game_id>")
   if not request.data:
      return "invalid request payload", 400
   # Validate the request during deserialization 
   try:
      data = PostAnswerRequestSchema().loads(request.data)
   except marshmallow.ValidationError as exc:
      logger.error("invalid payload %s", exc)
      return f"Invalid request payload: {exc}", 400 
   
   attempt_word = data.get('attempt_word')

   game = GameImpl.get_game(game_id)

   attempt_answers = game.add_attempt(attempt_word)

   payload = {'attempt_answers': attempt_answers}

   response = schemas.PostAnswerResponseSchema().dumps(payload)

   return response, 201


   @app.route('/v1/wordle/dictionary', methods=['POST'])
   def post_new_word(game_id):
      pass

@app.route('/', methods=['GET'])
def healthcheck():
   logger.info("Hello check successful")
   return 'health check good', 200



def get_server():
   return app
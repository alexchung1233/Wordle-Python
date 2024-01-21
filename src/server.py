"""Wordle server logic"""
import flask as flask
import logging 
import marshmallow
import http

import schemas as schemas

logger = logging.getLogger(__name__)
request = flask.request

CreateGameRequestSchema = schemas.CreateGameRequestSchema
CreateGameResponseSchema = schemas.CreateGameRequestSchema
PostAnswerRequestSchema = schemas.PostAnswerRequestSchema
PostAnswerResponseSchema = schemas.PostAnswerResponseSchema

Flask = flask.Flask

app = Flask(__name__)

@app.route('/v1/wordle/game/<game_id>', methods=['GET'])
def get_game_info(game_id):
   logger.info("Request made to GET 'wordle/%s'", game_id)
   return 'Hello world'

@app.route('/v1/wordle/user/<user_id>', methods=['GET'])
def get_user_info(user_id):
   logger.info("Request made to GET 'wordle/%s'", user_id)
   return "User data sent", 200


@app.route('/v1/wordle/game', methods=['POST'])
def create_game(game_id):
   """POST to create a new Wordle Game"""

   logger.info("Request made to POST 'wordle/")
   # Validate the request during deserialization 
   try:
      data = CreateGameRequestSchema().loads(request.data)
   except marshmallow.ValidationError as exc:
      logger.error("invalid payload %s", exc)
      return "Invalid request payload", 400 

   payload = {"game_id"}

   # serialize the response
   response = CreateGameResponseSchema().dumps(payload)

   return "Game created", 201

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
      return "Invalid request payload", 400 
   
   return "Answer successfully processed", 201




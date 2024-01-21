"""Wordle server logic"""
import flask as flask
import logging 

logger = logging.getLogger(__name__)

Flask = flask.Flask

app = Flask(__name__)

@app.route('/wordle/<game_id>', methods=['GET'])
def get_game_info(game_id):
   logger.info("Request made to GET 'wordle/%s'", game_id)
   return 'Hello world'




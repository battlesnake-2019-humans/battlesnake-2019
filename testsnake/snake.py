import bottle
from snakelib.gamestate import *

application = bottle.app()


@application.post("/start")
def start():
    return make_start_response(color="#FF0000")


@application.post("/move")
def move():
    state = GameState.from_snake_request(bottle.request.json)
    return make_move_response(move="left")

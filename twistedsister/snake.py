from bottle import default_app, request
from snakelib.gamestate import *

application = default_app()


@application.post("/start")
def start():
    state = GameState.from_snake_request(request.json)
    return make_start_response(color="#FF0000")


@application.post("/move")
def move():
    state = GameState.from_snake_request(request.json)

    map_3headed = state.get_map_3headed()
    result = dijkstra(map_3headed, state.you.head())

    return make_move_response(move="left")


@application.post("/end")
def end():
    pass


if __name__ == "__main__":
    application.run(port=8080)

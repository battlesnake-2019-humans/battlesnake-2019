from bottle import default_app, request
from snakelib.gamestate import *
from snakelib.crashstore import CrashStore

application = default_app()
crashstore = CrashStore()


@application.post("/start")
@crashstore.game_start
def start(state):
    return make_start_response(color="#FF0000")


@application.post("/move")
@crashstore.game_move
def move(state):
    map_3headed = state.get_map_3headed()

    result = dijkstra(map_3headed, state.you.head())

    return make_move_response(move="left")


@application.post("/end")
@crashstore.game_end
def end(state):
    pass


if __name__ == "__main__":
    application.run(port=8080)

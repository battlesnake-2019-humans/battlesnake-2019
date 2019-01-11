import json
import bottle
import traceback
from snakelib.gamestate import *
from snakelib.pathfinding import *
from snakelib.crashstore import CrashStore

g_crashstore = CrashStore()
application = bottle.app()

@application.post("/start")
def start():
    # Init crash dumps
    state = GameState.from_snake_request(bottle.request.json)
    global g_crashstore
    g_crashstore.init_game(state.game_id)

    return make_start_response(color="#FF0000")


@application.post("/move")
def move():
    state = GameState.from_snake_request(bottle.request.json)

    try:
        head_x, head_y = state.you.head()
        p = state.dijkstra_from(head_x, head_y)[1]

        nearestfood_x, nearestfood_y = state.find_nearest(head_x, head_y, MAP_FOOD)[0]
        path = path_to(p, nearestfood_x, nearestfood_y)
        next_move = next(get_moves_from_path(path))

        return make_move_response(move=next_move)
    except Exception:
        global g_crashstore
        g_crashstore.log_crash(state, traceback.format_exc())
        raise


@application.post("/end")
def end():
    state = GameState.from_snake_request(bottle.request.json)

    # If we encountered a crash, dump trace information
    global g_crashstore
    if g_crashstore.num_logged_crashes(state.game_id) > 0:
        g_crashstore.dump_game_to_file(state.game_id, "crash_%s.json" % state.game_id)


if __name__ == "__main__":
    application.run(port=8000)

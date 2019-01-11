import json
import bottle
import traceback
from snakelib.gamestate import *
from snakelib.pathfinding import *

g_crashdumps = {}
application = bottle.app()


def crash_dump(state, trace):
    global g_crashdumps
    g_crashdumps[state.game_id].append({
        "trace": trace,
        "state": state.dump_state_json()
    })


@application.post("/start")
def start():
    # Init crash dumps
    global g_crashdumps
    state = GameState.from_snake_request(bottle.request.json)
    g_crashdumps[state.game_id] = []

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
        crash_dump(state, traceback.format_exc())
        raise


@application.post("/end")
def end():
    state = GameState.from_snake_request(bottle.request.json)

    # If we encountered a crash, dump trace information
    global g_crashdumps
    if len(g_crashdumps[state.game_id]) > 0:
        print("Dump please!")
        with open("crash_%s.json" % state.game_id, "w") as crash_file:
            crash_file.write(json.dumps(g_crashdumps[state.game_id]))


if __name__ == "__main__":
    application.run(port=8000)

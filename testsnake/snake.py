import sys
import bottle
from snakelib.gamestate import *
from snakelib.pathfinding import *
from snakelib.crashstore import CrashStore

g_crashstore = CrashStore()
application = bottle.app()


@application.post("/start")
@g_crashstore.game_start
def start(state):
    # Init crash dumps
    return make_start_response(color="#FF0000")


@application.post("/move")
@g_crashstore.game_move
def move(state):
    head_x, head_y = state.you.head()
    result = state.dijkstra_from(head_x, head_y)

    nearestfood_x, nearestfood_y = state.find_nearest(head_x, head_y, MAP_FOOD)[0]
    moves = list(result.get_moves_to(nearestfood_x, nearestfood_y))
    next_move = moves[0]
    print("Target: (%d, %d) Head: (%d, %d) Next Move: %s" % (nearestfood_x, nearestfood_y, head_x, head_y, next_move))

    return make_move_response(move=next_move)


@application.post("/end")
@g_crashstore.game_end
def end(state):
    pass


if __name__ == "__main__":
    application.run(port=8000)

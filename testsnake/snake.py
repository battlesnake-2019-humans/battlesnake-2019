import bottle
from snakelib.gamestate import *
from snakelib.pathfinding import *

application = bottle.app()


@application.post("/start")
def start():
    return make_start_response(color="#FF0000")


@application.post("/move")
def move():
    state = GameState.from_snake_request(bottle.request.json)

    head_x, head_y = state.you.head()
    p = state.dijkstra_from(head_x, head_y)[1]

    nearestfood_x, nearestfood_y = state.find_nearest(head_x, head_y, MAP_FOOD)[0]
    path = path_to(p, nearestfood_x, nearestfood_y)
    next_move = next(get_moves_from_path(path))

    return make_move_response(move=next_move)


if __name__ == "__main__":
    application.run(port=8000)

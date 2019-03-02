from bottle import default_app, request
from snakelib.gamestate import *
from snakelib.crashstore import CrashStore

application = default_app()
crashstore = CrashStore()


def get_snake_scores(state, snakes):
    snake_scores = {}
    for snake in snakes:
        snake_scores[snake.id] = state.dijkstra_from(snake.head().x, snake.head().y)

    return snake_scores


@application.post("/start")
@crashstore.game_start
def start(state):
    return make_start_response(color="#00FF00")


@application.post("/move")
@crashstore.game_move
def move(state):
    if len(state.board.snakes) > 3:
        # EARLY GAME STRATEGY: stay far away from other snakes!

        # Get dijkstra scores for all snakes
        snake_scores = get_snake_scores(state, state.board.snakes)

        best_food = state.board.food[0]
        farthest_dist = 0
        for food in state.board.food:
            min_dist = state.board.width * state.board.height
            for snake in state.board.snakes:
                # Skip self
                if snake.id == state.you.id:
                    continue

                dist_to_head = snake_scores[snake.id].d[food.y][food.x]
                if dist_to_head < min_dist:
                    min_dist = dist_to_head

            if min_dist > farthest_dist:
                best_food = food
                farthest_dist = min_dist

        # Find path to best food
        my_score = snake_scores[state.you.id]
        moves = list(my_score.get_moves_to(best_food.x, best_food.y))

        return make_move_response(move=moves[0])
    else:
        # Voronoi strategy: maximize your control space of the board!
        # Get dijkstra scores for all snakes
        snake_scores = get_snake_scores(state, state.board.snakes)

        best_move = None
        best_control_space = 0
        for move in get_possible_snake_moves(state.you, state.get_map()):
            control_space = 0
            for y in range(state.board.height):
                for x in range(state.board.width):
                    min_opposing_score = state.board.width * state.board.height

                    # Count the spaces we CONTROL (can get to first)
                    for snake in state.board.snakes:

                        if snake.id == state.you.id:
                            continue  # skip self: only looking at opposing snakes!

                        if snake_scores[snake.id].d[y][x] < min_opposing_score:
                            min_opposing_score = snake_scores[snake.id][y][x]

                    # If we are closer than the minimum opposing snake distance, then we CONTROL
                    # this space
                    if snake_scores[state.you.id].d[y][x] < min_opposing_score:
                        control_space += 1

            if control_space > best_control_space:
                best_move = move
                best_control_space = control_space

        next_move = get_next_snake_move(state.you.head()[0], state.you.head()[1], best_move[0], best_move[1])
        return make_move_response(move=next_move)


@application.post("/end")
@crashstore.game_end
def end(state):
    pass


@application.post("/ping")
def ping():
    pass


if __name__ == "__main__":
    application.run(port=8080)

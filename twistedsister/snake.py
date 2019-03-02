from bottle import default_app, request
from snakelib.gamestate import *
from snakelib.crashstore import CrashStore

application = default_app()
crashstore = CrashStore()


@application.post("/start")
@crashstore.game_start
def start(state):
    return make_start_response(color="#00FF00")


@application.post("/move")
@crashstore.game_move
def move(state):
    # EARLY GAME STRATEGY: stay far away from other snakes!

    # Get dijkstra scores for all snakes
    snake_scores = {}
    for snake in state.board.snakes:
        snake_scores[snake.id] = state.dijkstra_from(snake.head().x, snake.head().y)

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


@application.post("/end")
@crashstore.game_end
def end(state):
    pass


@application.post("/ping")
def ping():
    pass


if __name__ == "__main__":
    application.run(port=8080)

import numpy as np
from .apis.webhook_2019 import *

MAP_EMPTY = 0
MAP_SNAKE = 1
MAP_FOOD  = 2


def make_start_response(**kwargs):
    return StartResponse(kwargs["color"]).to_dict()


def make_move_response(**kwargs):
    return MoveResponse(kwargs["move"]).to_dict()


class GameState:
    """Main class for tracking game state information. Contains all info on
    snakes, food positions, health, etc.

    For more resource-intensive operations, RAII seems like a good pattern
    here (Resource Acquisition Is Initialization). i.e. get_dijkstra() will
    run Diskstra's algorithm once and store the result for later use.
    """

    def __init__(self):
        self.game_id: str = None
        self.turn:    int = None
        self.board: Board = None
        self.you:   Snake = None

        # Initialized as needed
        self._game_map = None
        self._dijkstra_results = {}

    @staticmethod
    def from_snake_request(req_json):
        """Get a game state from a /move request.
        """
        state = GameState()

        snake_req = SnakeRequest.from_json(req_json)
        state.game_id = snake_req.game.id
        state.turn = snake_req.turn
        state.board = snake_req.board
        state.you = snake_req.you

        return state

    def get_map(self):
        """Get a 2D numpy array representing the game board.
        :return np.ndarray Containing MAP_EMPTY, MAP_FOOD or MAP_SNAKE
        """
        if self._game_map is None:
            self._game_map = self._make_map()
        return self._game_map

    def _make_map(self):
        map = np.full((self.board.height, self.board.width), MAP_EMPTY)

        for x, y in self.board.food:
            map[y][x] = MAP_FOOD
        for snake in self.board.snakes:
            for x, y in snake.body:
                map[y][x] = MAP_SNAKE

        return map

import numpy as np
from .constants import *
from .pathfinding import *
from .apis.webhook_2019 import *
from .utils import *


def make_start_response(**kwargs):
    return StartResponse(kwargs["color"]).to_dict()


def make_move_response(**kwargs):
    return MoveResponse(kwargs["move"]).to_dict()


class GameState:
    """Main class for tracking game state information. Contains all info on
    snakes, food positions, health, etc.

    For more resource-intensive operations, RAII seems like a good pattern
    here (Resource Acquisition Is Initialization). i.e. dijkstra_from() will
    run Diskstra's algorithm once and store the result for later use.
    """

    def __init__(self, **kwargs):
        self.game_id: str = None
        self.turn:    int = None
        self.board: Board = None
        self.you:   Snake = None

        # Initialized as needed
        self._game_map = None
        self._dijkstra_results = {}

        # Hang on to the raw JSON dict in case we need to dump for debugging
        self._json_raw: dict = kwargs.get("json_raw")

    @staticmethod
    def from_snake_request(req_json):
        """Get a game state from a /move request.
        """
        state = GameState(json_raw=req_json)

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

    def get_map_3headed(self):
        """Gets the "3 headed" board state - ANY possible move a snake can make
        will be marked as MAP_SNAKE.

        :return np.ndarray
        """
        game_map = np.zeros((self.board.height, self.board.width), dtype=np.uint8)
        for snake in self.board.snakes:

            # Mark each snake's body (tail can be excluded since we're assuming a move)
            # TODO: What happens if the snake is still growing?
            for x, y in snake.body[:-1]:
                game_map[y][x] = MAP_SNAKE

            # Only mark potential moves for enemy snakes
            if snake.id != self.you.id:
                for x, y in get_possible_snake_moves(snake, game_map):
                    game_map[y][x] = MAP_SNAKE

        for fx, fy in self.board.food:
            game_map[fy][fx] = MAP_FOOD

        return game_map

    def dijkstra_from(self, px, py):
        # Check dijkstra cache
        if (px, py) in self._dijkstra_results:
            return self._dijkstra_results[(px, py)]
        else:
            # Make sure we've populated the game map
            game_map = self.get_map()

            # Run dijkstra and cache results
            result = dijkstra(game_map, (px, py))
            self._dijkstra_results[(px, py)] = result
            return result

    def find_nearest(self, px, py, tile_type: int):
        result = self.dijkstra_from(px, py)
        d, p = result.d, result.p

        # Find tiles with a given type (i.e. food tiles)
        game_map = self.get_map()
        tile_coords = np.argwhere(game_map == tile_type)

        # If no coords returned, we can't find any tiles of the given type
        if np.shape(tile_coords)[1] == 0:
            return None

        # Find closest tile using d matrix
        min_score, cx, cy = np.inf, -1, -1
        for i in range(np.shape(tile_coords)[0]):
            ty, tx = tile_coords[i]
            if d[ty][tx] < min_score:
                min_score = d[ty][tx]
                cx, cy = tx, ty

        return (cx, cy), min_score

    def dump_state_json(self):
        """Dumps the JSON dict the game state was created from (for debugging).
        """
        return self._json_raw

    def _make_map(self):
        map = np.full((self.board.height, self.board.width), MAP_EMPTY)

        for x, y in self.board.food:
            map[y][x] = MAP_FOOD
        for snake in self.board.snakes:
            for x, y in snake.body:
                map[y][x] = MAP_SNAKE

        return map

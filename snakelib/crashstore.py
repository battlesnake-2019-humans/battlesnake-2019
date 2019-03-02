import binascii
import sys
import json
import pickle
import traceback
import bottle
from .gamestate import GameState


class CrashStore:
    """Store for logging exceptions during gameplay. These can later be dumped
    to a file and examined.

    Dump files use a JSON format:
    {
        trace: String traceback of the error
        state: JSON game state information (same as the webhook request that
               would have triggered the error)
    }
    """
    def __init__(self):
        self._store = {}

    def init_game(self, game_id: str):
        """Initializes the crash store for a new game."""
        self._store[game_id] = []

    def log_crash(self, state: GameState, tb):
        """Logs a crash (exception) during a game."""
        if state.game_id not in self._store:
            return

        tb_str = traceback.format_tb(tb)

        self._store[state.game_id].append({
            "trace": tb_str,
            "state": state.dump_state_json()
        })

    def num_logged_crashes(self, game_id: str):
        """Get the number of crashes logged for a given game."""
        if game_id not in self._store:
            return
        return len(self._store[game_id])

    def dump_game_to_file(self, game_id: str, filename: str):
        """Dumps all logged crashes for a given game to a file."""
        if game_id not in self._store:
            return
        with open(filename, 'w') as dumpfile:
            dumpfile.write(json.dumps(self._store[game_id]))

    def game_start(self, func):
        def start_wrapper():
            state = GameState.from_snake_request(bottle.request.json)
            self.init_game(state.game_id)
            return func(state)
        return start_wrapper

    def game_move(self, func):
        def move_wrapper():
            state = GameState.from_snake_request(bottle.request.json)
            try:
                return func(state)
            except Exception as e:
                print(e)
                self.log_crash(state, sys.exc_info()[2])
                raise
        return move_wrapper

    def game_end(self, func):
        def end_wrapper():
            state = GameState.from_snake_request(bottle.request.json)
            if self.num_logged_crashes(state.game_id) > 0:
                self.dump_game_to_file(state.game_id, "crash_%s.json" % state.game_id)

            return func(state)
        return end_wrapper


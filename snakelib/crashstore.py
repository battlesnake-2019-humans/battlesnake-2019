import binascii
import sys
import json
import pickle
import traceback
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
            raise Exception("Game %s not initialized in crash store")

        tb_str = traceback.format_tb(tb)

        self._store[state.game_id].append({
            "trace": tb_str,
            "state": state.dump_state_json()
        })

    def num_logged_crashes(self, game_id: str):
        """Get the number of crashes logged for a given game."""
        return len(self._store[game_id])

    def dump_game_to_file(self, game_id: str, filename: str):
        """Dumps all logged crashes for a given game to a file."""
        with open(filename, 'w') as dumpfile:
            dumpfile.write(json.dumps(self._store[game_id]))

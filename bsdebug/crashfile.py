from snakelib.gamestate import GameState


class CrashFile:
    def __init__(self, **kwargs):
        self.trace: str = kwargs.get("trace")
        self.state: dict = GameState.from_snake_request(kwargs.get("state"))

    @staticmethod
    def from_json(json_dict):
        return CrashFile(**json_dict)

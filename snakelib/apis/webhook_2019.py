"""
Battlesnake Webhook API Implementation
---------------------------------------

An implementation of all models in the 'Snake' webhook API. Response objects
are implemented as superclasses of dict for easy conversion to JSON.
"""

from typing import List


class Coords:
    def __init__(self, **kwargs):
        self.x: int = kwargs.get('x')
        self.y: int = kwargs.get('y')

    @staticmethod
    def from_json(json_dict):
        c = Coords()
        c.x = json_dict["x"]
        c.y = json_dict["y"]
        return c

    def __getitem__(self, i):
        return [self.x, self.y][i]


class Snake:
    def __init__(self, **kwargs):
        self.id:     str = kwargs.get("id")
        self.name:   str = kwargs.get("name")
        self.health: int = kwargs.get("health")
        self.body:   List[Coords] = kwargs.get("body")

    @staticmethod
    def from_json(json_dict):
        s = Snake()
        s.id = json_dict.get('id')
        s.name = json_dict.get('name')
        s.health = json_dict.get('health')

        if type(json_dict.get('body')) == list:
            s.body = [Coords.from_json(x) for x in json_dict['body']]

        return s

    def head(self):
        if getattr(self, 'body'):
            return self.body[0]


class Board:
    def __init__(self, **kwargs):
        self.width:  int = kwargs.get("width")
        self.height: int = kwargs.get("height")
        self.food:   List[Coords] = kwargs.get("food")
        self.snakes: List[Snake] = kwargs.get("snakes")

    @staticmethod
    def from_json(json_dict):
        b = Board()
        b.height = json_dict.get('height')
        b.width = json_dict.get('width')

        if type(json_dict.get('food')) == list:
            b.food = [Coords.from_json(x) for x in json_dict['food']]

        if type(json_dict.get('snakes')) == list:
            b.snakes = [Snake.from_json(x) for x in json_dict['snakes']]

        return b


class Game:
    def __init__(self, **kwargs):
        self.id: str = kwargs.get("id")

    @staticmethod
    def from_json(json_dict):
        g = Game()
        g.id = json_dict.get('id')
        return g


class SnakeRequest:
    def __init__(self, **kwargs):
        self.turn:  int = kwargs.get("turn")
        self.game:  Game = kwargs.get("game")
        self.board: Board = kwargs.get("board")
        self.you:   Snake = kwargs.get("you")

    @staticmethod
    def from_json(json_dict):
        req = SnakeRequest()
        req.turn = json_dict.get('turn')

        if type(json_dict.get('game')) == dict:
            req.game = Game.from_json(json_dict['game'])

        if type(json_dict.get('board')) == dict:
            req.board = Board.from_json(json_dict['board'])

        if type(json_dict.get('you')) == dict:
            req.you = Snake.from_json(json_dict['you'])

        return req


class MoveResponse:
    def __init__(self, move):
        self.move: str = move

    def to_dict(self):
        assert self.move in ['up', 'down', 'left', 'right'], \
            "Move must be one of [up, down, left, right]"
        return {"move": self.move}


class StartResponse:
    def __init__(self, color):
        self.color: str = color

    def to_dict(self):
        assert type(self.color) is str, "Color value must be string"
        return {"color": self.color}

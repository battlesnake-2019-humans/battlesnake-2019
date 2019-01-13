import csv
import json
import random
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from snakelib.gamestate import GameState

COLORS_FILE = Path(__file__).absolute().parent / "colors.csv"


def read_colors():
    with open(COLORS_FILE, 'r') as colorsfile:
        reader = csv.reader(colorsfile)
        return [row[1] for row in reader]


class BoardGraph:
    def __init__(self, state: GameState):
        self._state = state
        self._plt = plt

        self._unused_colors = read_colors()

        # Drawing and animating shapes in Matplotlib:
        # https://nickcharlton.net/posts/drawing-animating-shapes-matplotlib.html
        self._make_axes()
        self._draw_food()
        self._draw_snakes()

    def show(self):
        return self._plt.show()

    def _make_axes(self):
        bw, bh = self._state.board.width, self._state.board.height
        # TODO: plot tick labels in middle of square
        self._plt.xticks(np.arange(0, bw + 1))
        self._plt.yticks(np.arange(0, bh + 1))

        self._plt.gca().invert_yaxis()

        self._plt.grid()
        self._plt.gca().set_aspect("equal")

    def _draw_food(self):
        for fx, fy in self._state.board.food:
            circle = self._plt.Circle((fx + 0.5, fy + 0.5), radius=0.3, fc='y')
            plt.gca().add_patch(circle)

    def _draw_snakes(self):
        for snake in self._state.board.snakes:
            snake_color = random.choice(self._unused_colors)
            self._unused_colors.remove(snake_color)

            line = self._plt.Polygon([(c.x + 0.5, c.y + 0.5) for c in snake.body],
                                     closed=None, fill=None, linewidth=7, capstyle='round',
                                     edgecolor=snake_color)
            plt.gca().add_patch(line)


if __name__ == "__main__":
    with open("sample_data/test_state.json", 'r') as statefile:
        state = GameState.from_snake_request(json.load(statefile))

    BoardGraph(state).show()

from .gamestate import MAP_SNAKE


def neighbors_of(x, y, map):
    """Get the neighboring cells of a given cell. Excludes cells that are
    outside the boundaries of the world.
    :param x: X coordinate of cell
    :param y: Y coordinate of cell
    :param map: Map containing the cell.
    :return Iterator of all neighboring cells.
    """
    assert 0 <= x < map.shape[1], "X coordinate must be in bounds!"
    assert 0 <= y < map.shape[0], "Y coordinate must be in bounds!"

    if x + 1 < map.shape[1]:
        yield x + 1, y
    if y + 1 < map.shape[0]:
        yield x, y + 1
    if x - 1 >= 0:
        yield x - 1, y
    if y - 1 >= 0:
        yield x, y - 1


def get_possible_snake_moves(snake, map):
    # Find all possible moves a snake can make
    head = snake.head()
    adjacent_tiles = list(neighbors_of(head[0], head[1], map))

    for x, y in adjacent_tiles:
        if map[y][x] == MAP_SNAKE:
            adjacent_tiles.remove((x, y))

    return adjacent_tiles


def get_next_snake_move(p0x, p0y, p1x, p1y):
    if p0x == p1x:
        if p0y > p1y:
            return "up"
        elif p0y < p1y:
            return "down"
    elif p0y == p1y:
        if p0x < p1x:
            return "right"
        elif p0x > p1x:
            return "left"

import numpy as np
from heapq import *
from .constants import *
from .utils import neighbors_of, get_next_snake_move


class DijkstraResult:
    def __init__(self, px, py, d, p):
        self.root = (px, py)
        self.d = d
        self.p = p

    def path_to(self, x, y):
        """Gets the path to a given point from a predecessor matrix.
        """
        end_point = self.p[y][x]
        points = []

        cur = end_point
        while True:
            np_x = cur % np.shape(self.p)[1]
            np_y = int(cur / np.shape(self.p)[1])
            points.append((np_x, np_y))

            if self.p[np_y][np_x] == -1:
                break
            else:
                cur = self.p[np_y][np_x]

        points.reverse()
        points.append((x, y))  # include target point in path
        return points

    def get_moves_to(self, x, y, lim=-1):
        """Gets moves [up, down, left, right] for a given set of coordinates.
        """
        path = self.path_to(x, y)

        i = 1
        for p1x, p1y in path[1:]:
            p0x, p0y = path[i - 1]

            next_move = get_next_snake_move(p0x, p0y, p1x, p1y)

            # We must have only moved one space, otherwise something's gone
            # horribly wrong with the predecessor matrix!
            assert abs(p1y - p0y) + abs(p0x - p1x) == 1, \
                "Invalid move (%d, %d) -> (%d, %d)" % (p0x, p0y, p1x, p1y)

            # Stop early if caller provided a move limit
            if i >= lim >= 0:
                break
            i += 1

            yield next_move


def dijkstra(map, point):
    """Gets the distance "scores" and predecessor matrix from a given snake's
    head.
    :param map: World map object to map for the snake.
    :param point: Snake to calculate distances from.
    :return: d[] and p[] matrices for each point on the map.
        - p[] matrix uses integers as vertex labels: (y * width) + x
        - None indicates the head of the snake (source node).
        - -1 indicates an inaccessible point.
    """
    d = np.full((map.shape[0], map.shape[1]), np.inf)
    p = np.full((map.shape[0], map.shape[1]), -1)
    visited = np.full((map.shape[0], map.shape[1]), False, dtype=np.bool)

    # d at the snake's head should be 0 (we're already there, so no cost!)
    d[point[1]][point[0]] = 0

    pq = [(1, point)]
    heapify(pq)
    while len(pq) > 0:
        next_vert = heappop(pq)[1]
        nv_x, nv_y = next_vert[0], next_vert[1]

        # ignore if we've already visited this vertex
        if visited[nv_y][nv_x]:
            continue

        # consider neighbors of this vertex
        for x, y in neighbors_of(nv_x, nv_y, map):
            if map[y][x] == MAP_SNAKE:
                d[y][x] = -1
                p[y][x] = -1
            elif d[nv_y][nv_x] + 1 < d[y][x]:
                d[y][x] = d[nv_y][nv_x] + 1
                p[y][x] = map.shape[1] * nv_y + nv_x

                # re-add to pq if d[] was updated
                heappush(pq, (d[y][x], (x, y)))

        visited[nv_y][nv_x] = True

    return DijkstraResult(point[0], point[1], d, p)

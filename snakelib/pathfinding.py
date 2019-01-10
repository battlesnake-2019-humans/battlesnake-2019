import numpy as np
from heapq import *
from .gamestate import MAP_SNAKE


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

    return d, p

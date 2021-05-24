import heapq
import math
from collections import defaultdict


class AStarNode:
    def __init__(self, i=-1, j=-1, t=-1, g=math.inf, h=math.inf, F=None, parent=None):
        self.i = i
        self.j = j
        self.t = t
        self.g = g
        self.h = h
        if F is None:
            self.F = self.g + h
        else:
            self.F = F
        self.parent = parent

    def __eq__(self, other):
        return (self.i == other.i) and (self.j == other.j) and (self.t == other.t)

    def __hash__(self):
        return hash((self.i, self.j, self.t))

    def __str__(self):
        return f'(i: {self.i}, j: {self.j}, t: {self.t})'

    def __repr__(self):
        return self.__str__()


class AStarNodeHeap:

    def __init__(self, node, k=0):
        self.node = node
        self.removed = False
        self.k = k

    def __lt__(self, other):
        return (self.node.F, self.node.h, -self.k) < (other.node.F, other.node.h, -other.k)


class AStarOpen:

    def __init__(self):
        self.elements = []
        self.exists = {}
        self.k = 0

    def __len__(self):
        return len(self.elements)

    def __iter__(self):
        return map(lambda n: n.node, self.elements)

    def is_empty(self):
        return len(self.exists) == 0

    def get_best_node(self):
        smallest = heapq.heappop(self.elements)
        while smallest.removed:
            smallest = heapq.heappop(self.elements)
        del self.exists[smallest.node]
        return smallest.node

    def add_node(self, item: AStarNode):
        if item in self.exists:
            old_node = self.exists[item]
            if old_node.node.g <= item.g:
                return
            old_node.removed = True
        new_node_heap = AStarNodeHeap(item, self.k)
        self.k += 1
        heapq.heappush(self.elements, new_node_heap)
        self.exists[item] = new_node_heap


class AStarClosed:
    def __init__(self):
        self.elements = set()

    def __iter__(self):
        return iter(self.elements)

    def __len__(self):
        return len(self.elements)

    def add_node(self, item: AStarNode, *args):
        self.elements.add(item)

    def was_expanded(self, item: AStarNode, *args):
        return item in self.elements


def compute_cost(i1, j1, i2, j2):
    return math.sqrt((i1 - i2) ** 2 + (j1 - j2) ** 2)


def manhattan_distance(i1, j1, i2, j2):
    return abs(i1 - i2) + abs(j1 - j2)


def manhattan_distance_time(i_from, j_from, t_from, i_to, j_to, t_to):
    if t_from > t_to:
        return math.inf
    return abs(i_from - i_to) + abs(j_from - j_to) + abs(t_from - t_to)


class RealDistanceFinder:
    def __init__(self, i_start, j_start, i_goal, j_goal, grid_map):
        status, OPEN, CLOSED, _ = A_star_backward(grid_map, i_goal, j_goal, i_start, j_start)
        self.OPEN = OPEN
        self.CLOSED = CLOSED
        self.i_start = i_start
        self.j_start = j_start
        self.grid_map = grid_map

    def find_dist(self, i, j):
        node = AStarBackwardNode(i, j, 0, 0)
        if node in self.CLOSED:
            return self.CLOSED[node]
        else:
            while not self.OPEN.is_empty():
                cur_node = self.OPEN.get_best_node()
                self.CLOSED.add_node(cur_node)
                if cur_node.i == i and cur_node.j == j:
                    return cur_node.g
                for (i, j) in self.grid_map.get_neighbors(cur_node.i, cur_node.j):

                    new_node = AStarBackwardNode(i, j, g=cur_node.g + 1, h=manhattan_distance(self.i_start, self.j_start, i, j),
                                                 parent=cur_node)
                    if not self.CLOSED.was_expanded(new_node):
                        self.OPEN.add_node(new_node)
            return 10


def do_path(node):
    path = []
    while node.parent is not None:
        path.append((node.i, node.j))
        node = node.parent
    path.append((node.i, node.j))
    path.reverse()
    return path


def A_star(grid_map,
           i_start,
           j_start,
           i_goal,
           j_goal,
           vertex_constraints,
           edge_constraints,
           heuristic_function=manhattan_distance,
           t_start=0):
    OPEN = AStarOpen()
    CLOSED = AStarClosed()
    start_node = AStarNode(i_start, j_start, t_start, 0, 0)
    OPEN.add_node(start_node)
    if len(vertex_constraints) == 0 and len(edge_constraints) == 0:
        status, _, _, path = A_star_backward(grid_map, i_start, j_start, i_goal, j_goal)
        return status, path
    vertex_max_time = max(map(lambda x: x[1], vertex_constraints)) if vertex_constraints else 0
    edge_max_time = max(map(lambda x: x[1], edge_constraints)) if edge_constraints else 0
    max_time = max(edge_max_time, vertex_max_time)
    while not OPEN.is_empty():
        cur_node = OPEN.get_best_node()
        CLOSED.add_node(cur_node)
        if cur_node.i == i_goal and cur_node.j == j_goal and cur_node.t >= max_time:
            return True, do_path(cur_node)
        for (i, j) in grid_map.get_neighbors(cur_node.i, cur_node.j):
            to, frm, t = (i, j), (cur_node.i, cur_node.j), cur_node.t
            if (to, t + 1) in vertex_constraints or \
                    ((to, frm), t) in edge_constraints or \
                    ((frm, to), t) in edge_constraints:
                continue

            new_node = AStarNode(i, j, cur_node.t + 1, g=cur_node.t + 1, h=heuristic_function(i_goal, j_goal, i, j),
                                 parent=cur_node)
            if not CLOSED.was_expanded(new_node):
                OPEN.add_node(new_node)
    return False, None


def A_star_DS(grid_map,
              i_start,
              j_start,
              t_start,
              i_goal,
              j_goal,
              t_goal,
              vertex_constraints,
              edge_constraints,
              heuristic_function=manhattan_distance
              ):
    OPEN = AStarOpen()
    CLOSED = AStarClosed()
    start_node = AStarNode(i_start, j_start, t_start, 0, 0)
    OPEN.add_node(start_node)
    if len(vertex_constraints) == 0 and len(edge_constraints) == 0:
        status, _, _, path = A_star_backward(grid_map, i_start, j_start, i_goal, j_goal)
        return status, path
    vertex_max_time = max(map(lambda x: x[1], vertex_constraints)) if vertex_constraints else 0
    edge_max_time = max(map(lambda x: x[1], edge_constraints)) if edge_constraints else 0
    max_time = max(edge_max_time, vertex_max_time)
    while not OPEN.is_empty():
        cur_node = OPEN.get_best_node()
        CLOSED.add_node(cur_node)
        if cur_node.i == i_goal and cur_node.j == j_goal and cur_node.t == t_goal and cur_node.t >= max_time:
            return True, do_path(cur_node)
        for (i, j) in grid_map.get_neighbors(cur_node.i, cur_node.j):
            to, frm, t = (i, j), (cur_node.i, cur_node.j), cur_node.t
            if (to, t + 1) in vertex_constraints or \
                    ((to, frm), t) in edge_constraints or \
                    ((frm, to), t) in edge_constraints:
                continue

            new_node = AStarNode(i, j, cur_node.t + 1, g=cur_node.t + 1,
                                 h=heuristic_function(i, j, i_goal, j_goal),
                                 parent=cur_node)
            if not CLOSED.was_expanded(new_node) and new_node.t + heuristic_function(i, j, i_goal, j_goal) <= t_goal:
                OPEN.add_node(new_node)
    return False, None


class AStarBackwardNode:
    def __init__(self, i=-1, j=-1, g=math.inf, h=math.inf, F=None, parent=None):
        self.i = i
        self.j = j
        self.g = g
        self.h = h
        if F is None:
            self.F = self.g + h
        else:
            self.F = F
        self.parent = parent

    def __eq__(self, other):
        return (self.i == other.i) and (self.j == other.j)

    def __hash__(self):
        return hash((self.i, self.j))


class AStarBackwardClosed:
    def __init__(self):
        self.elements = {}

    def __iter__(self):
        return iter(self.elements.keys())

    def __len__(self):
        return len(self.elements.keys())

    def add_node(self, item: AStarBackwardNode, *args):
        self.elements[item] = item.g

    def was_expanded(self, item: AStarBackwardNode, *args):
        return item in self.elements

    def __getitem__(self, item):
        return self.elements[item]


def A_star_backward(grid_map,
                    i_start,
                    j_start,
                    i_goal,
                    j_goal,
                    heuristic_function=manhattan_distance):
    OPEN = AStarOpen()
    CLOSED = AStarBackwardClosed()
    start_node = AStarBackwardNode(i_start, j_start, 0, 0)
    OPEN.add_node(start_node)
    while not OPEN.is_empty():
        cur_node = OPEN.get_best_node()
        CLOSED.add_node(cur_node)
        if cur_node.i == i_goal and cur_node.j == j_goal:
            return True, OPEN, CLOSED, do_path(cur_node)
        for (i, j) in grid_map.get_neighbors(cur_node.i, cur_node.j):

            new_node = AStarBackwardNode(i, j, g=cur_node.g + 1, h=heuristic_function(i_goal, j_goal, i, j),
                                         parent=cur_node)
            if not CLOSED.was_expanded(new_node):
                OPEN.add_node(new_node)
    return False, None
import heapq
import math


class AStarNode:
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


class NodeHeap:

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
        del self.exists[(smallest.node.i, smallest.node.j)]
        return smallest.node

    def add_node(self, item: AStarNode):
        if (item.i, item.j) in self.exists:
            old_node = self.exists[(item.i, item.j)]
            if old_node.node.g < item.g:
                return
            old_node.removed = True
        new_node_heap = NodeHeap(item, self.k)
        self.k += 1
        heapq.heappush(self.elements, new_node_heap)
        self.exists[(item.i, item.j)] = new_node_heap


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


def A_star(grid_map, i_start, j_start, i_goal, j_goal, heuristic_function=manhattan_distance,
           open_type=AStarOpen, closed_type=AStarClosed):
    OPEN = open_type()
    CLOSED = closed_type()
    start_node = AStarNode(i_start, j_start, 0, 0)
    OPEN.add_node(start_node)
    while not OPEN.is_empty():
        cur_node = OPEN.get_best_node()
        CLOSED.add_node(cur_node)
        if cur_node.i == i_goal and cur_node.j == j_goal:
            return True, cur_node, CLOSED, OPEN
        for (i, j) in grid_map.GetNeighbors(cur_node.i, cur_node.j):
            dist = compute_cost(cur_node.i, cur_node.j, i, j)
            new_node = AStarNode(i, j, g=cur_node.g + dist, h=heuristic_function(i_goal, j_goal, i, j), parent=cur_node)
            if not CLOSED.was_expanded(new_node):
                OPEN.add_node(new_node)
    return False, None, CLOSED, OPEN

import heapq
import math


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
            if old_node.node.g < item.g:
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
           heuristic_function=manhattan_distance
           ):
    OPEN = AStarOpen()
    CLOSED = AStarClosed()
    start_node = AStarNode(i_start, j_start, 0, 0, 0)
    OPEN.add_node(start_node)
    while not OPEN.is_empty():
        cur_node = OPEN.get_best_node()
        CLOSED.add_node(cur_node)
        if cur_node.i == i_goal and cur_node.j == j_goal:
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

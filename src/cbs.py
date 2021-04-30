import math


class CBSNode:
    def __init__(self, constraints, parent=None):
        self.constraints = constraints
        if parent is not None:
            self.solutions = parent.solutions
        else:
            self.solutions = None
        self.cost = math.inf
        self.parent = parent
        self.find_best_solutions()
        self.sum_of_individual_costs()

    def find_best_solutions(self):
        pass

    def sum_of_individual_costs(self):
        pass


class CBSOpen:
    def __init__(self):
        pass

    def add_node(self, node):
        pass

    def is_empty(self):
        pass

    def get_best_node(self):
        pass


def find_conflict(node):
    return True, 0, 0, 0, 0  # found, a_i, a_j, v, t


def cbs(grid_map):
    OPEN = CBSOpen()
    root = CBSNode([])
    OPEN.add_node(root)
    while not OPEN.is_empty():
        best_node = OPEN.get_best_node()
        found, a, b, v, t = find_conflict(best_node)
        if not found:
            return best_node.solutions
        new_node_1 = CBSNode(best_node.constrainsts + [(b, v, t)], best_node)
        new_node_2 = CBSNode(best_node.constrainsts + [(a, v, t)], best_node)
        if new_node_1.cost < math.inf:
            OPEN.add_node(new_node_1)
        if new_node_2.cost < math.inf:
            OPEN.add_node(new_node_2)

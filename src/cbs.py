import math
import heapq

from src.a_star import A_star


class CBSNode:
    def __init__(self, constraints, grid_map, agents, parent=None, k=0):
        self.constraints = constraints
        if parent is not None:
            self.solutions = parent.solutions
        else:
            self.solutions = None
        self.k = k
        self.cost = math.inf
        self.parent = parent
        self.find_best_solutions(grid_map, agents)
        self.sum_of_individual_costs()

    def __lt__(self, other: 'CBSNode'):
        return (self.cost, -self.k) < (other.cost, other.k)

    def find_best_solutions(self, grid_map, agents):
        self.solutions = []
        for i, (s, f) in enumerate(agents):
            found, path = A_star(grid_map, s[0], s[1], f[0], f[1], self.constraints.get(i, []))
            if not found:
                self.cost = math.inf
                return
            self.solutions.append(path)

    def sum_of_individual_costs(self):
        self.cost = 0
        for path in self.solutions:
            self.cost += len(path)


class CBSOpen:
    def __init__(self):
        self.elements = []

    def add_node(self, node):
        heapq.heappush(self.elements, node)

    def is_empty(self):
        return len(self.elements) == 0

    def get_best_node(self):
        return heapq.heappop(self.elements)


def find_conflict(node):
    # todo: ай ай ай, как неэффективно я сделал
    # да еще и неправильно. После последнего шага агент все время стоит в одной и той же клетке
    # теперь правильно, но некрасиво
    n = len(node.solutions)
    for i in range(n):
        for j in range(i + 1, n):
            sol1 = node.solutions[i]
            sol2 = node.solutions[j]
            for t in range(max(len(sol1), len(sol2))):
                if t >= len(sol1):
                    v1 = sol1[-1]
                else:
                    v1 = sol1[t]
                if t >= len(sol2):
                    v2 = sol2[-1]
                else:
                    v2 = sol2[t]
                if v1 == v2:
                    return True, i, j, v1, t
    return False, 0, 0, 0, 0  # found, a_i, a_j, v, t


class CBS:
    def __init__(self, grid_map, agents):
        self.grid_map = grid_map
        self.agents = agents
        self.OPEN = CBSOpen()
        self.root = CBSNode({}, grid_map, agents)
        self.OPEN.add_node(self.root)
        self.counter = 0

    def find_best_solutions(self):
        while not self.OPEN.is_empty():
            best_node = self.OPEN.get_best_node()
            found, a, b, v, t = find_conflict(best_node)
            if not found:
                return best_node.solutions, best_node.cost
            # todo: вынести это в отдельную функцию и вообще сделать посимпатичнее (мб использовать setdefault)
            constraints = best_node.constraints.copy()
            constraints[b] = constraints.get(b, []) + [(v, t)]
            new_node_1 = CBSNode(constraints, self.grid_map,
                                 self.agents, best_node, self.counter)
            self.counter += 1
            constraints = best_node.constraints.copy()
            constraints[a] = constraints.get(a, []) + [(v, t)]
            new_node_2 = CBSNode(constraints, self.grid_map,
                                 self.agents, best_node, self.counter)
            self.counter += 1
            if new_node_1.cost < math.inf:
                self.OPEN.add_node(new_node_1)
            if new_node_2.cost < math.inf:
                self.OPEN.add_node(new_node_2)

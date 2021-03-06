import math
import heapq
from collections import defaultdict
from copy import deepcopy

from src.a_star import A_star, RealDistanceFinder


class CBSNode:
    def __init__(self, vertex_constraints, edge_constraints, grid_map, agents, parent=None, k=0, agents_to_recompute_ind=None):
        self.vertex_constraints = vertex_constraints
        self.edge_constraints = edge_constraints
        self.grid_map = grid_map
        self.agents = agents
        if parent is not None:
            self.solutions = deepcopy(parent.solutions)
        else:
            self.solutions = [None for _ in range(len(agents))]
        if agents_to_recompute_ind is None:
            agents_to_recompute_ind = range(len(agents))
        self.k = k
        self.cost = None
        self.parent = parent
        self.find_best_solutions(grid_map, agents_to_recompute_ind)
        self.sum_of_individual_costs()

    def __lt__(self, other: 'CBSNode'):
        return (self.cost, -self.k) < (other.cost, -other.k)

    def find_best_solutions(self, grid_map, agents_to_recompute_ind):
        for i in agents_to_recompute_ind:
            s, f = self.agents[i]
            found, path = A_star(grid_map, s[0], s[1], f[0], f[1], self.vertex_constraints[i], self.edge_constraints[i])
            if not found:
                self.cost = math.inf
                return
            self.solutions[i] = path

    def sum_of_individual_costs(self):
        if self.cost is not None:
            return
        self.cost = 0
        for path in self.solutions:
            while len(path) >= 2 and path[-1] == path[-2]:
                path.pop()
            self.cost += len(path)


class CBSOpen:
    def __init__(self):
        self.elements = []
        self.cnt = 0

    def add_node(self, node):
        heapq.heappush(self.elements, node)
        self.cnt += 1

    def is_empty(self):
        return len(self.elements) == 0

    def get_best_node(self):
        return heapq.heappop(self.elements)


def find_edge_conflict(node: CBSNode):
    # time associated with edge is the start time
    constraints_edges = {}  # map from (from_vertex, to_vertex, from_time) to path
    max_len = len(max(node.solutions, key=lambda x: len(x)))

    for t in range(max_len):
        for i, solution in enumerate(node.solutions):
            if len(solution) <= t + 1:
                continue
            frm, to = solution[t], solution[t + 1]
            if (to, frm, t) in constraints_edges.keys():
                j = constraints_edges[(to, frm, t)]
                return i, j, (frm, to), t

            constraints_edges[(frm, to, t)] = i

    return None, None, None, None


class CBS:
    def __init__(self, grid_map, agents, node_type=CBSNode):
        self.grid_map = grid_map
        self.agents = agents
        self.node_type = node_type
        self.OPEN = CBSOpen()
        self.root = None
        self.make_root()
        self.node_counter = 0

    def make_root(self):
        self.root = self.node_type(defaultdict(lambda: []), defaultdict(lambda: []), self.grid_map, self.agents)
        self.OPEN.add_node(self.root)

    def add_children_from_vertex_constraint(self, node: CBSNode, agent1, agent2, vertex, time):
        edge_constraints = deepcopy(node.edge_constraints)
        vertex_constraints1 = deepcopy(node.vertex_constraints)
        vertex_constraints1[agent1].append((vertex, time))
        new_node_1 = self.node_type(vertex_constraints1, edge_constraints, self.grid_map,
                                    self.agents, node, self.node_counter, agents_to_recompute_ind=[agent1])
        self.node_counter += 1
        vertex_constraints2 = deepcopy(node.vertex_constraints)
        vertex_constraints2[agent2].append((vertex, time))

        new_node_2 = self.node_type(vertex_constraints2, edge_constraints, self.grid_map,
                                    self.agents, node, self.node_counter, agents_to_recompute_ind=[agent2])
        self.node_counter += 1
        if new_node_1.cost < math.inf:
            self.OPEN.add_node(new_node_1)
        if new_node_2.cost < math.inf:
            self.OPEN.add_node(new_node_2)

    def add_children_from_edge_constraint(self, node: CBSNode, agent1, agent2, edge, time):
        vertex_constraints = deepcopy(node.vertex_constraints)
        edge_constraints1 = deepcopy(node.edge_constraints)
        edge_constraints1[agent1].append((edge, time))
        new_node_1 = self.node_type(vertex_constraints, edge_constraints1, self.grid_map,
                                    self.agents, node, self.node_counter, agents_to_recompute_ind=[agent1])
        self.node_counter += 1
        edge_constraints2 = deepcopy(node.edge_constraints)
        edge_constraints2[agent2].append((edge, time))

        new_node_2 = self.node_type(vertex_constraints, edge_constraints2, self.grid_map,
                                    self.agents, node, self.node_counter, agents_to_recompute_ind=[agent2])
        self.node_counter += 1
        if new_node_1.cost < math.inf:
            self.OPEN.add_node(new_node_1)
        if new_node_2.cost < math.inf:
            self.OPEN.add_node(new_node_2)

    def find_best_solutions(self):
        while not self.OPEN.is_empty():
            best_node = self.OPEN.get_best_node()
            agent1_vert, agent2_vert, v, t_vert = self.find_vertex_conflict(best_node)
            if agent1_vert is not None:
                self.add_children_from_vertex_constraint(best_node, agent1_vert, agent2_vert, v, t_vert)
            else:
                agent1_edge, agent2_edge, e, t_edge = find_edge_conflict(best_node)
                if agent1_edge is not None:
                    self.add_children_from_edge_constraint(best_node, agent1_edge, agent2_edge, e, t_edge)
                else:
                    return best_node.solutions, best_node.cost, self.OPEN.cnt
        return None, None, None

    def find_vertex_conflict(self, node: CBSNode):
        constraints_vertices = {}  # map from (vertex, time) to path
        max_len = len(max(node.solutions, key=lambda x: len(x)))

        for t in range(max_len):
            for i, solution in enumerate(node.solutions):
                if len(solution) <= t:
                    v = solution[-1]
                else:
                    v = solution[t]
                if (v, t) in constraints_vertices.keys():
                    j = constraints_vertices[(v, t)]
                    return i, j, v, t

                constraints_vertices[(v, t)] = i

        return None, None, None, None

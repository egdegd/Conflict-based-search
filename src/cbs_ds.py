import math
from collections import defaultdict
from copy import deepcopy
from src.cbs import CBS, CBSNode
from src.a_star import A_star_DS, A_star


class CBS_DS_Node(CBSNode):
    def __init__(self, vertex_constraints, edge_constraints, landmarks, grid_map, agents, parent=None, k=0, agents_to_recompute_ind=None):
        self.landmarks = landmarks  # map from agents to must_have vertices
        super().__init__(vertex_constraints, edge_constraints, grid_map, agents, parent, k, agents_to_recompute_ind)

    def find_best_solutions(self, grid_map, agents_to_recompute_ind):
        for i in agents_to_recompute_ind:
            s, f = self.agents[i]
            path = [s]
            for (v1, t1), (v2, t2) in zip(self.landmarks[i], self.landmarks[i][1:]):
                found, path_segment = A_star_DS(grid_map, v1[0], v1[1], t1, v2[0], v2[1], t2,
                                                self.vertex_constraints[i], self.edge_constraints[i])
                if not found:
                    self.cost = math.inf
                    return
                path += path_segment[1:]
            v_last, t1 = self.landmarks[i][-1]

            found, path_segment = A_star(grid_map, v_last[0], v_last[1], f[0], f[1], self.vertex_constraints[i],
                                         self.edge_constraints[i], t_start=t1)
            if not found:
                self.cost = math.inf
                return
            path += path_segment[1:]
            self.solutions[i] = path


class CBS_DS(CBS):
    def make_root(self):
        landmarks = dict()
        for agent, (s, f) in enumerate(self.agents):
            landmarks[agent] = [(s, 0)]
        self.root = CBS_DS_Node(defaultdict(lambda: []), defaultdict(lambda: []), landmarks, self.grid_map, self.agents)
        self.OPEN.add_node(self.root)

    def add_children_from_vertex_constraint(self, node: CBS_DS_Node, agent1, agent2, vertex, time):
        edge_constraints = deepcopy(node.edge_constraints)
        vertex_constraints1 = deepcopy(node.vertex_constraints)
        landmarks1 = deepcopy(node.landmarks)
        vertex_constraints1[agent1].append((vertex, time))
        new_node_1 = CBS_DS_Node(vertex_constraints1, edge_constraints, landmarks1, self.grid_map,
                                 self.agents, node, self.node_counter, agents_to_recompute_ind=[agent1])
        self.node_counter += 1

        vertex_constraints2 = deepcopy(node.vertex_constraints)
        vertex_constraints2[agent2].append((vertex, time))
        landmarks2 = deepcopy(node.landmarks)
        landmarks2[agent1] = sorted(landmarks2[agent1] + [(vertex, time)], key=lambda l: l[1])
        new_node_2 = CBS_DS_Node(vertex_constraints2, edge_constraints, landmarks2, self.grid_map,
                                 self.agents, node, self.node_counter, agents_to_recompute_ind=[agent1, agent2])
        self.node_counter += 1
        if new_node_1.cost < math.inf:
            self.OPEN.add_node(new_node_1)
        if new_node_2.cost < math.inf:
            self.OPEN.add_node(new_node_2)

    def add_children_from_edge_constraint(self, node: CBS_DS_Node, agent1, agent2, edge, time):
        vertex_constraints = deepcopy(node.vertex_constraints)
        landmarks = deepcopy(node.landmarks)
        edge_constraints1 = deepcopy(node.edge_constraints)
        edge_constraints1[agent1].append((edge, time))
        new_node_1 = CBS_DS_Node(vertex_constraints, edge_constraints1, landmarks, self.grid_map,
                                 self.agents, node, self.node_counter, agents_to_recompute_ind=[agent1])
        self.node_counter += 1
        edge_constraints2 = deepcopy(node.edge_constraints)
        edge_constraints2[agent2].append((edge, time))

        new_node_2 = CBS_DS_Node(vertex_constraints, edge_constraints2, landmarks, self.grid_map,
                                 self.agents, node, self.node_counter, agents_to_recompute_ind=[agent2])
        self.node_counter += 1
        if new_node_1.cost < math.inf:
            self.OPEN.add_node(new_node_1)
        if new_node_2.cost < math.inf:
            self.OPEN.add_node(new_node_2)

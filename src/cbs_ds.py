import math
from copy import deepcopy
from src.cbs import CBS, CBSNode


class CBS_DS(CBS):
    def add_children_from_vertex_constraint(self, node: CBSNode, agent1, agent2, vertex, time):
        edge_constraints = deepcopy(node.edge_constraints)
        vertex_constraints1 = deepcopy(node.vertex_constraints)
        vertex_constraints1[agent1].append((vertex, time))
        new_node_1 = CBSNode(vertex_constraints1, edge_constraints, self.grid_map,
                             self.agents, node, self.node_counter)
        self.node_counter += 1

        vertex_constraints2 = deepcopy(node.vertex_constraints)
        vertex_constraints2[agent1] += [(v, time) for v in node.grid_map.all_vertices() if v != vertex]
        new_node_2 = CBSNode(vertex_constraints2, edge_constraints, self.grid_map,
                             self.agents, node, self.node_counter)
        self.node_counter += 1
        if new_node_1.cost < math.inf:
            self.OPEN.add_node(new_node_1)
        if new_node_2.cost < math.inf:
            self.OPEN.add_node(new_node_2)

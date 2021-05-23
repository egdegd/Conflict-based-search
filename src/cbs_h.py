from src.cbs import CBS, CBSNode
from src.edge_cover import heuristic_edge_cover_size
from src.mdd import mdd_build


class CBS_H_Node(CBSNode):
    def __init__(self, vertex_constraints, edge_constraints, grid_map, agents, parent=None, k=0, agents_to_recompute_ind=None):
        super().__init__(vertex_constraints, edge_constraints, grid_map, agents, parent, k, agents_to_recompute_ind=agents_to_recompute_ind)
        self.h = self.calc_h()

    def __lt__(self, other: 'CBS_H_Node'):
        return self.cost + self.h < other.cost + other.h

    def calc_h(self):
        return heuristic_edge_cover_size(self.get_cardinal_conflicts())

    def get_cardinal_conflicts(self):
        constraints_vertices = {}  # map from (vertex, time) to path
        max_len = len(max(self.solutions, key=lambda x: len(x)))

        conflicts = []
        for t in range(max_len):
            for i, solution in enumerate(self.solutions):
                if len(solution) <= t:
                    v = solution[-1]
                else:
                    v = solution[t]
                if (v, t) in constraints_vertices.keys():
                    j = constraints_vertices[(v, t)]
                    conflicts += [(i, j, v, t)]

                constraints_vertices[(v, t)] = i

        mdds = {}
        cardinal_conflicts = []
        for i, j, v, t in conflicts:
            if i not in mdds or len(mdds[i]) < t + 1:
                start = self.solutions[i][0]
                finish = self.solutions[i][-1]
                cost = max(len(self.solutions[i]) - 1, t)
                mdds[i] = mdd_build(self.grid_map, start[0], start[1], finish[0], finish[1], cost,
                                    self.vertex_constraints[i], self.edge_constraints[i])
            if j not in mdds or len(mdds[j]) < t + 1:
                start = self.solutions[j][0]
                finish = self.solutions[j][-1]
                cost = max(len(self.solutions[j]) - 1, t)
                mdds[j] = mdd_build(self.grid_map, start[0], start[1], finish[0], finish[1], cost,
                                    self.vertex_constraints[j], self.edge_constraints[j])
            if len(mdds[i][t]) == 1 and len(mdds[j][t]) == 1:
                cardinal_conflicts.append((i, j))

        return cardinal_conflicts


class CBS_H(CBS):
    def __init__(self, grid_map, agents, node_type=CBS_H_Node):
        super().__init__(grid_map, agents, node_type)

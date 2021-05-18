from src.cbs import CBS, CBSNode
from src.mdd import mdd_build


class CBS_PC(CBS):

    def find_vertex_conflict(self, node: CBSNode):
        constraints_vertices = {}  # map from (vertex, time) to path
        max_len = len(max(node.solutions, key=lambda x: len(x)))

        conflicts = []
        for t in range(max_len):
            for i, solution in enumerate(node.solutions):
                if len(solution) <= t:
                    v = solution[-1]
                else:
                    v = solution[t]
                if (v, t) in constraints_vertices.keys():
                    j = constraints_vertices[(v, t)]
                    conflicts += [(i, j, v, t)]

                constraints_vertices[(v, t)] = i

        mdds = {}
        semi_card = []
        non_card = []
        for i, j, v, t in conflicts:
            if i not in mdds:
                start = node.solutions[i][0]
                finish = node.solutions[i][-1]
                mdds[i] = mdd_build(self.grid_map, start[0], start[1], finish[0], finish[1], node.cost)
            if j not in mdds:
                start = node.solutions[j][0]
                finish = node.solutions[j][-1]
                mdds[j] = mdd_build(self.grid_map, start[0], start[1], finish[0], finish[1], node.cost)
            if len(mdds[i][t]) == 1 and len(mdds[j][t]) == 1:
                return i, j, v, t
            elif len(mdds[i][t]) == 1 or len(mdds[j][t]) == 1:
                semi_card.append((i, j, v, t))
            else:
                non_card.append((i, j, v, t))
        if len(semi_card) > 0:
            return semi_card[0]
        if len(non_card) > 0:
            return non_card[0]
        return None, None, None, None

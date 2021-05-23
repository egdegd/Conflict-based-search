def mdd_build(grid_map,
              i_start,
              j_start,
              i_goal,
              j_goal,
              cost,
              vertex_constraints,
              edge_constraints):
    h = {c: {} for c in range(cost + 1)}
    h[0][(i_start, j_start)] = set()
    for c in range(cost):
        for i, j in h[c].keys():
            for (i_, j_) in grid_map.get_neighbors(i, j):
                to, frm = (i_, j_), (i, j)
                if (to, c + 1) in vertex_constraints or \
                        ((to, frm), c) in edge_constraints or \
                        ((frm, to), c) in edge_constraints:
                    continue
                if to not in h[c + 1]:
                    h[c + 1][to] = {frm}
                else:
                    h[c + 1][to].add(frm)
    mdd = {cost: set([p for p in h[cost].keys() if p == (i_goal, j_goal)])}
    cur = cost
    while cur > 0:
        mdd[cur - 1] = set()
        for p in mdd[cur]:
            for par in h[cur][p]:
                mdd[cur - 1].add(par)
        cur -= 1
    return mdd

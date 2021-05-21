from collections import defaultdict
from typing import List, Tuple


def remove_incident_edges(v, neighbours, edges):
    for v_neighbour in neighbours[v].copy():
        neighbours[v].remove(v_neighbour)
        neighbours[v_neighbour].remove(v)
        if (v, v_neighbour) in edges:
            edges.remove((v, v_neighbour))
        elif (v_neighbour, v) in edges:
            edges.remove((v_neighbour, v))
        else:
            raise KeyError


def heuristic_edge_cover_size(conflicting_agents: List[Tuple[int, int]]):
    edges = set(conflicting_agents)
    neighbours = defaultdict(lambda: set())
    for (u, v) in edges:
        neighbours[u].add(v)
        neighbours[v].add(u)

    cover_size = 0
    while len(edges) > 0:
        u, v = edges.pop()
        neighbours[u].remove(v)
        neighbours[v].remove(u)
        remove_incident_edges(v, neighbours, edges)
        remove_incident_edges(u, neighbours, edges)
        cover_size += 1

    return cover_size


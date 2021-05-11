import math

from src.a_star import A_star
from src.cbs import CBS
from src.map import Map
from movingai import read_map_from_moving_ai_file, read_tasks_from_moving_ai_file
from os import path


def A_star_test(path):
    i_start = 1
    j_start = 1
    i_goal = 13
    j_goal = 28
    width, height, cell = read_map_from_moving_ai_file(path)
    task_map = Map()
    task_map.set_grid_cells(width, height, cell)
    print(A_star(task_map, i_start, j_start, i_goal, j_goal, []))
    print(A_star(task_map, i_start, j_start, i_goal, j_goal, [((2, 1), 1)]))
    print(A_star(task_map, i_start, j_start, i_goal, j_goal, [((1, 1), 0)]))


def CBS_test(task_map, agents):
    try:
        cbs = CBS(task_map, agents)
        sol, cost = cbs.find_best_solutions()
        if cost < math.inf:
            print("Path found! Cost: " + str(cost))
            print(sol)
        else:
            print("Path not found!")
    except Exception as e:
        print("Execution error")
        print(e)


# A_star_test('../data/maps/simple_map.map')
# CBS_test('../data/maps/simple_map.map', [((1, 1), (13, 28)), ((3, 1), (2, 3))])
# CBS_test('../data/maps/simple_map_2.map', [((0, 0), (0, 4)), ((2, 2), (0, 3))])
def big_test(scenario_path, min_agents, max_agents):
    agents, map_file = read_tasks_from_moving_ai_file(scenario_path)
    width, height, cell = read_map_from_moving_ai_file(path.join('..', 'data', 'maps', map_file))
    task_map = Map()
    task_map.set_grid_cells(width, height, cell)
    for agents_n in range(min_agents, max_agents + 1):
        CBS_test(task_map, agents[:agents_n])


big_test('../data/scen-even/mice.scen', 2, 2)

import math
import multiprocessing

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


def CBS_test(task_map, agents, status):
    try:
        cbs = CBS(task_map, agents)
        sol, cost = cbs.find_best_solutions()
        if cost < math.inf:
            status.append("Path found! Cost: " + str(cost))
            # print(sol)
        else:
            status.append("Path not found!")
    except Exception as e:
        print("Execution error")
        print(e)


def big_test(scenario_path, min_agents, max_agents, experiment_time=10):
    """
    Makes MAPF tasks from scenario_path consequently from
    first agents_n agents for agents_n in [min_agents, max_agents].
    If one fails to run in experiment_time seconds, breaks.
    """

    agents, map_file = read_tasks_from_moving_ai_file(scenario_path)
    width, height, cell = read_map_from_moving_ai_file(path.join('..', 'data', 'maps', map_file))
    task_map = Map()
    task_map.set_grid_cells(width, height, cell)

    manager = multiprocessing.Manager()

    for agents_n in range(min_agents, max_agents + 1):
        res = manager.list()
        p = multiprocessing.Process(target=CBS_test, args=(task_map, agents[:agents_n], res))
        p.start()
        p.join(experiment_time)
        if p.is_alive():
            p.terminate()

        if len(res) == 0:
            print('Not finished on', agents_n)
            break

        print(res[0])


# big_test('../data/scenarios/den520d/den520d-even-1.scen', 5, 10)
big_test('../data/scenarios/mice.scen', 2, 2)

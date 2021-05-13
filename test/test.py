import math
import multiprocessing

from src.a_star import A_star
from src.cbs import CBS
from src.map import Map
from movingai import read_map_from_moving_ai_file, read_tasks_from_moving_ai_file
from os import path
from random import sample
from src.visualization import draw


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
        draw(task_map, sol, agents)
        if cost < math.inf:
            status.append("Found!")
            # print(sol)
        else:
            status.append("Not found!")
    except Exception as e:
        print("Execution error")
        print(e)


def big_test(scenario_path, min_agents, max_agents, step=5, sample_times=20, experiment_time=60*5):
    agents, map_file = read_tasks_from_moving_ai_file(scenario_path)
    width, height, cell = read_map_from_moving_ai_file(path.join('..', 'data', 'maps', map_file))
    task_map = Map()
    task_map.set_grid_cells(width, height, cell)

    manager = multiprocessing.Manager()

    for agents_n in range(min_agents, max_agents + 1, step):
        successes = 0
        for _ in range(sample_times):
            cur_agents = sample(agents, k=agents_n)
            res = manager.list()
            p = multiprocessing.Process(target=CBS_test, args=(task_map, cur_agents, res))
            p.start()
            p.join(experiment_time)
            if p.is_alive():
                p.terminate()

            if len(res) == 1 and res[0] == 'Found!':
                successes += 1

        print(f'{successes} out of {sample_times} successes on {agents_n} agents')


# big_test('../data/scenarios/Berlin_1_256/Berlin_1_256-even-1.scen', 5, 75)
big_test('../data/scenarios/empty_8_8/empty-8-8-even-25.scen', 5, 5, 1, 1)
# big_test('../data/scenarios/mice.scen', 2, 2, 1, 1)

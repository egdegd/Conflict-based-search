import math
import multiprocessing
import time

from src.a_star import A_star
from src.cbs import CBS
from src.cbs_ds import CBS_DS
from src.cbs_h import CBS_H
from src.cbs_pc import CBS_PC
from src.map import Map
from movingai import read_map_from_moving_ai_file, read_tasks_from_moving_ai_file
from os import path
from random import sample, seed
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
    cbs = CBS(task_map, agents)
    sol, cost = cbs.find_best_solutions()
    print("Plain: cost =", str(cost))
    # draw(task_map, sol, agents)
    if cost < math.inf:
        status.append("Found!")
    else:
        status.append("Not found!")


def CBS_PC_test(task_map, agents, status):
    cbs_pc = CBS_PC(task_map, agents)
    sol, cost = cbs_pc.find_best_solutions()
    print("PC: cost =", str(cost))
    # draw(task_map, sol, agents)
    if cost < math.inf:
        status.append("Found!")
    else:
        status.append("Not found!")


def CBS_DS_test(task_map, agents, status):
    cbs_ds = CBS_DS(task_map, agents)
    sol, cost = cbs_ds.find_best_solutions()
    print("DS: cost =", str(cost))
    # draw(task_map, sol, agents)
    if cost < math.inf:
        status.append("Found!")
    else:
        status.append("Not found!")


def CBS_H_test(task_map, agents, status):
    cbs_h = CBS_H(task_map, agents)
    sol, cost = cbs_h.find_best_solutions()
    print("H: cost =", str(cost))
    # draw(task_map, sol, agents)
    if cost < math.inf:
        status.append("Found!")
    else:
        status.append("Not found!")


def big_test(scenario_path,
             min_agents,
             max_agents,
             step=5,
             sample_times=20,
             experiment_time=6000*5,
             target_function=CBS_test):

    seed(1337)
    agents, map_file = read_tasks_from_moving_ai_file(scenario_path)
    width, height, cell = read_map_from_moving_ai_file(path.join('..', 'data', 'maps', map_file))
    task_map = Map()
    task_map.set_grid_cells(width, height, cell)

    manager = multiprocessing.Manager()
    cur_time = time.time()
    for agents_n in range(min_agents, max_agents + 1, step):
        successes = 0
        for _ in range(sample_times):
            cur_agents = sample(agents, k=agents_n)
            res = manager.list()
            p = multiprocessing.Process(target=target_function, args=(task_map, cur_agents, res))
            p.start()
            p.join(experiment_time)
            if p.is_alive():
                p.terminate()

            if len(res) == 1 and res[0] == 'Found!':
                successes += 1

        print(f'{successes} out of {sample_times} successes on {agents_n} agents')

    print(f'Time spent: {time.time() - cur_time}')


# big_test('../data/scenarios/den520d/den520d-even-1.scen', 6, 6, sample_times=1)
# big_test('../data/scenarios/empty_8_8/empty-8-8-even-25.scen', 5, 5, 1, 1)
# big_test('../data/scenarios/towards.scen', 2, 2, 1, 1, target_function=CBS_PC_test)
# big_test('../data/scenarios/mice.scen', 2, 2, 1, 1, target_function=CBS_PC_test)
big_test('../data/scenarios/empty_8_8/empty-8-8-even-25.scen', 10, 10, 1, 1)
big_test('../data/scenarios/empty_8_8/empty-8-8-even-25.scen', 10, 10, 1, 1, target_function=CBS_PC_test)
big_test('../data/scenarios/empty_8_8/empty-8-8-even-25.scen', 10, 10, 1, 1, target_function=CBS_DS_test)
big_test('../data/scenarios/empty_8_8/empty-8-8-even-25.scen', 10, 10, 1, 1, target_function=CBS_H_test)
# big_test('../data/scenarios/den520d/den520d-even-1.scen', 6, 6, sample_times=1, target_function=CBS_PC_test)
# big_test('../data/scenarios/den520d/den520d-even-1.scen', 6, 6, sample_times=1, target_function=CBS_DS_test)
# big_test('../data/scenarios/den520d/den520d-even-1.scen', 6, 6, sample_times=1, target_function=CBS_H_test)

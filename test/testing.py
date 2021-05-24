import math
import multiprocessing
import os
import time

from src.a_star import A_star
from src.cbs import CBS
from src.cbs_ds import CBS_DS
from src.cbs_h import CBS_H
from src.cbs_pc import CBS_PC
from src.map import Map
from test.movingai import read_map_from_moving_ai_file, read_tasks_from_moving_ai_file
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


def CBS_test(task_map, agents, status, target_class=CBS):
    cbs = target_class(task_map, agents)
    sol, cost, nodes_cnt = cbs.find_best_solutions()
    print(f"{target_class.__name__}: cost = {str(cost)}, nodes = {str(nodes_cnt)}")
    # draw(task_map, sol, agents)
    if cost < math.inf:
        status.append(cost)
        status.append(nodes_cnt)
        status.append("Found!")
    else:
        status.append("Not found!")


def big_test(scenario_path,
             min_agents,
             max_agents,
             step=5,
             sample_times=20,
             experiment_time=6000*5,
             target_class=CBS):

    seed(1337)
    agents, map_file = read_tasks_from_moving_ai_file(scenario_path)
    width, height, cell = read_map_from_moving_ai_file(path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'maps', map_file))
    task_map = Map()
    task_map.set_grid_cells(width, height, cell)

    manager = multiprocessing.Manager()
    cur_time = time.time()
    successes_ratios = []
    nodes = []
    times = []
    for agents_n in range(min_agents, max_agents + 1, step):
        successes = 0
        nodes += [[]]
        times += [[]]
        for i in range(sample_times):
            start_time = time.time()
            print(f"Starting experiment number {i + 1} / {sample_times} on {agents_n} agents")
            cur_agents = sample(agents, k=agents_n)
            res = manager.list()
            p = multiprocessing.Process(target=CBS_test, args=(task_map, cur_agents, res, target_class))
            p.start()
            p.join(experiment_time)
            if p.is_alive():
                print("Time limit exceeded, finishing")
                p.terminate()

            if len(res) == 3 and res[2] == 'Found!':
                successes += 1
                nodes[-1] += [res[1]]
            times[-1] += [time.time() - start_time]
        successes_ratios += [successes / sample_times]
        print(f'{successes} out of {sample_times} successes on {agents_n} agents')
    spended_time = time.time() - cur_time
    print(f'Time spent: {spended_time}')
    return successes_ratios, spended_time, nodes, times



# big_test('../data/scenarios/den520d/den520d-even-1.scen', 6, 6, sample_times=1)
# big_test('../data/scenarios/empty_8_8/empty-8-8-even-25.scen', 5, 5, 1, 1)
# big_test('../data/scenarios/towards.scen', 2, 2, 1, 1, target_function=CBS_PC_test)
# big_test('../data/scenarios/mice.scen', 2, 2, 1, 1, target_function=CBS_PC_test)
# big_test('../data/scenarios/empty_8_8/empty-8-8-even-25.scen', 10, 10, 1, 1)
# big_test('../data/scenarios/empty_8_8/empty-8-8-even-25.scen', 10, 10, 1, 1, target_class=CBS_PC)
# big_test('../data/scenarios/empty_8_8/empty-8-8-even-25.scen', 10, 10, 1, 1, target_class=CBS_DS)
# big_test('../data/scenarios/empty_8_8/empty-8-8-even-25.scen', 10, 10, 1, 1, target_class=CBS_H)
# big_test('../data/scenarios/den520d/den520d-even-1.scen', 6, 6, sample_times=1, target_class=CBS_PC)
# big_test('../data/scenarios/den520d/den520d-even-1.scen', 6, 6, sample_times=1, target_class=CBS_DS)
# big_test('../data/scenarios/den520d/den520d-even-1.scen', 6, 6, step=1, sample_times=1, target_class=CBS_H, experiment_time=300)
big_test('../data/scenarios/ost003d/ost003d-even-25.scen', 5, 10, step=1, sample_times=2, target_class=CBS_H, experiment_time=300)
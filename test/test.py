import math

from src.a_star import A_star
from src.cbs import CBS
from src.map import Map
from movingai import read_map_from_moving_ai_file


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


def CBS_test(path, agents):
    width, height, cell = read_map_from_moving_ai_file(path)
    task_map = Map()
    task_map.set_grid_cells(width, height, cell)

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


A_star_test('../data/maps/simple_map.map')
CBS_test('../data/maps/simple_map.map', [((1, 1), (13, 28)), ((3, 1), (2, 3))])
CBS_test('../data/maps/simple_map_2.map', [((0, 0), (0, 4)), ((2, 2), (0, 3))]) # чуть - чуть не работает, я вечером поправлю


from src.a_star import A_star
from src.cbs import CBS
from src.map import Map

height = 15
width = 30
mapstr = '''
. . . . . . . . . . . . . . . . . . . . . # # . . . . . . .  
. . . . . . . . . . . . . . . . . . . . . # # . . . . . . . 
. . . . . . . . . . . . . . . . . . . . . # # . . . . . . . 
. . . # # . . . . . . . . . . . . . . . . # # . . . . . . . 
. . . # # . . . . . . . . # # . . . . . . # # . . . . . . . 
. . . # # . . . . . . . . # # . . . . . . # # # # # . . . . 
. . . # # . . . . . . . . # # . . . . . . # # # # # . . . . 
. . . # # . . . . . . . . # # . . . . . . . . . . . . . . . 
. . . # # . . . . . . . . # # . . . . . . . . . . . . . . . 
. . . # # . . . . . . . . # # . . . . . . . . . . . . . . . 
. . . # # . . . . . . . . # # . . . . . . . . . . . . . . . 
. . . # # . . . . . . . . # # . . . . . . . . . . . . . . . 
. . . . . . . . . . . . . # # . . . . . . . . . . . . . . . 
. . . . . . . . . . . . . # # . . . . . . . . . . . . . . .
. . . . . . . . . . . . . # # . . . . . . . . . . . . . . .
'''
i_start = 1
j_start = 1
i_goal = 13
j_goal = 28

task_map = Map()
task_map.read_from_string(mapstr, width, height)


def A_star_test():
    print(A_star(task_map, i_start, j_start, i_goal, j_goal, []))
    print(A_star(task_map, i_start, j_start, i_goal, j_goal, [((2, 1), 1)]))
    print(A_star(task_map, i_start, j_start, i_goal, j_goal, [((1, 1), 0)]))


def CBS_test():
    cbs = CBS(task_map, [((1, 1), (13, 28)), ((3, 1), (2, 3))])
    print(cbs.find_best_solutions())


print(A_star(task_map, 1, 1, 13, 28, [])[1])
print(A_star(task_map, 3, 1, 2, 3, [])[1])
cbs = CBS(task_map, [((1, 1), (13, 28)), ((3, 1), (2, 3))])
sol = cbs.find_best_solutions()
print(sol[0])
print(sol[1])

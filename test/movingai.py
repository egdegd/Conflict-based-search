import math


def read_map_from_moving_ai_file(path):
    tasks_file = open(path)
    count = 0
    _ = tasks_file.readline()
    height = int(tasks_file.readline()[7:])
    width = int(tasks_file.readline()[6:])
    _ = tasks_file.readline()
    cells = [[0 for _ in range(width)] for _ in range(height)]
    i = 0
    j = 0

    for line in tasks_file:
        j = 0
        for c in line:
            if c == '.':
                cells[i][j] = 0
            elif c == '@':
                cells[i][j] = 1
            elif c == 'T':
                cells[i][j] = 1
            else:
                continue

            j += 1

        if j != width:
            raise Exception("Size Error. Map width = ", j, ", but must be", width, "(map line: ", i, ")")

        i += 1
        if i == height:
            break

    return width, height, cells


def read_tasks_from_moving_ai_file(path):
    tasks = []
    tasks_file = open(path)
    tasks_file.readline()
    map_file = ''
    for line in tasks_file:
        task = line.split()
        if int(task[0]) > 50:
            continue
        tasks.append(((int(task[5]), int(task[4])), (int(task[7]), int(task[6]))))
        map_file = task[1]
    return tasks, map_file

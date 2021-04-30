class Map:

    # Default constructor
    def __init__(self):
        self.width = 0
        self.height = 0
        self.cells = []

    # Initialization of map by string.
    def read_from_string(self, cell_str, width, height):
        self.width = width
        self.height = height
        self.cells = [[0 for _ in range(width)] for _ in range(height)]
        cell_lines = cell_str.split("\n")
        i = 0
        j = 0
        for l in cell_lines:
            if len(l) != 0:
                j = 0
                for c in l:
                    if c == '.':
                        self.cells[i][j] = 0
                    elif c == '#':
                        self.cells[i][j] = 1
                    else:
                        continue
                    j += 1
                if j != width:
                    raise Exception("Size Error. Map width = ", j, ", but must be", width)

                i += 1

        if i != height:
            raise Exception("Size Error. Map height = ", i, ", but must be", height)

    # Initialization of map by list of cells.
    def set_grid_cells(self, width, height, grid_cells):
        self.width = width
        self.height = height
        self.cells = grid_cells

    # Checks cell is on grid.
    def in_bounds(self, i, j):
        return (0 <= j < self.width) and (0 <= i < self.height)

    # Checks cell is not obstacle.
    def traversable(self, i, j):
        return not self.cells[i][j]

    # Creates a list of neighbour cells as (i,j) tuples.
    def get_neighbors(self, i, j):  # todo: нужно ли сюда передавать t или это будем учитывать внитри алгоритма.
        neighbors = []
        delta = [[0, 1], [1, 0], [0, -1], [-1, 0]]

        for d in delta:
            if self.in_bounds(i + d[0], j + d[1]) and self.traversable(i + d[0], j + d[1]):
                neighbors.append((i + d[0], j + d[1]))
        return neighbors

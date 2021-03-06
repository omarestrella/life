import sys
from copy import deepcopy


class Grid(object):
    """
    Represents a grid of cells for the game of life

    If the value is 1, the cell is 'alive'.
    If the value is 0, the cell is 'dead'.
    """

    grid = []

    def __init__(self, rows=5, cols=5):
        self.rows = rows
        self.cols = cols

    def load_file(self, file_):
        """Opens a file and populates the grid"""

        with open(file_, 'r') as grid_file:
            # Read the line, convert the string to an integer, and add the line
            # to the grid array. Note that any extra rows/cols are not included
            # if you provide a number less than the actual size of the grid.
            for i in range(self.rows):
                line = grid_file.readline().split(' ')
                self.grid.append([int(num) for num in line][:self.cols])

    def step(self, times=1):
        """
        Run through a set amount of steps
        """
        for time in range(times):
            # Use a new grid to hold the changed rows. We do this so the new state
            # of the row does not affect the processing of the next row.
            new_grid = deepcopy(self.grid)

            for row, values in enumerate(self.grid):
                for col, cell in enumerate(values):
                    live = self.check_neighbors(row, col)

                    # Life logic contained in the following four rules
                    # else needed in shortand if-else statement :(
                    if cell == 1:
                        new_grid[row][col] = 0 if live < 2 or live > 3 else 1
                    else:
                        new_grid[row][col] = 1 if live == 3 else 0

            self.grid = new_grid
            self.pretty_print()

    def check_neighbors(self, row, col):
        """Returns the number of live neighbors for a given cell"""
        neighbors = [
            (row - 1, col - 1,), (row - 1, col,), (row - 1, col + 1,),
            (row, col - 1,), (row, col + 1,),  # Do not include the cell itself!
            (row + 1, col - 1,), (row + 1, col,), (row + 1, col + 1,),
        ]

        # Sum up the live cells using the value of the neighbors
        return sum([self.check_cell(*neighbor) for neighbor in neighbors])

    def check_cell(self, row, col):
        """
        Helper method for returning the cells value
        Counts the boundaries as dead cells, otherwise we will wrap around
        or get an IndexError
        """
        return self.grid[row][col] if 0 <= row < self.rows and 0 <= col < self.cols else 0

    def pretty_print(self):
        """Print out the grid of cells (lazily...)"""
        print '\n'
        for row in self.grid:
            print ' '.join([str(val) for val in row])


if __name__ == '__main__':
    file_name = sys.argv[1]

    rows = int(raw_input('How many rows? '))
    cols = int(raw_input('How many columns? '))
    steps = int(raw_input('How many steps? '))

    grid = Grid(rows, cols)
    grid.load_file(file_name)
    grid.pretty_print()
    grid.step(steps)

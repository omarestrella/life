import sys
import pprint
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
            grid_file = file(file_)

            # Read the line, convert the string to integers, and add the line
            # to the grid array. Note that any extra rows/cols are not included
            # if you provide a number less than the actual size of the grid.
            for i in range(self.rows):
                line = grid_file.readline().split(' ')
                self.grid.append([int(num) for num in line][:self.cols])


    def step(self, times=1):
        """
        Run through a set amount of steps

        Use a new grid to hold the changed rows. We do this so the new state
        of the row does not affect the processing of the next row.
        """
        new_grid = deepcopy(self.grid)
        for time in range(times):
            for row, values in enumerate(self.grid):
                for col, cell in enumerate(values):
                    live = self.check_neighbors(row, col)
                    if cell == 1:
                        if live < 2 or live > 3:
                            new_grid[row][col] = 0
                        if live == 2 or live == 3:
                            new_grid[row][col] = 1 # stay the same
                    else:
                        if live == 3:
                            new_grid[row][col] = 1
            self.grid = new_grid
            self.pretty_print()


    def check_neighbors(self, row, col):
        """Returns the number of live neighbors for a given cell"""
        neighbors = [
            (row-1, col-1,), (row-1, col,), (row-1, col+1,),
            (row, col-1,), (row, col+1,),
            (row+1, col-1,), (row+1, col,), (row+1, col+1,),
        ]
        # Sum up
        return sum([self.check_cell(*neighbor) for neighbor in neighbors])


    def check_cell(self, row, col):
        """
        Helper method for returning the cells value
        Counts the boundaries as dead cells, otherwise we will wrap around
        or get an IndexError
        """
        try:
            return self.grid[row][col] if 0 <= row < self.rows and 0 <= col < self.cols else 0
        except IndexError:
            return 0


    def pretty_print(self):
        print '\n'
        for row in self.grid:
            print ' '.join([str(val) for val in row])


    def __str__(self):
        return '\n%s' % pprint.PrettyPrinter().pformat(self.grid)


if __name__ == '__main__':
    file_name = sys.argv[1]
    rows = int(raw_input('How many rows? '))
    cols = int(raw_input('How many columns? '))

    grid = Grid(rows, cols)
    grid.load_file(file_name)
    grid.pretty_print()
    grid.step()

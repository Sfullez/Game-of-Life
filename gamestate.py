from PyQt5.QtCore import pyqtSignal, QObject


class Grid:
    """
    Class that represents the grid for the game, containing all the cells and methods needed to simulate the population
    """

    def __init__(self, rows, cols):
        """
        Constructor of the class that sets the attributes and initializes all the Cell objects
        :param rows: number of rows of the grid
        :param cols: number of columns of the grid
        """

        self._rows = rows
        self._cols = cols
        self._cells = []

        for row in range(0, rows):
            self._cells.append([])

            for col in range(0, cols):
                self._cells[row].append(Cell(0, 0))

    def get_cell(self, row, col):
        """
        Selects a cell from the grid
        :param row: row from which the cell must be selected
        :param col: column from which the cell must be selected
        :returns: a Cell object from the _cells list
        """

        return self._cells[row][col]

    def occupied_neighbors(self, row, col):
        """
        Counts the alive neighbors of a given cell in the grid, paying attention to the position of the cell in the grid
        :param row: row of the cell to count the neighbors of
        :param col: column of the cell to count the neighbors of
        :returns: an integer representing the number of alive neighbors
        """

        count = 0

        if row > 0:
            count += self._cells[row - 1][col].get_value()

            if col > 0:
                count += self._cells[row - 1][col - 1].get_value()

            if col < self._cols - 1:
                count += self._cells[row - 1][col + 1].get_value()

        if row < self._rows - 1:
            count += self._cells[row + 1][col].get_value()

            if col > 0:
                count += self._cells[row + 1][col - 1].get_value()

            if col < self._cols - 1:
                count += self._cells[row + 1][col + 1].get_value()

        if col > 0:
            count += self._cells[row][col - 1].get_value()

        if col < self._cols - 1:
            count += self._cells[row][col + 1].get_value()

        return count

    def update_grid(self):
        """
        Updates in parallel the grid given the set of rules of the Game of Life
        """
        list_of_changes = {'birth': [], 'survival': [], 'death': []}

        for row in range(0, self._rows):
            for col in range(0, self._cols):
                cell_neighbors = self.occupied_neighbors(row, col)

                if self._cells[row][col].get_value():
                    if cell_neighbors in [2, 3]:  # Surviving cells
                        list_of_changes['survival'].append([row, col])
                    else:  # Dying cells
                        list_of_changes['death'].append([row, col])
                elif not self._cells[row][col].get_value() and cell_neighbors == 3:  # Newborn cells
                    list_of_changes['birth'].append([row, col])

        for coords in list_of_changes['birth']:
            self._cells[coords[0]][coords[1]].toggle_value()

        for coords in list_of_changes['survival']:
            self._cells[coords[0]][coords[1]].increase_time()

        for coords in list_of_changes['death']:
            self._cells[coords[0]][coords[1]].toggle_value()
            self._cells[coords[0]][coords[1]].reset_time()


class Cell(QObject):
    """
    Class that represents the single cell of the grid, holding the state of every single cell
    """
    cell_changed = pyqtSignal(int, int)

    def __init__(self, value, time):
        """
        Constructor of the class that sets the attributes
        :param value:
        :param time:
        """
        super().__init__()
        self._value = value if value in [0, 1] else 0  # Checks for not-allowed values
        self._alive_time = time

    def observe(self, slot):
        self.cell_changed.connect(slot)

    def get_value(self):
        """
        Getter of the value of the cell (occupied or empty)
        :returns: the value of the cell (1 or 0)
        """
        return self._value

    def toggle_value(self):
        """
        Toggles the value of the cell: 1 if 0, 0 if 1
        """
        self._value = 1 if self._value == 0 else 0
        self.cell_changed.emit(self._value, self._alive_time)

    def get_alive_time(self):
        """
        Getter of the number of time ticks in which the cell has been occupied
        :return: the value of the occupied time
        """
        return self._alive_time

    def increase_time(self):
        self._alive_time += 1
        self.cell_changed.emit(self._value, self._alive_time)

    def reset_time(self):
        self._alive_time = 0

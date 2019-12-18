from time import sleep

from PyQt5.QtCore import pyqtSignal, QObject

from events import game_event, window_event


class Grid:
    """
    Class that represents the grid for the game, containing all the cells and methods needed to simulate the population
    """

    def __init__(self, rows, cols, initial_state):
        """
        Constructor of the class that sets the attributes and initializes all the Cell objects
        :param rows: number of rows of the grid
        :param cols: number of columns of the grid
        """

        self._rows = rows
        self._cols = cols
        self._cells = []
        self._sleep = 0.03

        for row in range(0, rows):
            self._cells.append([])

            for col in range(0, cols):
                self._cells[row].append(Cell())

        if initial_state is not None:
            pass  # TODO: make a method that loads a previous state

    def get_cell(self, row, col):
        """
        Selects a cell from the grid
        :param row: row from which the cell must be selected
        :param col: column from which the cell must be selected
        :returns: a Cell object from the _cells list
        """

        return self._cells[row][col]

    def get_dimensions(self):
        return self._rows, self._cols

    def reset(self):
        """
        Resets the whole grid to its initial empty state
        """

        for row in range(0, self._rows):
            for col in range(0, self._cols):
                cell = self._cells[row][col]

                if cell.get_value() == 1:  # Toggles only the occupied cells, avoiding unnecessary propagation
                    cell.toggle_value()

    def occupied_neighbors(self, row, col):
        """
        Counts the alive neighbors of a given cell in the grid, paying attention to the position of the cell in the grid
        :param row: row of the cell to count the neighbors of
        :param col: column of the cell to count the neighbors of
        :returns: an integer representing the number of alive neighbors
        """

        count = 0  # Keeps track of how many alive cells are in the neighborhood

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

        list_of_changes = {'birth': [], 'survival': [], 'death': []}  # Keep the changes, make them at the end

        for row in range(0, self._rows):
            for col in range(0, self._cols):
                cell_neighbors = self.occupied_neighbors(row, col)

                if self._cells[row][col].get_value():  # If a cell is alive...
                    if cell_neighbors in [2, 3]:  # ...check if it survives
                        list_of_changes['survival'].append([row, col])
                    else:  # ...check if it dies
                        list_of_changes['death'].append([row, col])
                elif not self._cells[row][col].get_value() and cell_neighbors == 3:  # Check for a cell "birth"
                    list_of_changes['birth'].append([row, col])

        for coords in list_of_changes['birth']:  # Set the newborn cells to 1
            self._cells[coords[0]][coords[1]].toggle_value()

        for coords in list_of_changes['survival']:  # Increase the alive time of a surviving cell
            self._cells[coords[0]][coords[1]].increase_time()

        for coords in list_of_changes['death']:  # Set the dying cells to 0 and reset their alive time
            self._cells[coords[0]][coords[1]].toggle_value()
            self._cells[coords[0]][coords[1]].reset_time()

    def get_sleep(self):
        """
        Getter of _sleep
        :returns: an integer representing the value of _sleep
        """

        return self._sleep

    def set_sleep(self, fps):
        """
        Method that sets the _sleep value to render the target number of frames per second
        """

        self._sleep = round(1/fps, 3)

    def state_loop(self):
        """
        Main game loop that performs updates at the target number of times per second
        """

        while window_event.is_set():  # Checks if the main window is present
            while game_event.is_set() and window_event.is_set():  # Checks if the game is not paused
                self.update_grid()
                sleep(self._sleep)
            sleep(0.1)


class Cell(QObject):
    """
    Class that represents the single cell of the grid, holding the state of every single cell
    cell_changed signals a change in the cell, being the update of its value or alive time
    """

    cell_changed = pyqtSignal(int, int)

    def __init__(self):
        """
        Constructor of the class that initializes the attributes
        """

        super().__init__()
        self._value = 0
        self._alive_time = 0

    def observe(self, slot):
        """
        Method used to implement the observable behaviour, connecting a slot to the cell_changed signal
        :param slot: slot to connect to the cell_pressed signal
        """

        self.cell_changed.connect(slot)

    def get_value(self):
        """
        Getter of the value of the cell (alive or dead)
        :returns: the value of the cell (1 or 0)
        """

        return self._value

    def toggle_value(self):
        """
        Toggles the value of the cell: 1 if 0, 0 if 1
        """

        self._value = 1 if self._value == 0 else 0
        if self._value == 0:
            self.reset_time()
        self.cell_changed.emit(self._value, self._alive_time)  # Signal the change of value

    def get_time(self):
        """
        Getter of the number of time ticks in which the cell has been occupied
        :return: the value of the occupied time
        """

        return self._alive_time

    def increase_time(self):
        """
        Increases the alive time by 1, used by the game logic to keep track of the alive time of each cell
        """

        self._alive_time += 1
        self.cell_changed.emit(self._value, self._alive_time)  # Signal the change of alive time

    def set_time(self, value):
        """
        Sets the alive time at a precise value, used by the game logic to load a previously saved state
        """
        self._alive_time = value  # No signal emitting since we call toggle_value after this

    def reset_time(self):
        """
        Resets the alive time of the cell, used when a cell dies
        """

        self._alive_time = 0  # No need to signal the change, since the view is updated by the value toggle

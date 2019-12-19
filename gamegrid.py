from PyQt5.QtWidgets import QGridLayout, QGraphicsGridLayout
from gamestate import Grid
from gamecell import GameCell


class GameViewGrid(QGraphicsGridLayout):
    def __init__(self, rows, cols, initial_state):
        super().__init__()
        self.setHorizontalSpacing(0)
        self.setVerticalSpacing(0)
        self._stategrid = Grid(rows, cols, initial_state)
        self._rows = rows
        self._cols = cols
        self._grid = []

        for row in range(0, rows):
            self._grid.append([])

            for col in range(0, cols):
                game_cell = GameCell(row, col)  # Creates a new "visual" cell
                state_cell = self._stategrid.get_cell(row, col)  # Gets the corresponding state cell
                state_cell.observe(game_cell.update_color)  # Connects the color update to a change in the model cell
                game_cell.observe(state_cell.toggle_value)  # Connects the model update to a click in the "visual" cell
                self._grid[row].append(game_cell)
                self.addItem(game_cell, row, col)

        if len(initial_state) > 0:
            for row in range(0, rows):
                for col in range(0, cols):
                    if initial_state[row][col][0] == 1:
                        self._stategrid.get_cell(row, col).set_time(initial_state[row][col][1])
                        self._stategrid.get_cell(row, col).toggle_value()

        self.update_grid()

    def reset(self):
        self._stategrid.reset()

    def update_grid(self):
        """
        Update of the game grid, invoked by the game loop at the desired rate, that changes the color of every cell
        """

        for row in range(0, self._rows):
            for col in range(0, self._cols):
                occupied = self._stategrid.get_cell(row, col).get_value()
                time = self._stategrid.get_cell(row, col).get_time()
                self._grid[row][col].update_color(occupied, time)

    def get_state_grid(self):
        return self._stategrid


class GameGrid(QGridLayout):
    """
    Class that visually represents the game grid using a QGridLayout
    """

    def __init__(self, rows, cols, initial_state):
        """
        Initializes the model and associates a newly created "visual" cell to each model cell
        :param rows: number of rows of the grid
        :param cols: number of columns of the grid
        :param initial_state: initial state of the grid, loaded from a file or a known pattern in the initial dropdown
        """

        super().__init__()
        self.setHorizontalSpacing(0)  # Sets no horizontal spacing between adjacent cells
        self.setVerticalSpacing(0)  # Sets no vertical spacing between adjacent cells
        self._stategrid = Grid(rows, cols)  # Initialization of the state of the grid
        self._rows = rows
        self._cols = cols
        self._grid = []  # List containing all the game cells that are in the grid

        for row in range(0, rows):
            self._grid.append([])

            for col in range(0, cols):
                game_cell = GameCell(row, col)  # Creates a new "visual" cell
                state_cell = self._stategrid.get_cell(row, col)  # Gets the corresponding state cell
                state_cell.observe(game_cell.update_color)  # Connects the color update to a change in the model cell
                game_cell.observe(state_cell.toggle_value)  # Connects the model update to a click in the "visual" cell
                self._grid[row].append(game_cell)  # Adds the "visual" cell to the list of cells of the grid
                self.addWidget(game_cell, row, col)

        if len(initial_state) > 0:  # If the initial state is not empty, it is loaded into the state grid
            for row in range(0, rows):
                for col in range(0, cols):
                    if initial_state[row][col][0] == 1:
                        self._stategrid.get_cell(row, col).set_time(initial_state[row][col][1])
                        self._stategrid.get_cell(row, col).toggle_value()  # Visual update of the cell in the grid

        self.update_grid()

    def heightForWidth(self, width):
        """
        Overridden method to maintain a square ratio of the grid. Currently not working.
        """

        return width

    def hasHeightForWidth(self):
        """
        Overridden method to maintain a square ratio of the grid. Currently not working.
        """

        return True

    def reset(self):
        """
        Method used to trigger the reset of the state of the grid
        """

        self._stategrid.reset()

    def update_grid(self):
        """
        Update of the game grid, invoked by the game loop at the desired rate, which changes the color of every cell
        """

        for row in range(0, self._rows):
            for col in range(0, self._cols):
                occupied = self._stategrid.get_cell(row, col).get_value()
                time = self._stategrid.get_cell(row, col).get_time()
                self._grid[row][col].update_color(occupied, time)

    def get_state_grid(self):
        """
        Getter of the state (grid) of the game, used to access the state methods
        :returns: a Grid object representing the state of the game
        """

        return self._stategrid

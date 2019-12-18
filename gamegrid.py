from PyQt5.QtWidgets import QGridLayout
from gamestate import Grid
from gamecell import GameCell


class GameGrid(QGridLayout):
    """
    Class that visually represents the game grid using a QGridLayout
    """

    def __init__(self, rows, cols, cell_size):
        """
        Initializes the model and associates a newly created "visual" cell to each model cell
        :param rows:
        :param cols:
        :param cell_size:
        """
        super().__init__()
        self.setSpacing(1)
        self._stategrid = Grid(rows, cols)
        self._rows = rows
        self._cols = cols
        self._grid = []

        for row in range(0, rows):
            self._grid.append([])

            for col in range(0, cols):
                game_cell = GameCell(row, col, cell_size)  # Creates a new "visual" cell
                state_cell = self._stategrid.get_cell(row, col)  # Gets the corresponding state cell
                state_cell.observe(game_cell.update_color)  # Connects the color update to a change in the model cell
                game_cell.observe(state_cell.toggle_value)  # Connects the model update to a click in the "visual" cell
                self._grid[row].append(game_cell)
                self.addWidget(game_cell, row, col)

    def update_grid(self):
        """
        Update of the game grid, invoked by the game loop at the desired rate, that changes the color of every cell
        """
        for row in range(0, self._rows):
            for col in range(0, self._rows):
                occupied = self._stategrid.get_cell(row, col).get_value()
                time = self._stategrid.get_cell(row, col).get_alive_time()
                self._grid[row][col].update_color(occupied, time)

    def resize_grid(self, cell_size):
        # TODO: use it and document it or remove it
        for row in range(0, self._rows):
            for col in range(0, self._cols):
                self._grid[row][col].change_size(cell_size)

    def get_state_grid(self):
        return self._stategrid

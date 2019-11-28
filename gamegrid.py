from time import sleep

from PyQt5.QtWidgets import QGridLayout
from gamestate import Grid
from gamecell import GameCell


class GameGrid(QGridLayout):
    def __init__(self, rows, cols, cell_size):
        super().__init__()
        self._stategrid = Grid(rows, cols)
        self._rows = rows
        self._cols = cols
        self._grid = []

        for row in range(0, rows):
            self._grid.append([])

            for col in range(0, cols):
                game_cell = GameCell(row, col, cell_size)
                state_cell = self._stategrid.get_cell(row, col)
                state_cell.observe(game_cell.update_color)
                game_cell.observe(state_cell.toggle_value)
                self._grid[row].append(game_cell)
                self.addWidget(game_cell, row, col)

    def update_grid(self):
        self._stategrid.update_grid()  # TODO: remove

        for row in range(0, self._rows):
            for col in range(0, self._rows):
                occupied = self._stategrid.get_cell(row, col).get_value()
                time = self._stategrid.get_cell(row, col).get_alive_time()
                self._grid[row][col].update_color(occupied, time)

    def resize_grid(self, cell_size):
        for row in range(0, self._rows):
            for col in range(0, self._cols):
                self._grid[row][col].change_size(cell_size)

    def update_cell(self, row, col):
        self._stategrid.get_cell(row, col).toggle_value()
        print(str(row) + " " + str(col) + " clicked! " + str(self._stategrid.get_cell(row, col).get_value()))

    def mainloop(self, event):
        sleep(15)

        while not event.is_set():
            self._stategrid.update_grid()
            sleep(0.01)

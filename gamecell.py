from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QFrame, QSizePolicy

from events import game_event


class GameCell(QFrame):
    """
    Class that visually represents a cell of the game grid
    cell_pressed signals the mouse click on a cell by the user manually drawing a pattern on the grid
    """

    cell_pressed = pyqtSignal()

    def __init__(self, row, col):
        """
        Initializes the cell, assigning it an id to change its style individually and setting its pixel size
        :param row: row of the grid in which the cell is placed
        :param col: column of the grid in which the cell is placed
        """

        super().__init__()
        self.setAutoFillBackground(True)  # Necessary for the cell recolor done later
        self._id = str(row) + str(col)  # Creates a unique id for the cell, used to change its color with a stylesheet
        self.setFrameStyle(QFrame.StyledPanel)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.update_color(0, 0)  # Initial recolor to set the cell as white

    def observe(self, slot):
        """
        Method used to implement the observable behaviour, connecting a slot to the cell_pressed signal
        :param slot: slot to connect to the cell_pressed signal
        """

        self.cell_pressed.connect(slot)

    def mousePressEvent(self, event):
        """
        Overrides the QWidget method dedicated to handling mouse clicks on the widget
        """

        if not game_event.is_set():  # Checks if the game is running or is paused...
            self.cell_pressed.emit()  # ...and is it not running, enables the cell pressing with the mouse click

    def get_id(self):
        """
        Getter of the id attribute
        :returns: id of the cell
        """

        return self._id

    def update_color(self, value, time):
        """
        Changes the color of the cell based on its value (alive or dead) and, if applicable, calls a dedicated method
        for recoloring
        :param value: indicates whether the cell is alive (1) or dead (0)
        :param time: time that the cell has been alive, used to obtain a different color based on the cell age
        """

        if value == 1:  # If the cell is alive, it is recolored based on its time...
            self.recolor(time)
        else:  # ...otherwise it is just white
            palette = QPalette()  # Create a palette
            palette.setColor(QPalette.Background, QColor(255, 255, 255))  # Set its color to white
            self.setPalette(palette)  # Change the cell palette

    def recolor(self, time):
        """
        Custom function to make each cell vary from blue to red based on its age, supports up to 1024 different color
        variations and can be adapted to work with less color variations (limited to 128 different colors to quickly see
        cells aging)
        :param time: alive time of the cell, used to generate the color
        """

        if time < 32:
            red = 0
            green = (time*8)
            blue = 255
        elif 32 <= time < 64:
            red = 0
            green = 255
            blue = 511 - (time*8)
        elif 64 <= time < 96:
            red = (time * 8) - 512
            green = 255
            blue = 0
        elif 96 <= time < 128:
            red = 255
            green = 1023 - (time * 8)
            blue = 0
        else:
            return

        palette = QPalette()  # Create a new palette
        palette.setColor(QPalette.Background, QColor(red, green, blue))  # Set its color to the one calculated
        self.setPalette(palette)  # Change the cell palette

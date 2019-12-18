from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QStyleOption, QStyle, QFrame, QSizePolicy
from PyQt5.QtWidgets import QGraphicsWidget

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
        self._id = str(row) + str(col)
        self.setFrameStyle(QFrame.StyledPanel)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setProperty('id', self._id)
        self.setObjectName(self._id)
        self.update_color(0, 0)

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
        if not game_event.is_set():  # Checks if the game is running or is paused
            self.cell_pressed.emit()

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
        if value == 1:
            self.recolor(time)
        else:
            self.setStyleSheet('QWidget#' + self.get_id() + ' { background-color: #ffffff}')

    def paintEvent(self, event):
        """
        Specific implementation of the method from QWidget, mandatory for subclasses of QWidget/QFrame when a change of
        stylesheet is needed at runtime. Code adapted from https://stackoverflow.com/q/18344135/8263997
        :return:
        """
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)
        super().paintEvent(event)

    def recolor(self, time):
        """
        Custom function to make each cell vary from blue to red based on its age, supports up to 1024 different color
        variations and can be adapted to work with less color variations
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

        color = '#' + format(red, '02x') + format(green, '02x') + format(blue, '02x')  # Converting to hex and string
        self.setStyleSheet('QWidget#' + self.get_id() + ' { background-color:' + color + ' }')

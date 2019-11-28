from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget, QStyleOption, QStyle


class GameCell(QWidget):
    cell_pressed = pyqtSignal()

    def __init__(self, row, col, cell_size):
        super().__init__()
        self._id = str(row) + str(col)
        self._row = row
        self._col = col
        self.setFixedSize(cell_size, cell_size)
        self.setProperty('id', self._id)
        self.setObjectName(self._id)
        self.update_color(0, 0)

    def observe(self, slot):
        self.cell_pressed.connect(slot)

    def mousePressEvent(self, event):
        self.cell_pressed.emit()

    def get_position(self):
        return self._row, self._col

    def get_id(self):
        return self._id

    def change_size(self, cell_size):
        self.setFixedSize(cell_size)

    def update_color(self, value, time):
        if value == 1:
            self.recolor(time)
        else:
            self.setStyleSheet('QWidget#' + self.get_id() + ' { background-color: white}')

        #self.style().unpolish(self)
        #self.style().polish(self)

    def paintEvent(self, event):
        """Reimplementation of paintEvent to allow for style sheets"""
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)
        super().paintEvent(event)

    def recolor(self, time):
        if time < 256:
            red = 0
            green = time
            blue = 255
        elif 256 <= time < 512:
            red = 0
            green = 255
            blue = 511 - time
        elif 512 <= time < 768:
            red = time - 512
            green = 255
            blue = 0
        elif 768 <= time < 1024:
            red = 255
            green = 1023 - time
            blue = 0
        else:
            return

        color = '#' + format(red, '02x') + format(green, '02x') + format(blue, '02x')
        self.setStyleSheet('QWidget#' + self.get_id() + ' { background-color:' + color + ' }')

import json

from PyQt5.QtCore import *
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QSpinBox, QLabel, QWidget, QSizePolicy, QHBoxLayout, QFileDialog, \
    QMessageBox
from datetime import datetime

from events import game_event


class GameMenu(QVBoxLayout):
    def __init__(self, game_grid, signal):
        super().__init__()
        self._clear = ClearButton(game_grid)
        self._save = SaveButton(game_grid.get_state_grid())
        self._start = StartButton(self._clear, self._save)
        self._settings = SettingsButton(signal)
        self._fps = FPSRegulator(game_grid.get_state_grid())
        self.addWidget(self._start)
        self.addWidget(self._clear)
        self.addWidget(self._save)
        self.addWidget(self._settings)
        self._fps_box = None
        self._fps_widget = None

        self.create_fps_widget()

    def get_start(self):
        return self._start

    def create_fps_widget(self):
        self._fps_box = QHBoxLayout()
        fps_label = QLabel("FPS")
        self._fps_box.addWidget(fps_label)
        self._fps_box.addWidget(self._fps)
        self._fps_widget = QWidget()
        self._fps_widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self._fps_widget.setLayout(self._fps_box)
        self.addWidget(self._fps_widget, Qt.AlignLeft)


class StartButton(QPushButton):
    def __init__(self, clear_button, save_button):
        super().__init__("Start")
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self._running = False
        self._clear = clear_button
        self._save = save_button

    def mousePressEvent(self, event):
        self._running = not self._running

        if self._running:
            self.setText("Pause")
            game_event.set()
            self._clear.setEnabled(False)
            self._save.setEnabled(False)
        else:
            self.setText("Start")
            game_event.clear()
            self._clear.setEnabled(True)
            self._save.setEnabled(True)


class ClearButton(QPushButton):
    def __init__(self, game_grid):
        super().__init__("Clear grid")
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self._grid = game_grid

    def mousePressEvent(self, event):
        self._grid.reset()


class SaveButton(QPushButton):
    def __init__(self, state_grid):
        super().__init__("Save state")
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self._grid = state_grid

    def mousePressEvent(self, event):
        self.save()

    def save(self):
        rows, cols = self._grid.get_dimensions()
        state = []

        for row in range(0, rows):
            state.append([])

            for col in range(0, cols):
                cell = self._grid.get_cell(row, col)
                state[row].append([cell.get_value(), cell.get_time()])

        filename, _ = QFileDialog.getSaveFileName(self, "Save state to JSON file", "", "JSON (*.json)")
        msg = QMessageBox()

        if filename:
            with open(filename + ".json", "w+") as save_file:
                save_file.write(str(state))

            msg.setIcon(QMessageBox.Information)
            msg.setText("State successfully saved on file")
            msg.setWindowTitle("Save success")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        else:
            pass


class SettingsButton(QPushButton):
    def __init__(self, signal):
        super().__init__("Settings")
        self._signal = signal
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

    def mousePressEvent(self, event):
        game_event.clear()
        self._signal.emit()


class FPSRegulator(QSpinBox):
    def __init__(self, state_grid):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setValue(30)
        self.setMaximum(300)
        self.valueChanged.connect(state_grid.set_sleep)

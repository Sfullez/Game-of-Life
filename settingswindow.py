import json
from functools import partial

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QWidget, QFormLayout, QLabel, QPushButton, QComboBox, QFrame, QFileDialog, \
    QMessageBox


class SettingsWindow(QMainWindow):
    change_window = pyqtSignal()

    def __init__(self, state):
        super().__init__()
        self._state = state
        self.setWindowTitle("Conway's Game of Life setup")
        self.main_widget = QWidget()
        self.main_layout = SettingsLayout(self.change_window)
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

    def get_state(self):
        return self._state

    def set_state(self, state):
        self._state = state

    def observe(self, slot):
        self.change_window.connect(slot)


class SettingsLayout(QFormLayout):

    def __init__(self, signal):
        super().__init__()

        with open('patterns.json') as patterns_file:
            self.patterns = json.load(patterns_file)

        self.signal = signal

        self.patterns_combo = QComboBox()
        self.patterns_combo.addItem("None")
        self.patterns_combo.addItems(self.patterns.keys())
        self.addRow(QLabel("Pattern"), self.patterns_combo)
        # TODO: add a signal that modifies state as soon as a pattern has been selected from the QComboBox

        self.load_pattern = QPushButton("Load pattern from file")
        self.load_pattern.clicked.connect(self.load_file)
        self.addRow(self.load_pattern)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        self.addRow(line)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_pressed)
        self.addRow(self.save_button)

    def load_file(self):
        state_file = QFileDialog.getOpenFileName(None, 'Open file', filter='JSON files (*.JSON)')

        msg = QMessageBox()

        try:
            with open(state_file[0], 'r+') as file:
                file_content = json.load(file)
                # TODO: check for file content correctness?
                self.get_settings_window().set_state(file_content)
                self.file_loaded()
        except FileNotFoundError:
            msg.setIcon(QMessageBox.Warning)
            msg.setText("No state file was provided")
            msg.setWindowTitle("File selection error")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

    def get_settings_window(self):
        return self.parent().parent()

    def file_loaded(self):
        self.signal.emit()

    def save_pressed(self):
        text = self.patterns_combo.currentText()
        if text != "None":
            self.get_settings_window().set_state(self.patterns[text])
        self.signal.emit()

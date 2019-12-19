import json

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QWidget, QFormLayout, QLabel, QPushButton, QComboBox, QFrame, QFileDialog, \
    QMessageBox


class SettingsWindow(QMainWindow):
    """
    Class that visually represents the game settings window that lets the user select a know pattern or load one from a
    previously saved game state
    change_window is a signal emitted when the user has clicked the save button or has submitted a state file
    """

    change_window = pyqtSignal()

    def __init__(self, state):
        """
        Constructor that initializes the basic window structure
        :param state: list containing the initial state of the grid, given from a file or from a pattern
        """

        super().__init__()
        self._state = state
        self.setWindowTitle("Conway's Game of Life Remastered setup")
        self.main_widget = QWidget()
        self.main_layout = SettingsLayout(self.change_window)
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

    def get_state(self):
        """
        Getter method to access the state loaded from the patterns file or from a user-submitted previous state file
        :returns: the state loaded from the settings window
        """

        return self._state

    def set_state(self, state):
        """
        Setter method of the state, used to load a selected state into the state grid
        """

        self._state = state

    def observe(self, slot):
        """
        Method used to implement the observable behaviour, connecting a slot to the change_window signal
        :param slot: slot to connect to the change_window signal
        """

        self.change_window.connect(slot)


class SettingsLayout(QFormLayout):
    """
    Class representing the layout of the settings window, a form layout containing the dropdown menu for known patterns,
    a button which opens a window to load a saved file and a button to save the dropdown menu selection
    """

    def __init__(self, signal):
        """
        Constructor method that creates all the elements of the layout mentioned before
        :param signal: signal used to trigger the opening of the game window once the save button is pressed
        """

        super().__init__()

        with open('patterns.json') as patterns_file:
            self.patterns = json.load(patterns_file)  # Loads the know patterns listed in the dedicated file

        self.signal = signal

        self.patterns_combo = QComboBox()
        self.patterns_combo.addItem("None")
        self.patterns_combo.addItems(self.patterns.keys())
        self.addRow(QLabel("Pattern"), self.patterns_combo)

        self.load_pattern = QPushButton("Load pattern from file")
        self.load_pattern.clicked.connect(self.load_file)
        self.addRow(self.load_pattern)

        line = QFrame()  # Separator line between the load options and the save button
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        self.addRow(line)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_pressed)
        self.addRow(self.save_button)

    def load_file(self):
        """
        Method invoked when the "load from file" button is pressed, which asks the user to select a file using the
        default file explorer of the OS and then loads its contents into the state of the grid
        """

        state_file = QFileDialog.getOpenFileName(None, 'Open file', filter='JSON files (*.JSON)')  # Files are filtered

        msg = QMessageBox()

        try:  # state_file could be None (the user closes the window or presses the Cancel button)
            with open(state_file[0], 'r+') as file:
                file_content = json.load(file)
                # TODO: check for file content correctness?
                self.get_settings_window().set_state(file_content)
                self.signal.emit()  # Feedback of a correct file load is given to the user by switching window
                # to the window containing the grid
        except FileNotFoundError:
            msg.setIcon(QMessageBox.Warning)
            msg.setText("No state file was provided")
            msg.setWindowTitle("File selection error")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()  # A warning is print to users to let them know that no file was provided

    def get_settings_window(self):
        """
        Getter method used to retrieve a reference to the settings window
        :returns: a reference to the settings window in which the form layout is contained
        """

        return self.parent().parent()

    def save_pressed(self):
        """
        Method triggered when the user presses the save button, which checks what pattern (if any) is selected from the
        dropdown menu and, if selected, sets the state to the one represented by the pattern and then signals the change
        of window
        """

        text = self.patterns_combo.currentText()
        if text != "None":
            self.get_settings_window().set_state(self.patterns[text])
        self.signal.emit()

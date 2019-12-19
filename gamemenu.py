from PyQt5.QtCore import *
from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QSpinBox, QLabel, QWidget, QSizePolicy, QHBoxLayout, \
    QFileDialog, QMessageBox

from events import game_event


class GameMenu(QVBoxLayout):
    """
    Layout that represents the menu placed on the side of the game grid
    """

    def __init__(self, game_grid, signal):
        """
        Constructor used to instantiate all the buttons that compose the menu and the FPS setter
        :param game_grid: "visual" grid passed to enable reset, changes in FPS and save of the current state
        :param signal: signal used to trigger the window change when the settings button has been pressed
        """

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
        # TODO: check if it is used
        return self._start

    def create_fps_widget(self):
        """
        Method that incapsulates the creation of the FPS widget not to overcomplicate the constructor
        """

        self._fps_box = QHBoxLayout()
        fps_label = QLabel("FPS")
        self._fps_box.addWidget(fps_label)
        self._fps_box.addWidget(self._fps)
        self._fps_widget = QWidget()
        self._fps_widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self._fps_widget.setLayout(self._fps_box)
        self.addWidget(self._fps_widget, Qt.AlignLeft)


class StartButton(QPushButton):
    """
    Class that represents the start button placed in the game menu, created to customize the mousePressEvent method
    """

    def __init__(self, clear_button, save_button):
        """
        Constructor that sets the size policy to fixed (non-expanding), sets the references to the clear and save
        button and initializes a flag to control if the game is running or not without having to access the game grid.
        :param clear_button: reference to the clear button of the menu, used to change its "clickability" based on the
        state of the game (running or paused/stopped)
        :param save_button: reference to the save button of the menu, used to change its "clickability" based on the
        state of the game (running or paused/stopped)
        """

        super().__init__("Start")
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self._running = False
        self._clear = clear_button
        self._save = save_button

    def mousePressEvent(self, event):
        """
        Override of the superclass method, used to stop or start the game loop based on the current state of
        the game
        """

        self._running = not self._running  # First of all, toggle the state of the game...

        if self._running:  # If it is running, change it into a pause button and disable the other two buttons
            self.setText("Pause")
            game_event.set()  # Tells the game loop to actually update the grid
            self._clear.setEnabled(False)
            self._save.setEnabled(False)
        else:  # Otherwise, change it into a start button and enable the other two buttons
            self.setText("Start")
            game_event.clear()  # Tells the game loop to remain in the "outer" loop and wait for the game to start again
            self._clear.setEnabled(True)
            self._save.setEnabled(True)


class ClearButton(QPushButton):
    """
    Class that represents the clear button placed in the game menu, created to customize the mousePressEvent method
    """

    def __init__(self, game_grid):
        """
        Constructor that sets the size policy to fixed (non-expanding) and sets the reference to the game grid.
        :param game_grid: reference to the game grid, used to reset it
        """

        super().__init__("Clear grid")
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self._grid = game_grid

    def mousePressEvent(self, event):
        """
        Override of the superclass method, used to "clear" the grid by resetting it, only if the game is paused
        """

        self._grid.reset()


class SaveButton(QPushButton):
    """
    Class that represents the clear button placed in the game menu, created to customize the mousePressEvent method
    """

    def __init__(self, state_grid):
        """
        Constructor that sets the size policy to fixed (non-expanding) and sets the reference to the state grid.
        :param state_grid: reference to the state of the game grid, used to access it and read the state to save it
        """

        super().__init__("Save state")
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self._grid = state_grid

    def mousePressEvent(self, event):
        """
        Override of the superclass method, used to read and save the state of the grid by iterating in all of its cells
        """

        rows, cols = self._grid.get_dimensions()
        state = []

        for row in range(0, rows):
            state.append([])

            for col in range(0, cols):
                cell = self._grid.get_cell(row, col)
                state[row].append([cell.get_value(), cell.get_time()])  # Saves the alive/dead state and its alive time

        # Create the window and filters the files the user is able to see in the directory
        filename, _ = QFileDialog.getSaveFileName(self, "Save state to JSON file", "", "JSON (*.json)")
        msg = QMessageBox()

        if filename:  # If the filename has been selected and the save button has been pressed...
            with open(filename + ".json", "w+") as save_file:  # Create the file with filename + .json
                save_file.write(str(state))  # Dump the state onto the file

            msg.setIcon(QMessageBox.Information)
            msg.setText("State successfully saved on file")
            msg.setWindowTitle("Save success")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()  # Show the user a confirmation message box
        else:  # ...otherwise (window has been closed or Cancel button pressed) no confirmation is shown to the user
            pass


class SettingsButton(QPushButton):
    """
    Class that represents the settings button placed in the game menu, created to customize the mousePressEvent method
    """

    def __init__(self, signal):
        """
        Constructor that sets the size policy to fixed (non-expanding) and sets the signal that will be emitted.
        :param signal: signal used to trigger the opening of the settings window when the button is pressed
        """

        super().__init__("Settings")
        self._signal = signal
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

    def mousePressEvent(self, event):
        """
        Override of the superclass method, used to stop the "inner" game loop (if running) and trigger the opening of
        the settings window 
        """

        game_event.clear()
        self._signal.emit()


class FPSRegulator(QSpinBox):
    """
    Class that represents the FPS regulator in the game menu, constructed as a spin box (input field with only integer
    values that can be increased with the keyboard or the arrows provided alongside the value), created to customize its
    behavior
    """

    def __init__(self, state_grid):
        """
        Constructor that sets the minimum and maximum values of the spinbox and connects the valueChanged signal to the
        method used to set the sleep of the grid update (which changes the number of frames per second in the visual
        update)
        :param state_grid: reference to the state of the grid, used to invoke its set_sleep method
        """
        super().__init__()
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setValue(30)
        self.setMinimum(1)
        self.setMaximum(300)
        self.valueChanged.connect(state_grid.set_sleep)  # Sets the sleep value as soon as the value is changed

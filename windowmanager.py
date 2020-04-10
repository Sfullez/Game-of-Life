from events import window_event
from mainwindow import MainWindow
from settingswindow import SettingsWindow


class WindowManager:
    """
    Class that represents a controller of the two different main views of the game: the game main window and the game
    settings window. This class handles when to open each window by coordinating the signals emitted from both windows
    """

    def __init__(self):
        """
        Constructor of the class which initializes the state shared between the settings window and the main window and
        creates a game settings window to be initially shown to the user
        """

        self._state = []
        self._settings_window = SettingsWindow(self._state)
        self._settings_window.observe(self.open_main)  # We set the slot so that a press of the save button in the
        # settings window triggers the opening of the main window
        self._main_window = None

    def open_settings(self):
        """
        Method used to trigger the opening of the settings window when the Settings button is pressed in the game main
        window
        """

        if self._main_window is not None:  # The main window is not created the first time the game is started...
            if self._main_window.isVisible():
                self._main_window.close()  # Closes the main window if it has already been created and it is visible

        window_event.clear()  # Event that signals to the game loop (which is still not stopped or destroyed!) to pause
        # the update of the grid
        self._settings_window.show()  # Finally, the settings window is shown

    def open_main(self):
        """
        Method used to trigger the opening of the main game window when the Save button is pressed in the game settings
        window or when a state file is loaded
        """

        if self._settings_window.isVisible():
            self._settings_window.close()  # If the settings window is visible, close it

        self._main_window = MainWindow(self._settings_window.get_state())
        self._settings_window.set_state([])  # Clears the state before opening the window a second time (so that
        # clicking save without selecting anything, to get an empty state grid, will not load the state selected in the
        # previous iteration)
        self._main_window.observe(self.open_settings)  # Sets the slot so that a press of the settings button in the
        # game main window triggers the opening of the settings window
        window_event.set()  # The window event is set...
        self._main_window.start_loop()  # ...so the game main loop can start and wait for the user to start the game
        self._main_window.show()

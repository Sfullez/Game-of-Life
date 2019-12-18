import sys

from PyQt5.QtWidgets import QApplication

from events import window_event
from mainwindow import MainWindow
from settingswindow import SettingsWindow


class WindowManager:
    def __init__(self):
        self._state = []
        self._settings_window = SettingsWindow(self._state)
        self._settings_window.observe(self.open_main)
        self._main_window = None

    def open_settings(self):
        if self._main_window is not None:
            if self._main_window.isVisible():
                self._main_window.close()

        window_event.clear()
        self._settings_window.show()

    def open_main(self):
        if self._settings_window.isVisible():
            self._settings_window.close()

        self._main_window = MainWindow(self._settings_window.get_state())
        self._settings_window.set_state([])  # Clears the loaded state in the settings window
        self._main_window.observe(self.open_settings)
        window_event.set()
        self._main_window.start_loop()
        self._main_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wm = WindowManager()
    wm.open_settings()
    app.exec_()
    window_event.clear()

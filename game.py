import sys

from PyQt5.QtWidgets import QApplication

from events import window_event
from windowmanager import WindowManager

if __name__ == '__main__':
    app = QApplication(sys.argv)
    wm = WindowManager()
    wm.open_settings()
    app.exec_()
    window_event.clear()

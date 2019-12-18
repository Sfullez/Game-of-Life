from PyQt5.QtWidgets import QVBoxLayout, QPushButton

from events import game_event


class GameMenu(QVBoxLayout):
    def __init__(self, game_grid):
        super().__init__()
        self._start = StartButton()
        self._clear = ClearButton(self._start, game_grid)
        self.addWidget(self._start)
        self.addWidget(self._clear)

    def get_start(self):
        return self._start


class StartButton(QPushButton):
    def __init__(self):
        super().__init__("Start")
        self._running = False

    def mousePressEvent(self, event):
        self._running = not self._running

        if self._running:
            self.setText("Pause")
            game_event.set()
        else:
            self.setText("Start")
            game_event.clear()


class ClearButton(QPushButton):
    def __init__(self, start_button, game_grid):
        super().__init__("Clear grid")
        self._start = start_button
        self._grid = game_grid

    def mousePressEvent(self, event):
        self._start.setText("Start")
        self._start._running = False
        game_event.clear()
        self._grid.get_state_grid().reset()

import sys
import threading
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QHBoxLayout

from events import window_event
from gamegrid import GameGrid
from gamemenu import GameMenu


class MainPanel(QHBoxLayout):
    def __init__(self):
        super().__init__()
        game_grid = GameGrid(5, 5, 50)
        grid_widget = QWidget()
        grid_widget.setLayout(game_grid)
        game_menu = GameMenu(game_grid)
        menu_widget = QWidget()
        menu_widget.setLayout(game_menu)
        self.addWidget(grid_widget)
        self.addWidget(menu_widget)
        mainloop = threading.Thread(target=game_grid.get_state_grid().state_loop)
        mainloop.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window_event.set()
    root = QMainWindow()
    main_widget = QWidget()
    main_widget.setLayout(MainPanel())
    root.setCentralWidget(main_widget)
    root.show()
    app.exec_()
    window_event.clear()

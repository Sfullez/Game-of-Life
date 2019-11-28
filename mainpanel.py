import sys
import threading
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication

from gamegrid import GameGrid

if __name__ == '__main__':
    app = QApplication(sys.argv)
    root = QMainWindow()
    main_widget = QWidget()
    game_grid = GameGrid(5, 5, 50)
    main_widget.setLayout(game_grid)
    root.setCentralWidget(main_widget)
    root.show()
    event = threading.Event()
    mainloop = threading.Thread(target=game_grid.mainloop, args=(event,))
    mainloop.start()
    app.exec_()
    event.set()

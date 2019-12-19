import threading

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QHBoxLayout, QMainWindow, QSizePolicy, QWidget, QGraphicsWidget

from gamegrid import GameGrid, GameViewGrid
from gamemenu import GameMenu


class MainWindow(QMainWindow):
    """
    Class that visually represents the main game window, containing the grid and the lateral menu
    change_window is a signal emitted when the user wants to go to the settings window
    """

    change_window = pyqtSignal()

    def __init__(self, state):
        """
        Constructor that initializes the basic window options, sets its layout to a MainPanel and its minimum dimensions
        :param state: list containing the initial state of the grid, given from a file or from a pattern
        """

        super().__init__()
        self.setWindowTitle("Conway's Game of Life Remastered")  # The industry of gaming right now
        self.main_widget = QWidget()
        self.main_panel = MainPanel(state, self.change_window)
        self.main_widget.setLayout(self.main_panel)
        self.setCentralWidget(self.main_widget)
        self.show()
        self.setMinimumWidth(self.main_widget.width())
        self.setMinimumHeight(self.main_widget.height())

    def observe(self, slot):
        """
        Method used to implement the observable behaviour, connecting a slot to the change_window signal
        :param slot: slot to connect to the change_window signal
        """

        self.change_window.connect(slot)

    def start_loop(self):
        """
        Method used to expose the start loop method of the main panel to external parts of code
        """

        self.main_panel.start_loop()


class MainPanel(QHBoxLayout):
    """
    Class representing the layout of the main window, an horizontal layout containing the main grid of the game and the
    menu with buttons used to "control" the game. It contains a widget for both parts of the main view.
    """

    def __init__(self, state, signal):
        """
        Constructor of the class, which instantiates a grid and a menu and sets their proportions
        :param state: list containing an initial state of the grid, given from a file or from a pattern
        :param signal: signal used to trigger the opening of the settings window once the button is pressed
        """

        super().__init__()

        self.grid_widget = GridWidget()
        self.game_grid = GameGrid(50, 50, state)  # Static dimension of the grid
        self.grid_widget.setLayout(self.game_grid)
        self.game_menu = GameMenu(self.game_grid, signal)
        self.menu_widget = QWidget()
        self.menu_widget.setLayout(self.game_menu)
        self.menu_widget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.addWidget(self.grid_widget, 60)
        # TODO: add spacer?
        self.addWidget(self.menu_widget, 40)

    def start_loop(self):
        """
        Method used to start the simulation loop, contained in the state grid inside the "visual" grid
        """

        mainloop = threading.Thread(target=self.game_grid.get_state_grid().state_loop)
        mainloop.start()


class MainPanel2(QHBoxLayout):
    def __init__(self, state, signal):
        super().__init__()
        self.grid_scene = QtWidgets.QGraphicsScene(self)
        self.grid_view = QtWidgets.QGraphicsView(self.grid_scene)
        self.grid_widget = GridViewWidget()
        self.game_grid = GameViewGrid(50, 50, state)
        self.grid_widget.setLayout(self.game_grid)
        self.game_menu = GameMenu(self.game_grid, signal)
        self.menu_widget = QWidget()
        self.menu_widget.setLayout(self.game_menu)
        self.menu_widget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.addWidget(self.grid_view, 60)
        self.addWidget(self.menu_widget, 40)

    def start_loop(self):
        mainloop = threading.Thread(target=self.game_grid.get_state_grid().state_loop)
        mainloop.start()


class GridWidget(QWidget):
    """
    Class that represents the widget containing the visual grid, set to be expanding in case of a window resize
    """

    def __init__(self):
        super().__init__()
        self.setMinimumWidth(512)
        self.setMinimumHeight(512)
        policy = QSizePolicy()
        policy.setHorizontalPolicy(QSizePolicy.Expanding)
        policy.setVerticalPolicy(QSizePolicy.Expanding)
        policy.setHeightForWidth(True)
        self.setSizePolicy(policy)

    def heightForWidth(self, width):
        """
        Overridden method to maintain a square widget. Currently not working.
        """

        if self.layout():
            return super().heightForWidth(width)

        width = self.height()
        return width

    # def resizeEvent(self, event):
    #     print("Resizing")
    #     if event.size().width() > event.size().height():
    #         super().resize(event.size().height(), event.size().height())
    #     else:
    #         super().resize(event.size().width(), event.size().width())
    #
    #     event.accept()


class GridViewWidget(QGraphicsWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumWidth(512)
        self.setMinimumHeight(512)
        policy = QSizePolicy()
        policy.setHorizontalPolicy(QSizePolicy.Expanding)
        policy.setVerticalPolicy(QSizePolicy.Expanding)
        policy.setHeightForWidth(True)
        self.setSizePolicy(policy)

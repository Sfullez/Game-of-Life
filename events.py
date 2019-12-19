import threading

game_event = threading.Event()  # Shared event to signal whether the game is paused or currently running
window_event = threading.Event()  # Shared event to signal if window is closed and the game loop must be terminated


from problem_random_vars import tow_to_dock,tow_to_port,free_tug_movement

class Tug:
    def __init__(self,id) -> None:
        self.busy = False
        self.inDock = False
        self.free_movement = free_tug_movement()
        self.tow_to_dock = tow_to_dock()
        self.tow_to_port = tow_to_port()
        self.id = id

    def is_free(self) -> bool:
        return not self.busy
    def in_dock(self) -> bool:
        return self.inDock
    def reset(self):
        self.busy = False
        self.inDock = False

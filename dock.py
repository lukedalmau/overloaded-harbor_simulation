from ship import Ship

class Dock:
    def __init__(self,id, ship:Ship = None, isBusy = False,hasShip = False) -> None:
        self.isBusy = isBusy
        self.hasShip = hasShip
        self.id = id
        self.ship = None
        self.end_loading = False 
    
    def is_free(self) -> bool:
        return not self.isBusy
    def reset(self):
        self.isBusy = False
        self.hasShip = False
        
        self.ship = None
        self.end_loading = False 

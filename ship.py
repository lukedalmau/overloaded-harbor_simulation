
class Ship:
    def __init__(self,typeOfShip ,arrival_time = 0):
        self.typeOfShip = typeOfShip
        self.arrival_time = arrival_time
        self.tow_to_dock_time = 0
        self.tow_to_port_time = 0
        self.start_loading_time = 0
        self.end_loading_time = 0
        self.departure_time = 0
        self.in_dock= False
        self.in_port = False

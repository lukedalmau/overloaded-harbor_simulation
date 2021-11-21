from random import seed
from typing import List
from events import Ship_Arrival_Event
from ship import Ship
from tug import Tug 
from dock import Dock
from problem_random_vars import ship_arrival, ship_type,Small_Load_Time, Medium_Load_Time, Large_Load_Time
from heap import Heap


class Port:
    def __init__(self,tugs: List[Tug],docks: List[Dock]) -> None:
        self.tugs = tugs
        self.docks = docks
        self.tugs_in_port = len(tugs)
        self.docks_in_port = len(docks)
        self.time = 0
        self.time_limit = 0
        self.ship_arrivals : List[Ship] = []
        self.finished_docks : List[Dock] = []
        self.history : List[Ship] = []
        
        self.ship_arrival = ship_arrival()
        self.ship_type = ship_type()
        self.small_load = Small_Load_Time()
        self.medium_load = Medium_Load_Time()
        self.large_load = Large_Load_Time()
        
        self.event_list = Heap([Ship_Arrival_Event(self.time +self.ship_arrival())])

    def run(self,h=24) -> None:
        self.reset()
        self.time_limit = h
        while not self.event_list.isEmpty():
            event = self.event_list.pop()
            self.time = event.time
            event.handle(self)
    
    def reset(self):
        self.time = 0
        self.time_limit = 0
        for tug in self.tugs:
            tug.reset()
        for dock in self.docks:
            dock.reset()
        self.ship_arrivals: List[Ship] = []
        self.finished_docks: List[Dock] = []
        self.history: List[Ship] = []
        self.event_list = Heap([Ship_Arrival_Event(self.time + self.ship_arrival())])


port = Port([Tug(0),Tug(1) ],[Dock(0),Dock(1),Dock(2), Dock(3)])

sims=[]

for _ in range(1000):
    
    port.run(7*24)
    sim_mean = sum([ship.tow_to_port_time-ship.start_loading_time for ship in port.history])/len(port.history)
    print(sim_mean)
    sims.append(sim_mean)
all_sim_mean =  sum(sims)/len(sims)
print("All simulations mean : ",all_sim_mean)
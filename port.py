
import matplotlib.pyplot as plt

from typing import List
from events import Ship_Arrival_Event
from ship import Ship
from tug import Tug 
from dock import Dock
from problem_random_vars import ship_arrival, ship_type,Small_Load_Time, Medium_Load_Time, Large_Load_Time
from heap import Heap


TUG_AMOUNT = 1
DOCK_AMOUNT = 3
TIME_LIMIT = 24


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


port = Port([Tug(i) for i in range(TUG_AMOUNT)], [Dock(i) for i in range(DOCK_AMOUNT)])


X = []
Y = []

ships_by_type = [[[],[]],[[],[]],[[],[]]]

sims=[]

for _ in range(1000):
    
    port.run(TIME_LIMIT)
    sim_mean = sum([ship.tow_to_port_time-ship.end_loading_time for ship in port.history])/len(port.history)
    #print(sim_mean)
    sims.append(sim_mean)
    X.extend([ship.departure_time for ship in port.history])
    Y.extend([ship.tow_to_port_time -
             ship.end_loading_time for ship in port.history])
    
    ships_type0_X = [ship.departure_time for ship in port.history if ship.typeOfShip == 0]
    ships_type1_X = [ship.departure_time for ship in port.history if ship.typeOfShip == 1]
    ships_type2_X = [ship.departure_time for ship in port.history if ship.typeOfShip == 2]
    
    ships_type0_Y = [ship.tow_to_port_time -
                     ship.end_loading_time for ship in port.history if ship.typeOfShip == 0]
    ships_type1_Y = [ship.tow_to_port_time -
                     ship.end_loading_time for ship in port.history if ship.typeOfShip == 1]
    ships_type2_Y = [ship.tow_to_port_time -
                     ship.end_loading_time for ship in port.history if ship.typeOfShip == 2]

    ships_by_type[0][0].extend(ships_type0_X)
    ships_by_type[0][1].extend(ships_type0_Y)

    ships_by_type[1][0].extend(ships_type1_X)
    ships_by_type[1][1].extend(ships_type1_Y)

    ships_by_type[2][0].extend(ships_type2_X)
    ships_by_type[2][1].extend(ships_type2_Y)


all_sim_mean =  sum(sims)/len(sims)
print("All simulations mean : ",all_sim_mean,"hours")
print("Min : ",min(sims),"Max : ", max(sims))

mean0X = sum(ships_by_type[0][0])/len(ships_by_type[0][0])
mean1X = sum(ships_by_type[1][0])/len(ships_by_type[1][0])
mean2X = sum(ships_by_type[2][0])/len(ships_by_type[2][0])

mean0Y = sum(ships_by_type[0][1])/len(ships_by_type[0][1])
mean1Y = sum(ships_by_type[1][1])/len(ships_by_type[1][1])
mean2Y = sum(ships_by_type[2][1])/len(ships_by_type[2][1])


plt.plot(X, Y, "b.", label="barcos")
plt.plot([mean2X for _ in range(len(sims))],sims,"m.",label="media de cada simulacion")
plt.plot([mean0X, mean1X, mean2X], [mean0Y, mean1Y, mean2Y], "ys",label="media por tipo de barco")
plt.plot(mean1X, all_sim_mean, "r.", label="media general")
plt.xlabel("tiempo de salida del puerto (horas)")
plt.ylabel("tiempo de espera (horas)" )
plt.legend()
plt.show()

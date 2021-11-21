from ship import Ship
from dock import Dock
from tug import Tug


class Event:
    def __init__(self,time) -> None:
        self.time = time

    def handle(self,environment) -> None:
        pass
    def __lt__(self,other):
        return self.time < other.time
    def __lg__(self,other):
        return self.time > other.time
    def __le__(self,other):
        return self.time <= other.time
    def __ge__(self,other):
        return self.time >= other.time
    def __gt__(self,other):
        return self.time > other.time
    def __eq__(self,other):
        return self.time == other.time
    def __ne__(self,other):
        return self.time != other.time
    
class Ship_Arrival_Event(Event):
    def __init__(self,time) -> None:
        super().__init__(time)
    
    def handle(self,port) -> None:
        shiptype = port.ship_type()

        if shiptype >= 0.5:
            shiptype = 2
        elif shiptype < 0.5 and shiptype >= 0.25:
            shiptype = 1
        else:
            shiptype = 0

        ship = Ship(typeOfShip = shiptype)
        ship.arrival_time = self.time
        ship.in_port = True

        for dock in port.docks:
            if dock.is_free():
                for tug in port.tugs:
                    if tug.is_free() :
                        tug.busy = True
                        dock.isBusy = True
                        if tug.in_dock():   
                            time = self.time + tug.free_movement()
                            port.event_list.push(Tow_To_Dock_Event(time,tug,dock,ship))
                            time = self.time + port.ship_arrival()
                            if port.time_limit >= time:
                                port.event_list.push(Ship_Arrival_Event(time))
                            tug.inDock = False
                            return None
                        else:
                            port.event_list.push(Tow_To_Dock_Event(self.time,tug,dock,ship))
                            time = self.time + port.ship_arrival()
                            if port.time_limit >= time:
                                port.event_list.push(Ship_Arrival_Event(time))
                            return None
        else:
            port.ship_arrivals.append(ship)
            time = self.time + port.ship_arrival()
            if port.time_limit >= time:
                port.event_list.push(Ship_Arrival_Event(time))

class Tow_To_Dock_Event(Event):
    def __init__(self,time,tug:Tug,dock:Dock,ship: Ship) -> None:
        super().__init__(time)
        self.tug = tug
        self.dock = dock
        self.ship = ship

    def handle(self,port) -> None:
        self.ship.tow_to_dock_time = self.time
        self.dock.hasShip = True
        self.dock.ship = self.ship
        self.dock.isBusy = True
        self.dock.end_loading = False
        self.tug.busy = False
        self.tug.inDock = True
        time = self.time + self.tug.tow_to_dock()
        port.event_list.push(Start_Loading_Ship_Event(time,self.dock,self.ship))
        port.event_list.push(Check_Finished_Ship_Event(time,self.tug))
        #port.event_list.push(ShipArrival(self.time + port.ship_arrival()))

class Start_Loading_Ship_Event(Event):
    def __init__(self,time,dock:Dock,ship: Ship) -> None:
        super().__init__(time)
        self.dock = dock
        self.ship = ship
    
    def handle(self,port) -> None:
        self.ship.start_loading_time = self.time

        if self.ship.typeOfShip == 0:
            time = self.time + port.small_load()
        elif self.ship.typeOfShip == 1:
            time = self.time + port.medium_load()
        else:
            time = self.time + port.large_load()

        port.event_list.push(End_Loading_Ship_Event(time,self.dock,self.ship))
        #port.event_list.push(ShipArrival(self.time + port.ship_arrival()))

class End_Loading_Ship_Event(Event):
    def __init__(self,time,dock:Dock,ship: Ship) -> None:
        super().__init__(time)
        self.dock = dock
        self.ship = ship
    
    def handle(self,port) -> None:
        self.dock.end_loading = True
        self.ship.end_loading_time = self.time
        for tug in port.tugs:
            if tug.is_free():
                tug.busy = True
                self.dock.isBusy = False
                self.dock.ship = None
                tug.inDock = False
                if tug.in_dock():
                    port.event_list.push(Tow_To_Port_Event(self.time,tug,self.ship))
                    #port.event_list.push(ShipArrival(self.time + port.ship_arrival()))
                    break
                else:
                    port.event_list.push(Tow_To_Port_Event(self.time + tug.free_movement(),tug,self.ship))
                    #port.event_list.push(ShipArrival(self.time + port.ship_arrival()))
                    break

                
        else:
            port.finished_docks.append(self.dock)

class Check_Finished_Ship_Event(Event):
    def __init__(self,time,tug:Tug) -> None:
        super().__init__(time) 
        self.tug = tug
        self.tug.busy = False
        self.tug.inDock = True
        
    
    def handle(self,port) -> None:
        if len(port.finished_docks)!=0:
            dock = port.finished_docks.pop(0)
            dock.hasShip = False
            ship= dock.ship
            dock.ship = None
            dock.isBusy = False
            self.tug.busy = True
            self.tug.inDock = False
            ship.tow_to_port_time = self.time
            self.time += self.tug.tow_to_port()
            port.event_list.push(Tow_To_Port_Event(self.time,self.tug,ship))
            #port.event_list.push(ShipArrival(self.time + port.ship_arrival()))

        elif len(port.ship_arrivals)!=0:
            for dock in port.docks:
                if dock.is_free():
                    dock.isBusy = True
                    self.tug.busy = True
                    self.tug.inDock = False
                    ship = port.ship_arrivals.pop(0)
                    time = self.time + self.tug.free_movement()
                    ship.tow_to_dock_time = time
                    port.event_list.push(Tow_To_Dock_Event(time,self.tug,dock,ship))
                    #port.event_list.push(ShipArrival(self.time + port.ship_arrival()))
                    break
            else:
                self.tug.busy = False
                self.tug.inDock = True
                
        else:
            if any([dock.hasShip for dock in port.docks]):
                self.tug.busy = False
                self.tug.inDock = True
            else:
                self.tug.busy = True
                self.tug.inDock = False
                port.event_list.push(Wait_Ship_Arrival_Event(self.time+self.tug.free_movement(),self.tug))

class Wait_Ship_Arrival_Event(Event):
    def __init__(self, time, tug: Tug) -> None:
        super().__init__(time)
        self.tug = tug

    def handle(self,port):
        self.tug.busy = False
        self.tug.inDock = False

class Tow_To_Port_Event(Event):
    def __init__(self,time,tug:Tug ,ship: Ship) -> None:
        super().__init__(time)
        self.tug = tug
        self.ship = ship
    
    def handle(self,port) -> None:
        
        self.ship.tow_to_port_time = self.time
        self.time+= self.tug.tow_to_port()
        self.ship.departure_time = self.time
        self.ship.in_port = False
        self.tug.busy = False
        self.tug.inDock = False
        port.history.append(self.ship)
        

        if len(port.ship_arrivals)!=0:
            for dock in port.docks:
                if dock.is_free():
                    ship = port.ship_arrivals.pop(0)
                    dock.hasShip = True
                    dock.ship = ship
                    dock.isBusy = True
                    dock.end_loading = False
                    self.tug.inDock = True
                    self.tug.busy = True
                   
                    port.event_list.push(Tow_To_Dock_Event(self.time,self.tug,dock,ship))
                    # port.event_list.push(ShipArrival(
                    #     self.time + port.ship_arrival()))
                    break
            else:
                events_removed = []
                while(len(port.event_list) != 0):
                    event = port.event_list.pop()
                    events_removed.append(event)
                    if isinstance(event, End_Loading_Ship_Event):
                        port.event_list.push(Check_Finished_Ship_Event(self.time, self.tug))
                        # port.event_list.push(ShipArrival(
                        #     self.time + port.ship_arrival()))
                        break
                    elif isinstance(event, Ship_Arrival_Event):
                        self.tug.busy = False
                        self.tug.inDock = False
                        # port.event_list.push(ShipArrival(
                        #     self.time + port.ship_arrival()))
                        break
                for event in events_removed:
                    port.event_list.push(event)

        else:
            events_removed = []
            while(len(port.event_list)!=0):
                event = port.event_list.pop()
                events_removed.append(event)
                if isinstance(event, End_Loading_Ship_Event):
                    self.tug.busy = False
                    self.tug.inDock = True
                    port.event_list.push(Check_Finished_Ship_Event(self.time + self.tug.free_movement(), self.tug))
                    # port.event_list.push(ShipArrival(
                    #     self.time + port.ship_arrival()))
                    break
                elif isinstance(event, Ship_Arrival_Event):
                    self.tug.busy = False
                    self.tug.inDock = False
                    break
            for event in events_removed:
                port.event_list.push(event)


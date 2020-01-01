import pandas as pd
import numpy as np
from IPython.display import display
import matplotlib.pyplot as plt
import math


###################################
###################################
###################################
###################################
###################################


class Passenger:
    def __init__(self, start, end, speed):
        self.x1, self.y1 = start
        self.x2, self.y2 = end
        self.speed = speed
    def walk_time(self):
        '''
        Calculates the time it would take a passenger to reach the final destination
        from their starting location.
        '''
        self.time = np.sqrt((self.x2-self.x1)**2
                           + (self.y2-self.y1)**2) * self.speed

        return self.time
    def display(self):
        print("start = ", self.x1 , self.y1)
        print("end = ", self.x2 , self.y2)
        print("speed = ", self.speed)
    
    def return_values(self):
        
        return((self.x1, self.y1), (self.x2, self.y2), self.speed)


###################################
###################################
###################################
###################################
###################################

class Route:
    def __init__(self, route):
        self.route = route
    
    
    def read_route(self):
        '''
         This reads the bus route csv file and returns a list containing touples 
         with the route of the bus and the name of the bus stops.    
        '''
        df = pd.read_csv(self.route, names=['x1','y1','stop'])
        df.fillna(0,inplace=True)
        # Make collapsed columns for positional dat
        df['x1, y1, stop'] = list(zip(df['x1'],df['y1'],df['stop']))
        # Make output list
        data_out = [(df.iloc[i]['x1, y1, stop']) for i in range(len(df))]
        
        return data_out    
    
    
    def plot_map(self): #filename):
        route = self.read_route()
        max_x = max([n[0] for n in route]) + 5 # adds padding
        max_y = max([n[1] for n in route]) + 5
        grid = np.zeros((max_y, max_x))
        for x,y,stop in route:
            grid[y, x] = 1
            if stop:
                grid[y, x] += 1
        fig, ax = plt.subplots(1, 1)
        ax.pcolor(grid)
        ax.invert_yaxis()
        ax.set_aspect('equal', 'datalim')
        plt.show()
        

    # stops is a dictionary holding the bus stop name and time of arrival. 
    # starting from 0 at stop A and taking 10 mins to reach checkpoints in  
    # the travel of bus
    def timetable(self):
        '''
        Generates a timetable for a route as minutes from its first stop.
        '''
        # stops is a dictionary holding the bus stop name and time of arrival. 
        # starting from 0 at stop A and taking 10 mins to reach checkpoints in  
        # the travel of bus.
        # can potentially change the speed
        route1 = self.read_route()
        time = 0
        stops = {}
        for step in route1:
            if step[2]:
                stops[step[2]] = time
            time += 10
            
        return stops
    
    def route_cc(self):
        '''
        Converts a set of route into a Freeman chain code
        3 2 1
        \ | /
        4 - C - 0
        / | \
        5 6 7
        '''
        #starting cord of bus route
        #Choosing bus stop A and giving (x,y) cord for it 
        route = self.read_route()
        start = route[0][:2]
        cc = []
        #dictionary containing Freeman chaid code
        freeman_cc2coord = {0: (1, 0),
                            1: (1, -1),
                            2: (0, -1),
                            3: (-1, -1),
                            4: (-1, 0),
                            5: (-1, 1),
                            6: (0, 1),
                            7: (1, 1)}
        #dict other way around relative to the one above
        freeman_coord2cc = {val: key for key,val in freeman_cc2coord.items()}
        for b, a in zip(route[1:], route):
            x_step = b[0] - a[0]
            y_step = b[1] - a[1]
            cc.append(str(freeman_coord2cc[(x_step, y_step)]))
       
        return start, ''.join(cc)




###################################
###################################
###################################
###################################
###################################




def read_passengers(file_name):    
    '''
    Reads the passengers csv file and returns a list containing touples with the 
    details of the starting and ending location, and speed for a passenger.
    '''
    df = pd.read_csv(file_name, names=['x1','y1','x2','y2','speed'])
    # Make collapsed columns for positional dat
    df['x1, y1'] = list(zip(df['x1'],df['y1']))
    df['x2, y2'] = list(zip(df['x2'],df['y2']))
    # Make output list
    data_out = [(df.iloc[i]['x1, y1'], df.iloc[i]['x2, y2']
                ,(df.iloc[i]['speed'])) for i in range(len(df))]
    
    return data_out

class Journey(Route, Passenger):
    def __init__(self, class_route, passengers):
        self.class_route = class_route
        self.passengers = passengers
        
    def passenger_trip(self, passenger):
        ''' 
        Returns the distance to the nearest bus stop to starting and ending location.
        '''
        start, end, pace = passenger
        stops = [value for value in self.class_route.read_route() 
                                                        if value[2]]
        # calculate closer stops
        # to start
        distances = [(math.sqrt((x - start[0])**2 +
                    (y - start[1])**2), stop) for x,y,stop in stops]
        closer_start = min(distances)
        # to end
        distances = [(math.sqrt((x - end[0])**2 +
                    (y - end[1])**2), stop) for x,y,stop in stops]
        closer_end = min(distances)
        
        return(closer_start, closer_end)

        
    def plot_bus_load(self): 
        '''
        Shows the amount of people on the bus during the bus journey.
        '''
        stops = {step[2]:0 for step in self.class_route.read_route()
                                                         if step[2]}

        for self.passenger_id, passenger in self.passengers.items():
            trip = self.passenger_trip(passenger.return_values())
            stops[trip[0][1]] += 1
            stops[trip[1][1]] -= 1
        for i, stop in enumerate(stops):
            if i > 0:
                stops[stop] += stops[prev]
            prev = stop
        fig, ax = plt.subplots()
        ax.step(range(len(stops)), list(stops.values()), where='post')
        ax.set_xticks(range(len(stops)))
        ax.set_xticklabels(list(stops.keys()))
        plt.show()

    def passenger_trip_time(self,passenger):
        '''
        Finds the duration of the journey for the passenger onn the bus and walking.
        '''        
        start, end, pace = passenger
        walk_distance_stops =  self.passenger_trip(passenger)#.return_values())
        bus_times = self.class_route.timetable()
        bus_travel = bus_times[walk_distance_stops[1][1]] - \
        bus_times[walk_distance_stops[0][1]]
        walk_travel = walk_distance_stops[0][0] * passenger[2] + \
        walk_distance_stops[1][0] * passenger[2]
        
        return(bus_travel, walk_travel) 
    
    def travel_time(self, passenger_id):
        '''This returns a dictioanry containing how long the passenger was on the bus and how long they walked for'''

        self.bus_travel_time_dict = {}
        for self.passenger_identification, passenger in self.passengers.items():
            self.bus_travel_time_dict[self.passenger_identification] = {'bus':self.passenger_trip_time(passenger.return_values())[0]
                                                                   ,'walk':self.passenger_trip_time(passenger.return_values())[1]}
        return self.bus_travel_time_dict[passenger_id]
    
    def print_time_stats(self):
        '''
        Prints the average time passengers spent on the bus and walking
        '''
        sum_bus_time = 0
        sum_walk_time = 0
        for i, passenger in enumerate(self.passengers.values()):
            sum_bus_time += self.passenger_trip_time(passenger.return_values())[0]
            sum_walk_time += self.passenger_trip_time(passenger.return_values())[1]
        average_bus_time = sum_bus_time/i 
        average_walk_time = sum_walk_time/i
        print((f"Average time on the bus: {average_bus_time:3.2f} minutes, \n"
              f"Average time walking: {average_walk_time:3.2f} minutes"))



if __name__ == "__main__":
    route = Route("route.csv")
    passengers = read_passengers("passenger.csv")
    # passenger = ((0, 1), (3, 9), 16)
    new_passenger_dict = {i: Passenger(start_end_speed[0],start_end_speed[1],start_end_speed[2])
                        for i, start_end_speed in enumerate(read_passengers("passenger.csv"))}

    journey = Journey(route,new_passenger_dict)
    journey.plot_bus_load()
    journey.print_time_stats()
    
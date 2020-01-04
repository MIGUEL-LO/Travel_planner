import pandas as pd
import numpy as np
from IPython.display import display
import matplotlib.pyplot as plt
import math
from string import ascii_uppercase

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
        '''
        Displays the input values for the passenger 
        '''
        print("start = ", self.x1 , self.y1)
        print("end = ", self.x2 , self.y2)
        print("speed = ", self.speed)
    
    def return_values(self):
        '''
        Returns the values input for the passenger
        '''
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
    def timetable(self,bus_speed=10):
        self.bus_speed = bus_speed
        
        '''
        Generates a timetable for a route as minutes from its first stop.
        With a user defined bus_speed otherwise default bus_speed = 10
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
            time += bus_speed
            
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
        # starting cord of bus route
        # Choosing bus stop A and giving (x,y) cord for it 
        route = self.read_route()
        start = route[0][:2]
        cc = []
        # dictionary containing Freeman chaid code
        freeman_cc2coord = {0: (1, 0),
                            1: (1, -1),
                            2: (0, -1),
                            3: (-1, -1),
                            4: (-1, 0),
                            5: (-1, 1),
                            6: (0, 1),
                            7: (1, 1)}
        # dict other way around relative to the one above
        freeman_coord2cc = {val: key for key,val in freeman_cc2coord.items()}
        for b, a in zip(route[1:], route):
            x_step = b[0] - a[0]
            y_step = b[1] - a[1]
            cc.append(int(freeman_coord2cc[(x_step, y_step)]))

        return cc
    
    
    def check_error(self):
        '''
        The bus is not allowed to move diagonally. This function checks wether the bus moves diagonally.
        To then use the result from this function to either allow the input passenger route or not.
        If the return value is > 0 then there is a diagonal movement, otherwise there isn't and the 
        route is valid.
        '''
        is_odd = 0
        for cc_number in self.route_cc():
            if cc_number % 2 != 0:
                is_odd += 1 
        
        if is_odd > 0:
            
            return 1
        else:
            
            return 0

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
        self.bus_travel_time_dict = {}
        
    def passenger_trip(self, passenger):
        ''' 
        Returns the distance to the nearest bus stop to starting and ending location.
        '''
        # Passed in a single passenger details from passangers containing the
        # starting location, ending location and pace of passenger.
        # pace = minutes per unit grid
        start, end, pace = passenger
        if self.class_route.check_error() > 0:
            raise ValueError('The route file input contains a diagonal movement')
        else:
            # Stops holds the cordinates for a bus stop in the bus route journey.
            # unpacked stops into x, y, stop. 
            stops = [value for value in self.class_route.read_route() 
                                                        if value[2]]
    
        # The distance to the closest bus stop for a passenger
        # from their start location.
        start_dist = [(math.sqrt((x - start[0])**2 +
                    (y - start[1])**2), stop) for x,y,stop in stops]
        closer_start = min(start_dist)
        # to end
        end_dist = [(math.sqrt((x - end[0])**2 +
                    (y - end[1])**2), stop) for x,y,stop in stops]
        closer_end = min(end_dist)
        
        return(closer_start, closer_end)

    
    def passenger_get_on_off_bus_stop_name(self, passenger):
        '''
        Returns the bus stop name that the passenger gets on and off.
        '''
        walk_distance_stops = self.passenger_trip(passenger)
        get_on_bus_stop = walk_distance_stops[0][1]
        get_off_bus_stop = walk_distance_stops[1][1]

        return(get_on_bus_stop, get_off_bus_stop)


    def passenger_walk_distance_to_from_bus_stop(self, passenger):
        '''
        The distance the passenger needs to walk to get on the bus and 
        the distance the passenger needs to walk to their final destination
        from the stop they got off.
        '''
        walk_distance_stops = self.passenger_trip(passenger)
        walk_distance_get_on_bus_stop = walk_distance_stops[0][0]
        walk_distance_get_off_bus_stop = walk_distance_stops[1][0]

        return(walk_distance_get_on_bus_stop, walk_distance_get_off_bus_stop)


    def passenger_journey_allowed(self,passenger):
        '''
        Checks wether the passenger journey travels in the same direction as the bus route
        to see if the passenger can use the bus.

        Making a dictionary of the alphabet with key = Letter and value = corresponding number .
        ie. The bus goes from A=1 to Z=26, if the passenger gets on at Z=26 and wants to go to A=1,
        it can not do this, as the bus only travels in one direction.
        Therefore the end location bus stop number must be greater than start location bus stop number
        The better option is to walk.
        '''

        number_lett_dict = dict(('{}'.format(letter), number) for number, letter in enumerate(ascii_uppercase, 1))

        bus_stop_name = self.passenger_get_on_off_bus_stop_name(passenger)
        get_on_bus_stop = bus_stop_name[0]
        get_off_bus_stop = bus_stop_name[1]

        value_get_on_bus_stop = number_lett_dict[get_on_bus_stop]
        value_get_off_bus_stop = number_lett_dict[get_off_bus_stop]

        if value_get_on_bus_stop > value_get_off_bus_stop:
            # person taking the bus on the oposite direction to the bus route
            return 1
        elif value_get_on_bus_stop == value_get_off_bus_stop:
            # gets on and off the same bus stop
            return 2
        else:
            # person getting on and off bus stop, following the bus route
            return 3   
        
        
    def plot_bus_load(self): 
        '''
        Shows the amount of people on the bus during the bus journey.
        '''
        stops = {step[2]:0 for step in self.class_route.read_route()
                                                         if step[2]}
        for passenger in self.passengers:
            bus_stop_name = self.passenger_get_on_off_bus_stop_name(passenger.return_values())
            # passenger gets on at bus stop
            get_on_bus_stop = bus_stop_name[0]
            # passenger gets off at bus stop
            get_off_bus_stop = bus_stop_name[1]

            # check to see if journey is allowed
            check_journey_allowed = self.passenger_journey_allowed(passenger.return_values())
            if check_journey_allowed == 3: 
                # ie. person getting on at bus stop 'A'.
                stops[get_on_bus_stop] += 1
                # person leaving bus stop at 'C'.
                stops[get_off_bus_stop] -= 1
                
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
        pace = passenger[2]
        
        # Name of the bus stop they will need to get on and off.
        bus_stop_name = self.passenger_get_on_off_bus_stop_name(passenger)
        get_on_bus_stop = bus_stop_name[0]
        get_off_bus_stop = bus_stop_name[1]

        # Distance walked by the passenger to the bus stop and to the final location.
        walk_to_from_bus_stop = self.passenger_walk_distance_to_from_bus_stop(passenger)
        walk_distance_get_on_bus_stop = walk_to_from_bus_stop[0]
        walk_distance_get_off_bus_stop = walk_to_from_bus_stop[1]
        
        # The bus route timetable.
        bus_times = self.class_route.timetable()
        
        # Calculating the length of the bus ride.
        bus_travel = bus_times[get_off_bus_stop] - \
                     bus_times[get_on_bus_stop]
        
        # Finding out how long the passenger walked for to get to the bus stop
        # and to get to their final destination from the bus stop they got off.
        walk_travel = walk_distance_get_on_bus_stop * pace + \
                      walk_distance_get_off_bus_stop * pace
        
        return(bus_travel, walk_travel, bus_stop_name, walk_to_from_bus_stop)


    def travel_time(self, passenger_id):
        '''This returns a dictioanry containing how long the passenger was on the bus and how long they walked for'''
        # Need to add BC to not add times for not allowed journeys
        # self.bus_travel_time_dict = {}

        for passenger_identification, passenger in enumerate(self.passengers):
            # check to see if journey is allowed
            check_journey_allowed = self.passenger_journey_allowed(passenger.return_values())
            if check_journey_allowed == 3: 
                self.bus_travel_time_dict[passenger_identification] = {'bus':self.passenger_trip_time(passenger.return_values())[0]
                                                                   ,'walk':self.passenger_trip_time(passenger.return_values())[1]}
            else:
                self.bus_travel_time_dict[passenger_identification] = {'bus':0
                                                                   ,'walk':passenger.walk_time()}
                
        return self.bus_travel_time_dict[passenger_id]
    
    
    def print_time_stats(self):
        '''
        Prints the average time passengers spent on the bus and walking
        '''
        sum_bus_time = 0
        sum_walk_time = 0
        for i in range(len(self.passengers)):
            # Uses the return values from the travel_time method to calculate the average
            sum_bus_time += self.travel_time(i)['bus']
            sum_walk_time += self.travel_time(i)['walk']

        average_bus_time = sum_bus_time/(i+1.0) 
        average_walk_time = sum_walk_time/(i+1.0)
        
        print((f"Average time on the bus: {average_bus_time:3.2f} minutes, \n"
              f"Average time walking: {average_walk_time:3.2f} minutes."))
    
    
    def recommended_route(self):
        '''
        Advices the passenger on what would be the best travelling option
        for their journey.
        Take the bus or walk it.
        '''
        for passenger_id, passenger in enumerate(self.passengers):
            # How long the passenger will need to walk for
            walking_time = passenger.walk_time()
            # check to see if journey is allowed
            check_journey_allowed = self.passenger_journey_allowed(passenger.return_values())
            print("\n")
            print(f"Trip for passenger: {passenger_id}")
            if check_journey_allowed == 1:
                # Bus travels in the opposite direction of the passenger journey
                print("The bus does not travel in the direction of your destination.")
                print("It will be better if you walked.")
                print(f"The total time of the journey if you walked is: {walking_time:03.2f} minutes.")            

            elif check_journey_allowed == 2:
                # The closest bus stop to get on is the same bus stop to get off at
                print("The bus route does not suit your journey.")
                print("It will be better if you walked.")
                print(f"The total time of travel if you walked is: {walking_time:03.2f} minutes.")            

            else:
                # The passenger can use the bus to travel
                bus_travel, walk_travel, bus_stop_name, walk_to_from_bus_stop = self.passenger_trip_time(passenger.return_values())
                # Name of the bus stop they will need to get on and off.
                get_on_bus_stop = bus_stop_name[0]
                get_off_bus_stop = bus_stop_name[1]
                # Distance walked by the passenger to get on the bus and distace the passenger
                # walked from the bus they got off to their final destination.
                walk_distance_get_on_bus_stop = walk_to_from_bus_stop[0]
                walk_distance_get_off_bus_stop = walk_to_from_bus_stop[1]
                total_time = bus_travel + walk_travel
                def print_bus_journey_direction(walk_distance_get_on_bus_stop, walk_distance_get_off_bus_stop
                                                ,get_on_bus_stop, get_off_bus_stop):
                    print("If you take the bus, you should take this route:")
                    print((f" Walk {walk_distance_get_on_bus_stop:3.2f} units to stop {get_on_bus_stop}, \n"
                    f" get on the bus and aligth at stop {get_off_bus_stop} and \n"
                    f" walk {walk_distance_get_off_bus_stop:3.2f} units to your destination."))
                    print(f" Total time of travel: {total_time:03.2f} minutes.")
                    
                if walking_time > total_time:
                    # Print journey option when walking takes longer than the bus ride
                    print((f"It is advised that you take the bus as walking will take : {walking_time:03.2f} minutes. "))
                    print_bus_journey_direction(walk_distance_get_on_bus_stop, walk_distance_get_off_bus_stop
                                                ,get_on_bus_stop, get_off_bus_stop)

                elif round(walking_time,0) == round(total_time,0):
                    # Rounds the time to nearest minute to allow the passenger to make the better decision
                    print(f"You can either walk or take the bus, both journey methods take : {walking_time:03.2f} minutes. ")
                    print(f"The total time of travel if you walked is: {walking_time:03.2f} minutes.")       
                    print("\n")
                    print_bus_journey_direction(walk_distance_get_on_bus_stop, walk_distance_get_off_bus_stop
                                                ,get_on_bus_stop, get_off_bus_stop)

                else:
                    # Print journey option when taking the bus takes longer than walking
                    diff_in_time = total_time - walking_time
                    print(f"The total time of travel if you walked is: {walking_time:03.2f} minutes.")       
                    print((f"Taking the the bus will make your journey: {diff_in_time:03.2f} " 
                           "minutes longer compared to walking, it's up to you if you want to walk or take the bus."))
                    print("\n")
                    print_bus_journey_direction(walk_distance_get_on_bus_stop, walk_distance_get_off_bus_stop
                                                ,get_on_bus_stop, get_off_bus_stop)

if __name__ == "__main__":
    route = Route("route.csv")
    passengers = read_passengers("passenger.csv")
    # passenger = ((0, 1), (3, 9), 16)
    passengers_list = [Passenger(start,end,speed) for start, end, speed in passengers]
    journey = Journey(route,passengers_list)
    journey.plot_bus_load()
    for i in range(len(passengers_list)):
        print(journey.travel_time(i))
    journey.print_time_stats()
    journey.recommended_route()


    print("---------------------------------------")
    john = Passenger(start=(0,2), end=(8,1), speed=15)
    mary = Passenger(start=(0,0), end=(6,2), speed=12)  
    john_mary = [john,mary]
    journey2 = Journey(route,john_mary)
    journey2.plot_bus_load()
    for i in range(len(john_mary)):
        print(journey2.travel_time(i))
    # print(journey.travel_time(0))
    journey2.print_time_stats()
    journey2.recommended_route()
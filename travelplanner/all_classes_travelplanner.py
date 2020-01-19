import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from string import ascii_uppercase as aci
from operator import itemgetter


class Passenger:
    def __init__(self, start, end, speed):
        self.x1, self.y1 = start
        self.x2, self.y2 = end
        self.speed = speed

        if type(self.x1) == str:
            raise Exception('x_1 coordinate should not be a letter but a'
                            'number. The value of x_1 was: {}'.format(self.x1))
        elif type(self.x2) == str:
            raise Exception('x_2 coordinate should not be a letter but a'
                            'number. The value of x_2 was: {}'.format(self.x2))
        elif type(self.y1) == str:
            raise Exception('y_1 coordinate should not be a letter but a'
                            'number. The value of y_1 was: {}'.format(self.y1))
        elif type(self.y2) == str:
            raise Exception('y_2 coordinate should not be a letter but a'
                            'number. The value of y_2 was: {}'.format(self.y2))
        elif type(self.speed) == str:
            raise Exception('speed should not be a letter but a number.'
                            'The value of speed was: {}'.format(self.speed))

    def walk_time(self):
        '''
        Calculates the time it would take a passenger to reach the final
        destination from their starting location.
        '''
        self.time = np.sqrt((self.x2-self.x1)**2
                            + (self.y2-self.y1)**2) * self.speed

        return self.time

    def return_values(self):
        return((self.x1, self.y1), (self.x2, self.y2), self.speed)


def passengers_list(passengers):
    my_pass_list = []
    for start, end, speed in passengers:
        my_pass_list.append(Passenger(start, end, speed))
    return my_pass_list


class Route:
    def __init__(self, route, bus_speed=10):
        self.route = route
        self.bus_speed = bus_speed

    def read_route(self):
        '''
        This reads the bus route csv file and returns a list containing
        touples with the route of the bus and the name of the bus stops.
        '''
        if type(self.route) == list:
            return self.route
        else:
            df = pd.read_csv(self.route, names=['x1', 'y1', 'stop'])
            df.fillna(0, inplace=True)
            # Make collapsed columns for positional dat
            df['x1, y1, stop'] = list(zip(df['x1'], df['y1'], df['stop']))
            # Make output list
            data_out = [(df.iloc[i]['x1, y1, stop']) for i in range(len(df))]

            return data_out

    def plot_map(self, save_plot=None):

        route = self.read_route()

        for x, y, stop in route:
            if type(x) == str:
                raise Exception('The bus journey x coordinate should not be a'
                                'letter but a number.'
                                'The value of x was: {}'.format(x))
            elif type(y) == str:
                raise Exception('The bus journey y coordinate should not be a'
                                'letter but a number.'
                                'The value of y was: {}'.format(y))
            elif type(stop) != str and stop != 0:
                raise Exception('The bus journey bus stop should not be a'
                                'number but a letter.'
                                'The value of x was: {}'.format(stop))

        max_x = max([n[0] for n in route]) + 5  # adds padding
        max_y = max([n[1] for n in route]) + 5
        grid = np.zeros((max_y, max_x))

        for x, y, stop in route:

            grid[y, x] = 1
            if stop:
                grid[y, x] += 1

        fig, ax = plt.subplots(1, 1, figsize=(8, 6))
        ax.pcolor(grid)
        ax.invert_yaxis()
        ax.set_aspect('equal', 'datalim')
        if save_plot:
            plt.savefig("map.png")
        # else:
            # plt.show()

    # stops is a dictionary holding the bus stop name and time of arrival.
    # starting from 0 at stop A and taking 10 mins to reach checkpoints in
    # the travel of bus
    def timetable(self):
        '''
        Generates a timetable for a route as minutes from its first stop.
        With a user defined bus_speed otherwise default bus_speed = 10
        '''
        if type(self.bus_speed) == str:
            raise Exception('The speed of the bus should not be a letter,'
                            'but a number.The value of bus_speed was: {}'
                            .format(self.bus_speed))
        # stops is a dictionary holding the bus stop name and time of arrival.
        # starting from 0 at stop A and taking 10 mins to reach checkpoints in
        # the travel of bus.
        # can potentially change the speed

        route = self.read_route()
        time = 0
        stops = {}
        for step in route:
            if step[2]:
                stops[step[2]] = time
            time += self.bus_speed
        return stops

    def route_cc(self):
        '''
        Converts a set of route into a Freeman chain code
        '''
        # starting cord of bus route
        # Choosing bus stop A and giving (x,y) cord for it

        route = self.read_route()
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
        freeman_coord2cc = {val: key for key, val in freeman_cc2coord.items()}
        for b, a in zip(route[1:], route):
            x_step = b[0] - a[0]
            y_step = b[1] - a[1]
            cc.append(int(freeman_coord2cc[(x_step, y_step)]))

        return cc

    def check_error(self):
        '''
        The bus is not allowed to move diagonally. This function checks wether
        the bus moves diagonally.
        To then use the result from this function to either allow the input
        passenger route or not.
        If the return value is > 0 then there is a diagonal movement,
        otherwise there isn't and the route is valid.
        '''
        route_cc = self.route_cc()

        is_odd = 0
        for cc_number in route_cc:
            if cc_number % 2 != 0:
                is_odd += 1
        if is_odd > 0:
            return 1
        else:
            return 0


def read_passengers(file_name):
    '''
    Reads the passengers csv file and returns a list containing touples with
    the details of the starting and ending location, and speed for a passenger.
    '''
    df = pd.read_csv(file_name, names=['x1', 'y1', 'x2', 'y2', 'speed'])
    # Make collapsed columns for positional dat
    df['x1, y1'] = list(zip(df['x1'], df['y1']))
    df['x2, y2'] = list(zip(df['x2'], df['y2']))
    # Make output list
    data_out = [(df.iloc[i]['x1, y1'], df.iloc[i]['x2, y2'],
                 (df.iloc[i]['speed'])) for i in range(len(df))]
    return data_out


class Journey(Route, Passenger):
    def __init__(self, route, passengers):
        self.route = route
        self.passengers = passengers
        self.bus_trav_time_dic = {}

    def passenger_trip(self, passenger):
        '''
        Returns the distance to the nearest bus stop to starting
        and ending location.
        '''
        # Passed in a single passenger details from passangers containing the
        # starting location, ending location and pace of passenger.
        # pace = minutes per unit grid
        # check if the passenger file is valid

        start, end, speed = passenger[0], passenger[1], passenger[2]
        if type(start[0]) == str or type(start[1]) == str:
            raise Exception('The passenger starting coordinate contains a'
                            'wrong input. The value of the'
                            'starting coordinate:{}'.format(start))
        elif type(end[0]) == str or type(end[1]) == str:
            raise Exception('The passenger end coordinate contains'
                            'a wrong input. The value of the'
                            'end coordinate: {}'.format(end))
        elif type(speed) == str:
            raise Exception('The passenger speed contains is of wrong input.'
                            'The value of the speed: {}'.format(speed))

        if self.route.check_error() > 0:
            raise ValueError('The bus route has a diagonal movement')
        else:
            # Stops holds the cordinates for a bus stop in the bus route
            # journey.
            # unpacked stops into x, y, stop.
            stops = [value for value in self.route.read_route() if value[2]]

        def locate_min_distance(touple_dis_stop):
            my_dis = []
            my_stop = []
            for dis, stop in touple_dis_stop:
                my_dis.append(dis)
                my_stop.append(stop)
            small = min(my_dis)

            small_id = [ind for ind, ele in enumerate(my_dis) if small == ele]

            return small, [my_stop[i] for i in small_id]

        def distance(s_or_e, start, end, stops):
            my_dist = []
            for i, x_y_stop in enumerate(stops):
                x, y, stop = x_y_stop[0], x_y_stop[1], x_y_stop[2]
                if s_or_e == 0:
                    # finding the starting distance between passenger
                    # and bus stop
                    dis = math.sqrt((x - start[0])**2 + (y - start[1])**2)
                else:
                    # finding the ending distance between passenger
                    # and bus stop
                    dis = math.sqrt((x - end[0])**2 + (y - end[1])**2)
                my_dist.append([dis, stop])
            return my_dist

        start_dist = distance(0, start, end, stops)
        closer_start_points = locate_min_distance(start_dist)

        end_dist = distance(1, start, end, stops)
        closer_end_points = locate_min_distance(end_dist)

        return(closer_start_points, closer_end_points)

    def passenger_bus_stop_name(self, passenger):
        '''
        Returns the bus stop name that the passenger gets on and off.
        '''
        walk_distance_stops = self.passenger_trip(passenger)
        get_on_bus_stop = walk_distance_stops[0][1]
        get_off_bus_stop = walk_distance_stops[1][1]

        return(get_on_bus_stop, get_off_bus_stop)

    def passenger_walk_bus_stop(self, passenger):
        '''
        The distance the passenger needs to walk to get on the bus and
        the distance the passenger needs to walk to their final destination
        from the stop they got off.
        '''
        walk_distance_stops = self.passenger_trip(passenger)
        walk_distance_get_on_bus_stop = walk_distance_stops[0][0]
        walk_distance_get_off_bus_stop = walk_distance_stops[1][0]

        return(walk_distance_get_on_bus_stop, walk_distance_get_off_bus_stop)

    def passenger_trip_time(self, passenger, isTesting=None):
        '''
        Finds the duration of the journey for the passenger onn the bus
        and walking.
        '''
        pace = passenger[2]

        # Name of the bus stop they will need to get on and off.
        bus_stop_name = self.passenger_bus_stop_name(passenger)
        get_on = bus_stop_name[0]
        get_off = bus_stop_name[1]

        # Distance walked by the passenger to the bus stop
        # and to the final location.
        walk_to_from_bus_stop = self.passenger_walk_bus_stop(passenger)
        walk_on = walk_to_from_bus_stop[0]
        walk_off = walk_to_from_bus_stop[1]

        def time_bus_stp(get_on_or_off_bus_stop):
            bus_times = self.route.timetable()
            bus_time_and_stop = []
            # making a 2D array containing a touple,
            # where the first value in touple holds,
            # the time arrival of the bus at second value,
            # of the touple bus stop,
            # at which the passenger either gets on or off
            for stop in get_on_or_off_bus_stop:
                bus_time_and_stop.append([bus_times[stop], stop])
            return bus_time_and_stop

        # Minimising the time the passenger travels for by not,
        # adding unecessary bus stops to their journey.
        # Finding the nearest and earliest bus stop to the,
        # passengers final destination.
        get_off_bus_stop = min(time_bus_stp(get_off), key=itemgetter(0))
        # Finding the nearest and latest bus stop,
        # to the passengers starting destination
        get_on_bus_stop = max(time_bus_stp(get_on), key=itemgetter(0))

        min_trav_time_get_off_bus = get_off_bus_stop[0]
        min_trav_time_get_on_bus = get_on_bus_stop[0]

        # How long the passenger travelled for in the bus,
        # by chossing best bus route option
        bustime = min_trav_time_get_off_bus - min_trav_time_get_on_bus

        # Finding out how long the passenger walked for to get to the bus stop
        # and to get to their final destination from the bus stop they got off.
        min_time_on = get_on_bus_stop[1]
        min_time_off = get_off_bus_stop[1]

        walktime = walk_on * pace + walk_off * pace
        vals = bustime, walktime, min_time_on, min_time_off, walk_on, walk_off
        if isTesting:
            my_vals = []
            for item in vals:
                if type(item) != str:
                    my_vals.append(round(item, 2))
                else:
                    my_vals.append(item)
            return my_vals
        else:
            return vals

    def passenger_journey_allowed(self, passenger):
        '''
        Checks wether the passenger journey travels in the same direction as
        the bus route, to see if the passenger can use the bus.

        Making a dictionary of the alphabet with key = Letter,
        and value = corresponding number. ie. The bus goes from A=1 to Z=26,
        if the passenger gets on at Z=26 and wants to go to A=1,
        it can not do this, as the bus only travels in one direction.
        Therefore the end location bus stop number must be greater than,
        the start location bus stop number. The better option is to walk.
        '''

        number_lett_dict = dict(zip(aci, range(1, 27)))
        get_on_bus_stop_name = self.passenger_trip_time(passenger)[2]
        get_off_bus_stop_name = self.passenger_trip_time(passenger)[3]

        value_get_on_bus_stop = number_lett_dict[get_on_bus_stop_name]
        value_get_off_bus_stop = number_lett_dict[get_off_bus_stop_name]

        if value_get_on_bus_stop > value_get_off_bus_stop:
            # person taking the bus on the oposite direction to the bus route
            return 1
        elif value_get_on_bus_stop == value_get_off_bus_stop:
            # gets on and off the same bus stop
            return 2
        else:
            # person getting on and off bus stop, following the bus route
            return 3

    def plot_bus_load(self, save_plot=None, isTesting=None):
        '''
        Shows the amount of people on the bus during the bus journey.
        '''
#         stops = self.stops
        route = self.route
        stops = {step[2]: 0 for step in route.read_route() if step[2]}
        for passenger in self.passengers:
            pass_val = passenger.return_values()
            get_on_bus_stop_name = self.passenger_trip_time(pass_val)[2]
            get_off_bus_stop_name = self.passenger_trip_time(pass_val)[3]
            # check to see if journey is allowed
            check_journ_allowed = self.passenger_journey_allowed(pass_val)
            if check_journ_allowed == 3:
                # ie. person getting on at bus stop 'A'.
                stops[get_on_bus_stop_name] += 1
                # person leaving bus stop at 'C'.
                stops[get_off_bus_stop_name] -= 1

        if isTesting:
            return stops
        else:
            for i, stop in enumerate(stops):
                if i > 0:
                    stops[stop] += stops[prev]
                prev = stop
            fig, ax = plt.subplots()
            ax.step(range(len(stops)), list(stops.values()), where='post')
            ax.set_xticks(range(len(stops)))
            ax.set_xticklabels(list(stops.keys()))
            if save_plot:
                plt.savefig("load.png")
            # else:
            #     plt.show()

    def travel_time(self, passenger_id):
        '''
        This returns a dictioanry containing how long the passenger,
        was on the bus and how long they walked for.
        '''
        # Need to add BC to not add times for not allowed journeys

        for pass_id, passenger in enumerate(self.passengers):
            # check to see if journey is allowed
            pass_val = passenger.return_values()
            check_journey_allowed = self.passenger_journey_allowed(pass_val)
            if check_journey_allowed == 3:
                bus = self.passenger_trip_time(pass_val)[0]
                walk = self.passenger_trip_time(pass_val)[1]
                self.bus_trav_time_dic[pass_id] = {'bus': bus, 'walk': walk}
            else:
                pass_walk = passenger.walk_time()
                self.bus_trav_time_dic[pass_id] = {'bus': 0, 'walk': pass_walk}

        return self.bus_trav_time_dic[passenger_id]

    def print_time_stats(self):
        '''
        Prints the average time passengers spent on the bus and walking
        '''
        sum_bus_time = 0
        sum_walk_time = 0
        for i in range(len(self.passengers)):
            # Uses the return values from the travel_time method,
            #  to calculate the average.
            sum_bus_time += self.travel_time(i)['bus']
            sum_walk_time += self.travel_time(i)['walk']

        average_bus_time = sum_bus_time/(i+1.0)
        average_walk_time = sum_walk_time/(i+1.0)

        print((f"Average time on the bus: {average_bus_time:3.2f} minutes. \n"
              f"Average time walking: {average_walk_time:3.2f} minutes."))

    def recommended_route_for_passenger(self, id):
        '''
        Advices the passengers on what would be the best travelling option
        for their journey.
        Take the bus or walk it.
        '''
        self.id = id

        # recommended_route_for_passenger_dict = {}
        for passenger_id, passenger in enumerate(self.passengers):
            # How long the passenger will need to walk for
            walking_time = passenger.walk_time()
            pass_val = passenger.return_values()
            # check to see if journey is allowed
            check_journey_allowed = self.passenger_journey_allowed(pass_val)
            print("\n")
            if passenger_id == self.id:
                # print(f"Trip for passenger: {passenger_id}")
                if check_journey_allowed == 1:
                    # Bus travels in the opposite direction,
                    # of the passenger journey
                    return (f"Trip for passenger: {passenger_id}\n"
                            "The bus does not travel in the direction,"
                            "of your destination.\n"
                            "It will be better if you walked.\n"
                            "The total time of the journey if you walked is:"
                            f"{walking_time:03.2f} minutes.")

                elif check_journey_allowed == 2:
                    # The closest bus stop to get on,
                    # is the same bus stop to get off at
                    return (f"Trip for passenger: {passenger_id}\n"
                            "The bus route does not suit your journey.\n"
                            "It will be better if you walked.\n"
                            "The total time of travel if you walked is:"
                            f"{walking_time:03.2f} minutes.")

                else:
                    # Name of the bus stop they will need to get on and off.
                    # Distance walked by the passenger to get on the bus,
                    # and distance the passenger.
                    # walked from the bus they got off,
                    # to their final destination.
                    # The passenger can use the bus to travel
                    pass_trip = self.passenger_trip_time(pass_val)
                    bustime, walktime = pass_trip[0], pass_trip[1]
                    min_time_on, min_time_off = pass_trip[2], pass_trip[3]
                    walk_on, walk_off = pass_trip[4], pass_trip[5]
                    total_time = bustime + walktime

                    if walking_time > total_time:
                        # Print journey option when,
                        # walking takes longer than the bus ride

                        return (f"Trip for passenger: {passenger_id}\n"
                                "It is advised that you take the bus"
                                "as walking will take:"
                                f"{walking_time:03.2f} minutes.\n"
                                "If you take the bus,"
                                "you should take this route:\n"
                                f"Walk {walk_on:3.2f} units to stop:"
                                "{min_time_on}, \n"
                                f"get on the bus and aligth at stop:"
                                "{min_time_off} and \n"
                                f"walk {walk_off:3.2f} units,"
                                "to your destination.\n"
                                f"Total time of travel:"
                                "{total_time:03.2f} minutes.")

                    elif round(walking_time, 0) == round(total_time, 0):
                        # Rounds the time to nearest minute to allow,
                        # the passenger to make the better decision

                        return (f"Trip for passenger: {passenger_id}\n"
                                "You can either walk or take the bus,"
                                "both journey methods take:"
                                f"{walking_time:03.2f} minutes."
                                "The total time of travel if you walked is:"
                                f"{walking_time:03.2f} minutes. \n"
                                "If you take the bus, you should take route:\n"
                                "Walk {walk_on:3.2f} units to stop:"
                                f"{min_time_on}, \n"
                                "get on the bus and aligth at stop:"
                                f"{min_time_off} and \n"
                                f"walk:{walk_off:3.2f} units to destination.\n"
                                "Total time of travel:"
                                f"{total_time:03.2f} minutes.")

                    else:
                        # Print journey option when taking the bus,
                        # takes longer than walking
                        diff_in_time = total_time - walking_time
                        return (f"Trip for passenger: {passenger_id}\n"
                                "The total time of travel if you walked is:"
                                f"{walking_time:03.2f} minutes. \n"
                                "Taking the the bus will make your journey:"
                                f"{diff_in_time:03.2f} \n"
                                "minutes longer compared to walking,"
                                "it's up to you if you want to walk"
                                "or take the bus.\n"
                                "If you take the bus, take this route:\n"
                                f"Walk {walk_on:3.2f} units,"
                                f"to stop {min_time_on}, \n"
                                "get on the bus ,and"
                                f"aligth at stop {min_time_off} and \n"
                                f"walk {walk_off:3.2f} units to destination.\n"
                                f"Total time of travel:"
                                f"{total_time:03.2f} minutes.")


# if __name__ == "__main__":
# from travelplanner import Passenger, Route, Journey, read_passengers
# from travelplanner import "passenger.csv", "route.csv"
# route = Route("route.csv")
# passengers = read_passengers("passenger.csv")
# passengers_list = [Passenger(start,end,speed) for start, end, speed in
# passengers]
# journey = Journey(route,passengers_list)
# journey.plot_bus_load()
# for i in range(len(passengers_list)):
#     print(journey.travel_time(i))
# journey.print_time_stats()
# for i in range(len(passengers_list)):
#     print(journey.recommended_route_for_passenger(i))
# route.plot_map()

#     print("----------------------------------------")
    # john = Passenger(start=(0,2), end=(8,1), speed=15)
    # mary = Passenger(start=(0,0), end=(6,2), speed=12)
    # john_mary = [john,mary]
    # journey2 = Journey(route,john_mary)
    # journey2.plot_bus_load()
    # for i in range(len(john_mary)):
    #     print(journey2.travel_time(i))
    # # print(journey.travel_time(0))
    # journey2.print_time_stats()
    # for i in range(len(john_mary)):
    #     print(journey2.recommended_route_for_passenger(i))

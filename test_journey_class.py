from journey_class import Journey, read_passengers 
from route_class import Route
from passenger_class import Passenger
import pytest

#param
def test_read_route():
    passengers = read_passengers("passenger.csv")
    assert passengers == [((1, 6), (3, 5), 11), ((10, 0), (12, 1), 14), \
    ((0, 1), (3, 9), 16), ((5, 5), (6, 1), 15), ((10, 11), (18, 0), 16), \
    ((2, 6), (3, 6), 9), ((3, 4), (13, 11), 11), ((3, 5), (7, 0), 25),\
    ((3, 9), (3, 11), 18)]

# class Test_journey_class:
#param
def test_passenger_get_on_off_bus_stop_name():
    route = Route("route.csv")
    passengers = read_passengers("passenger.csv")
    passengers_list = [Passenger(start,end,speed) for start, end, speed in passengers]
    journey = Journey(route,passengers_list) 
    passenger = ((0, 1), (3, 9), 16)
    assert journey.passenger_get_on_off_bus_stop_name(passenger) == ('G', 'A')
#param
def test_passenger_walk_distance_to_from_bus_stop():
    route = Route("route.csv")
    passengers = read_passengers("passenger.csv") 
    passengers_list = [Passenger(start,end,speed) for start, end, speed in passengers]
    journey = Journey(route,passengers_list)
    passenger = ((0, 1), (3, 9), 16)
    
    assert journey.passenger_walk_distance_to_from_bus_stop(passenger) == (1.0, 6.324555320336759)

@pytest.mark.parametrize(
    'passenger, expected', [
        (((0, 1), (3, 9), 16),1),
        (((1, 6), (3, 5), 11),2),
        (((10, 11), (18, 0), 16),3),
    ]
)
def test_passenger_journey_allowed(passenger, expected):
    route = Route("route.csv")
    passengers = read_passengers("passenger.csv") 
    passengers_list = [Passenger(start,end,speed) for start, end, speed in passengers]
    journey = Journey(route,passengers_list)
    # passenger = ((0, 1), (3, 9), 16)
    journey_allowed = journey.passenger_journey_allowed(passenger)
    assert journey_allowed == expected
#param
def test_plot_bus_load():
    route = Route("route.csv")
    passengers = read_passengers("passenger.csv") 
    passengers_list = [Passenger(start,end,speed) for start, end, speed in passengers]
    journey = Journey(route,passengers_list)
    bus_plot_load = journey.plot_bus_load(1)
    assert bus_plot_load ==  {'A': 0, 'B': 1, 'C': 0, 'D': -1, 'E': 0, 'F': 0, 'G': 0}
    # passenger = ((0, 1), (3, 9), 16)
#param
def test_passenger_trip_time():
    route = Route("route.csv")
    passengers = read_passengers("passenger.csv") 
    passengers_list = [Passenger(start,end,speed) for start, end, speed in passengers]    
    journey = Journey(route,passengers_list)
    passenger = ((0, 1), (3, 9), 16)
    passenger_trip_time = journey.passenger_trip_time(passenger)
    assert passenger_trip_time == (-260, 117.19288512538814, ('G', 'A'), (1.0, 6.324555320336759))
#param
def test_travel_time():
    route = Route("route.csv")
    passengers = read_passengers("passenger.csv") 
    passengers_list = [Passenger(start,end,speed) for start, end, speed in passengers]    
    journey = Journey(route,passengers_list)
    travel_time = journey.travel_time(2)
    assert travel_time == {'bus': 0, 'walk': 136.7040599250805}

def test_print_time_stats():
    route = Route("route.csv")
    passengers = read_passengers("passenger.csv") 
    passengers_list = [Passenger(start,end,speed) for start, end, speed in passengers]    
    journey = Journey(route,passengers_list)
    print_time_stats = journey.print_time_stats()
    assert print_time_stats == print((f"Average time on the bus: 6.67 minutes. \n"
                                    f"Average time walking: 86.79 minutes."))

def test_recommended_route_for_passenger():
    route = Route("route.csv")
    passengers = read_passengers("passenger.csv") 
    passengers_list = [Passenger(start,end,speed) for start, end, speed in passengers]    
    journey = Journey(route,passengers_list)    
    recommended_route_for_passenger = journey.recommended_route_for_passenger(0)
    assert recommended_route_for_passenger == print("Trip for passenger: 0 \n"
                                                    "The bus route does not suit your journey.\n"
                                                    "It will be better if you walked.\n"
                                                    "The total time of travel if you walked is: 24.60 minutes.\n")
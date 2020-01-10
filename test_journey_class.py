from journey_class import Journey, read_passengers 
from route_class import Route
from passenger_class import Passenger
import pytest

#param
@pytest.mark.parametrize(
    'passenger, expected', [
        ("testpassenger.csv",[((6, 11), (18, 0), 9), ((1, 1), (3, 0), 22), ((0, 7), (0, 10), 19)]),
        ("testpassenger2.csv",[((1, 5), (1, 28), 25),((9, 10), (11, 10), 19),((0, 14), (14, 0), 13),
                                 ((5, 7), (9, 8), 19),((9, 8), (10, 2), 21)]),
        ("testpassenger3.csv",[((8, 3), (8, 3), 25), ((20, 7), (0, 0), 10), ((8, 2), (0, 4), 14)])
    ]
)
def test_read_route(passenger,expected):
    passengers = read_passengers(passenger)
    assert passengers == expected

# class Test_journey_class:
#param
@pytest.mark.parametrize(
    'passenger, expected', [
        (((0, 1), (3, 9), 16),('G', 'A')),
        (((3, 4), (13, 11), 11),('F', 'B')),
        (((3, 9), (3, 11), 18),('A', 'A'))
    ]
)
def test_passenger_get_on_off_bus_stop_name(passenger, expected):
    route = Route("route.csv")
    passengers = read_passengers("passenger.csv")
    passengers_list = [Passenger(start,end,speed) for start, end, speed in passengers]
    journey = Journey(route,passengers_list) 
    assert journey.passenger_get_on_off_bus_stop_name(passenger) == expected
#param
@pytest.mark.parametrize(
    'passenger, expected', [
        (((0, 1), (3, 9), 16),(1.0, 6.324555320336759)),
        (((3, 4), (13, 11), 11),(2.23606797749979, 3.605551275463989)),
        (((3, 9), (3, 11), 18),(6.324555320336759, 7.211102550927978))
    ]
)
def test_passenger_walk_distance_to_from_bus_stop(passenger, expected):
    route = Route("route.csv")
    passengers = read_passengers("passenger.csv") 
    passengers_list = [Passenger(start,end,speed) for start, end, speed in passengers]
    journey = Journey(route,passengers_list)    
    assert journey.passenger_walk_distance_to_from_bus_stop(passenger) == expected

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
@pytest.mark.parametrize(
    'route, passengers, expected', [
        ("testroute.csv","testpassenger.csv",{'A': 0, 'B': 0, 'C': 0}),
        ("testroute2.csv","testpassenger2.csv",{'A': 2, 'B': 0, 'C': -2, 'D': 0}),
        ("testroute3.csv","testpassenger3.csv",{'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0})
    ]
)
def test_plot_bus_load(route, passengers, expected):
    route = Route(route)
    passengers = read_passengers(passengers) 
    passengers_list = [Passenger(start,end,speed) for start, end, speed in passengers]
    journey = Journey(route,passengers_list)
    bus_plot_load = journey.plot_bus_load(1)
    assert bus_plot_load ==  expected
#param
@pytest.mark.parametrize(
    'passenger, expected', [
        (((0, 1), (3, 9), 16),(-260, 117.19288512538814, ('G', 'A'), (1.0, 6.324555320336759))),
        (((1, 6), (3, 5), 11),(0, 64.11269837220809, ('F', 'F'), (3.0, 2.8284271247461903))),
        (((10, 11), (18, 0), 16),(60, 187.30050248777457, ('B', 'D'), (3.1622776601683795, 8.54400374531753)))
    ]
)
def test_passenger_trip_time(passenger, expected):
    route = Route("route.csv")
    passengers = read_passengers("passenger.csv") 
    passengers_list = [Passenger(start,end,speed) for start, end, speed in passengers]    
    journey = Journey(route,passengers_list)
    passenger_trip_time = journey.passenger_trip_time(passenger)
    assert passenger_trip_time == expected
#param
@pytest.mark.parametrize(
    'id, expected', [
        (0,{'bus': 0, 'walk': 24.596747752497688}),
        (1,{'bus': 0, 'walk': 31.304951684997057}),
        (2,{'bus': 0, 'walk': 136.7040599250805})
    ]
)
def test_travel_time(id, expected):
    route = Route("route.csv")
    passengers = read_passengers("passenger.csv") 
    passengers_list = [Passenger(start,end,speed) for start, end, speed in passengers]    
    journey = Journey(route,passengers_list)
    travel_time = journey.travel_time(id)
    assert travel_time == expected

@pytest.mark.parametrize(
    'route, passengers, expected', [
        ("testroute.csv","testpassenger.csv","Average time on the bus: 0.00 minutes.\nAverage time walking: 84.23 minutes."),
        ("testroute2.csv","testpassenger2.csv","Average time on the bus: 8.00 minutes.\nAverage time walking: 208.34 minutes."),
        ("testroute3.csv","testpassenger3.csv","Average time on the bus: 0.00 minutes.\nAverage time walking: 109.11 minutes.")
    ]
)
def test_print_time_stats(route, passengers, expected):
    route = Route(route)
    passengers = read_passengers(passengers) 
    passengers_list = [Passenger(start,end,speed) for start, end, speed in passengers]    
    journey = Journey(route,passengers_list)
    assert journey.print_time_stats() == print(expected)


@pytest.mark.parametrize(
    'id, expected', [
        (0,"Trip for passenger: 0\nThe bus route does not suit your journey.\nIt will be better if you walked.\nThe total time of travel if you walked is: 24.60 minutes."),
        (1,"Trip for passenger: 1\nThe bus route does not suit your journey.\nIt will be better if you walked.\nThe total time of travel if you walked is: 31.30 minutes."),
        (2,"Trip for passenger: 2\nThe bus does not travel in the direction of your destination.\nIt will be better if you walked.\nThe total time of the journey if you walked is: 136.70 minutes.")
    ]
)
def test_recommended_route_for_passenger(id, expected):
    route = Route("route.csv")
    passengers = read_passengers("passenger.csv") 
    passengers_list = [Passenger(start,end,speed) for start, end, speed in passengers]    
    journey = Journey(route,passengers_list)    
    recommended_route_for_passenger = journey.recommended_route_for_passenger(id)
    assert print(recommended_route_for_passenger) == print(expected)
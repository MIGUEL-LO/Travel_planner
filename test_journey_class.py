from journey_class import Journey, read_passengers 
from route_class import Route
from passenger_class import Passenger
import pytest

def test_read_route():
    passengers = read_passengers("passenger.csv")
    assert passengers == [((1, 6), (3, 5), 11), ((10, 0), (12, 1), 14), \
    ((0, 1), (3, 9), 16), ((5, 5), (6, 1), 15), ((10, 11), (18, 0), 16), \
    ((2, 6), (3, 6), 9), ((3, 4), (13, 11), 11), ((3, 5), (7, 0), 25),\
    ((3, 9), (3, 11), 18)]

# class Test_journey_class:
def test_passenger_get_on_off_bus_stop_name():
    route = Route("route.csv")
    passengers = read_passengers("passenger.csv") 
    passenger = ((0, 1), (3, 9), 16)
    journey = Journey(route,passengers)
    assert journey.passenger_get_on_off_bus_stop_name(passenger) == ('G', 'A')

def test_passenger_walk_distance_to_from_bus_stop():
    route = Route("route.csv")
    passengers = read_passengers("passenger.csv") 
    passenger = ((0, 1), (3, 9), 16)
    journey = Journey(route,passengers)
    assert journey.passenger_walk_distance_to_from_bus_stop(passenger) == (1.0, 6.324555320336759)
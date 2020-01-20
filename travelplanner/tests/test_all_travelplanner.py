from travelplanner.all_classes_travelplanner import (Journey, read_passengers,
                                                     Route, Passenger,
                                                     passengers_list)
import pytest
import numpy as np
from pathlib import Path
import yaml
import os

TEST_DIR = Path(__file__).parent


class Test_passenger_class:

    def read_fixture():
        with open(os.path.join(os.path.dirname(__file__),
                               'fixture_data.yaml')) as fixtures_file:
            fixtures = yaml.safe_load(fixtures_file)
        return fixtures

    @pytest.mark.parametrize("fixture", read_fixture())
    def test_passenger_return_values(self, fixture):
        start = fixture.pop('start')
        end = fixture.pop('end')
        speed = fixture.pop('speed')
        start_toup = tuple(map(int, start.split(' ')))
        end_toup = tuple(map(int, end.split(' ')))
        passenger = Passenger(start_toup, end_toup, speed)
        assert passenger.return_values() == (start_toup, end_toup, speed)

    @pytest.mark.parametrize(
        'start, end, speed', [
            (('one', 2), (3, 4), 5),
            ((6, 7), ('eight', 9), 10),
            ((-11, 12), (13, 14), '-fifteen')
        ]
    )
    def test_Passenger_return_values_type_error(self, start, end, speed):
        with pytest.raises(Exception):
            Passenger(start_str, end_str, speed_str).return_values()

    @pytest.mark.parametrize(
        'start, end, speed', [
            ((1, 2), (3, 4), 5),
            ((6, 7), (8, 9), 10),
            ((-11, 12), (13, 14), -15),
        ]
    )
    def test_walk_time(self, start, end, speed):
        passenger = Passenger(start, end, speed)
        calc = np.sqrt((start[0]-end[0])**2 + (start[1]-end[1])**2) * speed
        assert passenger.walk_time() == calc


class Test_route_class:

    @pytest.mark.parametrize(
        'route,expectation', [
            ("rt1.csv", [(5, 1, 'A'), (5, 2, 0), (5, 3, 'B'), (5, 4, 'C')]),
            ("rt2.csv", [(10, 8, 'A'), (10, 7, 'B'), (10, 6, 'C')]),
            ("rt3.csv", [(6, 10, 'A'), (7, 10, 'B'), (8, 10, 'C')])
        ]
    )
    def test_read_route(self, route, expectation):
        self.route = Route(TEST_DIR / route)
        assert self.route.read_route() == expectation

    @pytest.mark.parametrize(
        'route', [
            ([(9, 'B', 'A'), (9, 8, 0), (9, 9, 0), (9, 10, 'B')]),
            ([(9, 7, 'A'), (9, 'D', 0), (9, 9, 0), (9, 10, 'B')]),
            ([(9, 7, 'A'), (9, 8, 0), (9, 9, 0), (9, 10, 1)])
        ]
    )
    def test_plot_map(self, route):
        with pytest.raises(Exception):
            Route(route).plot_map()

    @pytest.mark.parametrize(
        'route', [
            ([(9, 'B', 'A'), (9, 8, 0), (9, 9, 0), (9, 10, 'B')]),
            ([(9, 7, 'A'), (9, 'D', 0), (9, 9, 0), (9, 10, 'B')]),
            ([(9, 7, 'A'), (9, 8, 0), (9, 9, 0), (9, 10, 1)])
        ]
    )
    def test_timetable_speed(self, route):
        with pytest.raises(Exception):
            Route(route).timetable('A')

    # need to somehow paramatrie these ones
    def test_timetable(self):
        route = Route(TEST_DIR / "rt1.csv")
        t_tab = {'A': 0, 'B': 20, 'C': 30}
        assert route.timetable() == t_tab

    @pytest.mark.parametrize(
        'route,expectation', [
            ("testroute.csv", [6, 6, 6]),
            ("testroute2.csv", [2, 2, 4, 4]),
            ("testroute3.csv", [0, 0, 0, 0, 2, 4, 4])
            ]
    )
    def test_route_cc(self, route, expectation):
        route = Route(TEST_DIR / route)
        assert route.route_cc() == expectation

    @pytest.mark.parametrize(
        'route', [
            ("testroute4.csv"),
            ("testroute5.csv"),
            ("testroute6.csv"),
            ]
    )
    def test_return_route(self, route):
        with pytest.raises(Exception):
            bus_route = Route(TEST_DIR / route)
            bus_route.return_route()


@pytest.mark.parametrize(
    'passenger, expected', [
        ("tp1.csv", [((6, 11), (18, 0), 9), ((1, 1), (3, 0), 22)]),
        ("tp2.csv", [((1, 5), (1, 28), 25), ((9, 10), (11, 10), 19)]),
        ("tp3.csv", [((8, 3), (8, 3), 25), ((20, 7), (0, 0), 10)])
    ]
)
def test_read_route(passenger, expected):
    passengers = read_passengers(TEST_DIR / passenger)
    assert passengers == expected


class Test_journey_class:

    @pytest.mark.parametrize(
        'passenger', [
            (('one', 2), (3, 4), 5),
            ((6, 7), ('eight', 9), 10),
            ((-11, 12), (13, 14), '-fifteen')
        ]
    )
    def test_passenger_trip(self, passenger):
        with pytest.raises(Exception):
            route = Route(TEST_DIR / "route.csv")
            passengers = read_passengers(TEST_DIR / "passenger.csv")
            passengers_ls = passengers_list(passengers)
            journey = Journey(route, passengers_ls)
            journey.passenger_trip(passenger)

    @pytest.mark.parametrize(
        'passenger, expected', [
            (((0, 1), (3, 9), 16), ('G', 'A')),
            (((3, 4), (13, 11), 11), ('F', 'B')),
            (((3, 9), (3, 11), 18), ('F', 'A'))
        ]
    )
    def test_passenger_get_on_off_bus_stop_name(self, passenger, expected):
        route = Route(TEST_DIR / "route.csv")
        passengers = read_passengers(TEST_DIR / "passenger.csv")
        passengers_ls = passengers_list(passengers)
        journey = Journey(route, passengers_ls)
        get_on_bus = journey.passenger_trip_time(passenger)[2]
        get_off_bus = journey.passenger_trip_time(passenger)[3]
        assert (get_on_bus, get_off_bus) == expected

    @pytest.mark.parametrize(
        'passenger, expected', [
            (((0, 1), (3, 9), 16), (1.0, 6.324555320336759)),
            (((3, 4), (13, 11), 11), (2.23606797749979, 3.605551275463989)),
            (((3, 9), (3, 11), 18), (6.324555320336759, 7.211102550927978))
        ]
    )
    def test_passenger_walk_bus_stop(self, passenger, expected):
        route = Route(TEST_DIR / "route.csv")
        passengers = read_passengers(TEST_DIR / "passenger.csv")
        passengers_ls = passengers_list(passengers)
        journey = Journey(route, passengers_ls)
        assert journey.passenger_walk_bus_stop(passenger) == expected

    @pytest.mark.parametrize(
        'passenger, expected', [
            (((0, 1), (3, 9), 16), 1),
            (((1, 6), (3, 5), 11), 2),
            (((10, 11), (18, 0), 16), 3),
        ]
    )
    def test_passenger_journey_allowed(self, passenger, expected):
        route = Route(TEST_DIR / "route.csv")
        passengers = read_passengers(TEST_DIR / "passenger.csv")
        passengers_ls = passengers_list(passengers)
        journey = Journey(route, passengers_ls)
        journey_allowed = journey.passenger_journey_allowed(passenger)
        assert journey_allowed == expected

    @pytest.mark.parametrize(
        'route, passengers, expected', [
            ("rt2.csv", "tp1.csv", {'A': 1, 'B': 0, 'C': -1}),
            ("rt2.csv", "tp3.csv", {'A': 0, 'B': 1, 'C': -1}),
            ("rt3.csv", "tp1.csv", {'A': 1, 'B': 0, 'C': -1})
        ]
    )
    def test_plot_bus_load(self, route, passengers, expected):
        route = Route(TEST_DIR / route)
        passengers = read_passengers(TEST_DIR / passengers)
        passengers_ls = passengers_list(passengers)
        journey = Journey(route, passengers_ls)
        bus_plot_load = journey.plot_bus_load(isTesting=1)
        assert bus_plot_load == expected

    @pytest.mark.parametrize(
        'passenger, expected', [
            (((0, 1), (3, 9), 16), [-260, 117.19, 'G', 'A', 1.0, 6.32]),
            (((1, 6), (3, 5), 11), [0, 64.11, 'F', 'F', 3.0, 2.83]),
            (((10, 11), (18, 0), 16), [60, 187.30, 'B', 'D', 3.16, 8.54])
        ]
    )
    def test_passenger_trip_time(self, passenger, expected):
        route = Route(TEST_DIR / "route.csv")
        passengers = read_passengers(TEST_DIR / "passenger.csv")
        passengers_ls = passengers_list(passengers)
        journey = Journey(route, passengers_ls)
        pass_trip_time = journey.passenger_trip_time(passenger, isTesting=1)
        assert pass_trip_time == expected

    @pytest.mark.parametrize(
        'pass_id, expected', [
            (0, {'bus': 0, 'walk': 24.596747752497688}),
            (1, {'bus': 0, 'walk': 31.304951684997057}),
            (2, {'bus': 0, 'walk': 136.7040599250805})
        ]
    )
    def test_travel_time(self, pass_id, expected):
        route = Route(TEST_DIR / "route.csv")
        passengers = read_passengers(TEST_DIR / "passenger.csv")
        passengers_ls = passengers_list(passengers)
        journey = Journey(route, passengers_ls)
        travel_time = journey.travel_time(pass_id)
        assert travel_time == expected

    @pytest.mark.parametrize(
        'route, passengers, expected', [
            ("testroute.csv", "tpassenger.csv", ("Average time on the bus:"
                                                 "0.00 minutes."
                                                 "\nAverage time walking:"
                                                 "84.23 minutes.")),
            ("testroute2.csv", "tpassenger2.csv", ("Average time on the bus:"
                                                   "8.00 minutes."
                                                   "\nAverage time walking:"
                                                   " 208.34 minutes.")),
            ("testroute3.csv", "tpassenger3.csv", ("Average time on the bus:"
                                                   "0.00 minutes."
                                                   "\nAverage time walking:"
                                                   "109.11 minutes."))
        ]
    )
    def test_print_time_stats(self, route, passengers, expected):
        route = Route(TEST_DIR / route)
        passengers = read_passengers(TEST_DIR / passengers)
        passengers_ls = passengers_list(passengers)
        journey = Journey(route, passengers_ls)
        assert journey.print_time_stats() == print(expected)

    @pytest.mark.parametrize(
        'pass_id, expected', [
            (0, ("Trip for passenger: 0\nThe bus route does not suit your"
                 "journey.\nIt will be better if you walked.\nThe total time"
                 "of travel if you walked is:24.60 minutes.")),
            (1, ("Trip for passenger: 1\nThe bus route does not suit your"
                 "journey.\nIt will be better if you walked.\nThe total time"
                 "of travel if you walked is:31.30 minutes.")),
            (2, ("Trip for passenger: 2\nThe bus does not travel in the"
                 "direction,of your destination.\nIt will be better if you"
                 "walked.\nThe total time of the journey if you walked is:"
                 "136.70 minutes."))
        ]
    )
    def test_recommended_route_for_passenger(self, pass_id, expected):
        route = Route(TEST_DIR / "route.csv")
        passengers = read_passengers(TEST_DIR / "passenger.csv")
        passengers_ls = passengers_list(passengers)
        journey = Journey(route, passengers_ls)
        route_for_passenger = journey.recommended_route_for_passenger(pass_id)
        assert print(route_for_passenger) == print(expected)

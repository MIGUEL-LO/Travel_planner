from route_class import Route
import pytest
# might turn into a class and find a method to create multiple tests with varibles
# the values used to assert the functions are manually put in, might need to use
# an automated form
#can i parametrize

class Test_route_class:

    def test_read_route(self):
        route = Route("route.csv")
        assert route.read_route() == [(9, 7, 'A'), (9, 8, 0), (9, 9, 0), (9, 10, 0), \
        (10, 10, 0), (11, 10, 0), (11, 9, 0), (11, 8, 'B'), (11, 7, 'C'), (11, 6, 0), \
        (11, 5, 0), (11, 4, 0), (11, 3, 0), (10, 3, 'D'), (9, 3, 0), (8, 3, 0), (7, 3, 'E'), \
        (6, 3, 0), (5, 3, 0), (4, 3, 0), (3, 3, 0), (2, 3, 0), (1, 3, 'F'), (0, 3, 0),\
        (0, 2, 0), (0, 1, 0), (0, 0, 'G')]


    @pytest.mark.parametrize(
        'route', [
            ([(9, 'B', 'A'), (9, 8, 0), (9, 9, 0), (9, 10, 'B')]),
            ([(9, 7, 'A'), (9, 'D', 0), (9, 9, 0), (9, 10, 'B')]),
            ([(9, 7, 'A'), (9, 8, 0), (9, 9, 0), (9, 10, 1)])
        ]
    )
    def test_plot_map(self,route):
        with pytest.raises(Exception):
            Route(route).plot_map(route)


    @pytest.mark.parametrize(
        'route', [
            ([(9, 'B', 'A'), (9, 8, 0), (9, 9, 0), (9, 10, 'B')]),
            ([(9, 7, 'A'), (9, 'D', 0), (9, 9, 0), (9, 10, 'B')]),
            ([(9, 7, 'A'), (9, 8, 0), (9, 9, 0), (9, 10, 1)])
        ]
    )
    def test_timetable_speed(self,route):
        with pytest.raises(Exception):
            Route(route).timetable('A')

    # need to somehow paramatrie these ones
    def test_timetable(self):
        route = Route("route.csv")
        assert route.timetable() == {'A': 0, 'B': 70, 'C': 80, 'D': 130, 'E': 160, 'F': 220, 'G': 260}


    def test_route_cc(self):
        route = Route("route.csv")
        assert route.route_cc() == [6, 6, 6, 0, 0, 2, 2, 2, 2, 2, 2, 2, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 2, 2, 2]


    def test_check_error_no_diag(self):
        route = Route("route.csv")
        assert route.check_error() == 0


    @pytest.mark.parametrize(
        'route', [
            ([(9, 7, 'A'), (10, 8, 0), (9, 9, 0), (9, 10, 'B')]),
            ([(9, 7, 'A'), (9, 8, 0), (10, 9, 0), (9, 10, 1)]),
            ([(9, 7, 'A'), (9, 8, 0), (9, 9, 0), (10, 10, 'B')])
        ]
    )
    def test_check_error_diag(self,route):
        assert Route(route).check_error(route) == 1
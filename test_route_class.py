from route_class import Route
import pytest
# might turn into a class and find a method to create multiple tests with varibles
# the values used to assert the functions are manually put in, might need to use
# an automated form
#can i parametrize

class Test_route_class:

    @pytest.mark.parametrize(
        'route,expectation', [
            ("testroute.csv",[(5, 1, 'A'), (5, 2, 0), (5, 3, 'B'), (5, 4, 'C')]),
            ("testroute2.csv",[(10, 8, 'A'), (10, 7, 'B'), (10, 6, 'C'), (9, 6, 'D'), (8, 6, 0)]),
            ("testroute3.csv",[(6, 10, 'A'), (7, 10, 'B'), (8, 10, 'C'),(9, 10, 'D'), (10, 10, 0),
                                (10, 9, 0), (9, 9, 0),(8, 9, 'E')])
        ]
    )
    def test_read_route(self,route,expectation):
        self.route = Route(route)
        assert self.route.read_route() == expectation   


    @pytest.mark.parametrize(
        'route', [
            ([(9, 'B', 'A'), (9, 8, 0), (9, 9, 0), (9, 10, 'B')]),
            ([(9, 7, 'A'), (9, 'D', 0), (9, 9, 0), (9, 10, 'B')]),
            ([(9, 7, 'A'), (9, 8, 0), (9, 9, 0), (9, 10, 1)])
        ]
    )
    def test_plot_map(self,route):
        with pytest.raises(Exception):
            Route(route).plot_map()


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

    @pytest.mark.parametrize(
        'route,expectation', [
            ("testroute.csv",[6, 6, 6]),
            ("testroute2.csv",[2, 2, 4, 4]),
            ("testroute3.csv",[0, 0, 0, 0, 2, 4, 4])
            ]
    )
    def test_route_cc(self,route,expectation):
        route = Route(route)
        assert route.route_cc() == expectation

    @pytest.mark.parametrize(
        'route,expectation', [
            ("testroute.csv",0),
            ("testroute2.csv",0),
            ("testroute3.csv",0),
            ([(9, 7, 'A'), (10, 8, 0), (9, 9, 0), (9, 10, 'B')],1),
            ([(9, 7, 'A'), (9, 8, 0), (10, 9, 0), (9, 10, 1)],1),
            ([(9, 7, 'A'), (9, 8, 0), (9, 9, 0), (10, 10, 'B')],1)
            ]
    )
    def test_check_error(self, route, expectation):
        route = Route(route)
        assert route.check_error() == expectation

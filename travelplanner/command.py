from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from travelplanner.all_classes_travelplanner import (Journey, read_passengers,
                                                     Route, Passenger,
                                                     passengers_list)


def process():
    parser = ArgumentParser(description=("Finds the best route option for a"
                            "passenger."),
                            formatter_class=ArgumentDefaultsHelpFormatter)

    parser.add_argument('route_file', default="route.csv",
                        help="Input CSV file with the route of the bus.")

    parser.add_argument('passengers_file', default="passenger.csv",
                        help=("Input CSV file with the passengers journey"
                              "details."))

    parser.add_argument('--bus_speed', '-s', type=int, default=10,
                        help="Speed of the bus.")

    parser.add_argument('--saveplots', '-sps', default=None,
                        action="store_true",
                        help="Saving the plots of bus load.")

    arguments = parser.parse_args()
    route = Route(route=arguments.route_file, bus_speed=arguments.bus_speed)
    passengers = read_passengers(arguments.passengers_file)
    timetable = route.timetable()
    passengers_ls = passengers_list(passengers)
    journey = Journey(route, passengers_ls)
    save_bus_map = route.plot_map(save_plot=arguments.saveplots)
    save_bus_load = journey.plot_bus_load(save_plot=arguments.saveplots)

    return 0

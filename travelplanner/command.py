from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from travelplanner.all_classes_travelplanner import (Journey, read_passengers,
                                                     Route, Passenger,
                                                     passengers_list)


def process():
    parser = ArgumentParser(description=("Finds the best route option for a"
                            "passenger."),
                            formatter_class=ArgumentDefaultsHelpFormatter)

    parser.add_argument('routefile',
                        help="Input CSV file with the route of the bus.")

    parser.add_argument('passfile',
                        help=("Input CSV file with the passengers journey"
                              "details."))

    parser.add_argument('--speed', '-s', type=int, default=10,
                        help="Speed of the bus.")

    parser.add_argument('--saveplots', '-sps', default=None,
                        action="store_true",
                        help="Saving the plots of bus load.")

    arguments = parser.parse_args()
    route_ins = Route(route=arguments.routefile, bus_speed=arguments.speed)
    passengers = read_passengers(arguments.passfile)
    timetable = route_ins.timetable()
    passengers_ls = passengers_list(passengers)
    journey = Journey(route_ins, passengers_ls)
    save_bus_map = route_ins.plot_map(save_plot=arguments.saveplots)
    save_bus_load = journey.plot_bus_load(save_plot=arguments.saveplots)
    print(timetable)
    for i in range(len(passengers_ls)):
        print(journey.recommended_route_for_passenger(i))

    return 0

# mphy0021-2019-travel-planner-MIGUEL-LO
# A Travel Planner Package

This is a library that calculates travel paths and times for a set of passengers for a given bus route timetable.

## Installation

Browse to the directory where this file lives, and run:
```bash
pip install .
```
That command will download any dependencies we have


## Usage

You can use the package in the following way, this will output most of the desired outputs relavent to the problem.


```python
from travelplanner import (Journey, read_passengers,
                           Route, Passenger, 
                           passengers_list)


route = Route("route.csv")
passengers = read_passengers("passenger.csv")
passengers_list = passengers_list(passengers)
# or
# passengers_list = [Passenger(start,end,speed) for start, end, speed in passengers]
journey = Journey(route,passengers_list)
for i in range(len(passengers_list)):
    print(journey.travel_time(i))
journey.print_time_stats()
for i in range(len(passengers_list)):
    print(journey.recommended_route_for_passenger(i))
journey.plot_bus_load(save_plot=1)
route.plot_map(save_plot=1)
```

Or alternativaly you can run it from the terminal as:

```bash
$ bussimula routefile passfile --speed 5 [--saveplots]
```

## Contributing

We accept contributions via GitHub!!

To install the development version, clone this repository and install it on 
a virtual environment

```bash
git clone https://github.com/UCL/mphy0021-2019-travel-planner-MIGUEL-LO.git
conda create -n travelplanner python=3.7
conda activate travelplanner
cd mphy0021-2019-travel-planner-MIGUEL-LO
pip install -e .
... code code code ...
conda deactivate
```
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Route:
    def __init__(self, route):
        self.route = route
    
    
    def read_route(self):
        '''
         This reads the bus route csv file and returns a list containing touples 
         with the route of the bus and the name of the bus stops.    
        '''
        df = pd.read_csv(self.route, names=['x1','y1','stop'])
        df.fillna(0,inplace=True)
        # Make collapsed columns for positional dat
        df['x1, y1, stop'] = list(zip(df['x1'],df['y1'],df['stop']))
        # Make output list
        data_out = [(df.iloc[i]['x1, y1, stop']) for i in range(len(df))]
        
        return data_out    
    
    
    def plot_map(self, route_input=None):
        if route_input:
            route = route_input
        else:
            route = self.read_route()

        max_x = max([n[0] for n in route]) + 5 # adds padding
        max_y = max([n[1] for n in route]) + 5
        grid = np.zeros((max_y, max_x))
        for x,y,stop in route:
            if type(x) == str:
                raise Exception('The bus journey x coordinate should not be a letter but a number.'
                            'The value of x was: {}'.format(x))
            elif type(y) == str:
                raise Exception('The bus journey y coordinate should not be a letter but a number.'
                            'The value of y was: {}'.format(y))
            elif type(stop) != str and stop != 0:
                raise Exception('The bus journey bus stop should not be a number but a letter.'
                            'The value of x was: {}'.format(stop))
            grid[y, x] = 1
            if stop:
                grid[y, x] += 1
        fig, ax = plt.subplots(1, 1)
        ax.pcolor(grid)
        ax.invert_yaxis()
        ax.set_aspect('equal', 'datalim')
        plt.show()
        

    # stops is a dictionary holding the bus stop name and time of arrival. 
    # starting from 0 at stop A and taking 10 mins to reach checkpoints in  
    # the travel of bus
    def timetable(self,bus_speed=10,route_input=None):
        self.bus_speed = bus_speed
        '''
        Generates a timetable for a route as minutes from its first stop.
        With a user defined bus_speed otherwise default bus_speed = 10
        '''
        if type(self.bus_speed) == str:
            raise Exception('The speed of the bus should not be a letter but a number.'
                            'The value of bus_speed was: {}'.format(self.bus_speed))
        # stops is a dictionary holding the bus stop name and time of arrival. 
        # starting from 0 at stop A and taking 10 mins to reach checkpoints in  
        # the travel of bus.
        # can potentially change the speed
        if route_input:
            route = route_input
        else:
            route = self.read_route()
        time = 0
        stops = {}
        for step in route:
            if step[2]:
                stops[step[2]] = time
            time += bus_speed
            
        return stops
    
    
    def route_cc(self,route_input=None):
        '''
        Converts a set of route into a Freeman chain code
        3 2 1
        \ | /
        4 - C - 0
        / | \
        5 6 7
        '''
        # starting cord of bus route
        # Choosing bus stop A and giving (x,y) cord for it 
        if route_input:
            route = route_input
        else:
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
        freeman_coord2cc = {val: key for key,val in freeman_cc2coord.items()}
        for b, a in zip(route[1:], route):
            x_step = b[0] - a[0]
            y_step = b[1] - a[1]
            cc.append(int(freeman_coord2cc[(x_step, y_step)]))

        return cc
    
    
    def check_error(self,route_input=None):
        '''
        The bus is not allowed to move diagonally. This function checks wether the bus moves diagonally.
        To then use the result from this function to either allow the input passenger route or not.
        If the return value is > 0 then there is a diagonal movement, otherwise there isn't and the 
        route is valid.
        '''
        if route_input:
            route = route_input
            route_cc = self.route_cc(route)
        else:
            route = self.read_route()
            route_cc = self.route_cc()

        is_odd = 0
        for cc_number in route_cc:
            if cc_number % 2 != 0:
                is_odd += 1 
        
        if is_odd > 0:
            
            return 1
        else:
            
            return 0


if __name__ == "__main__":
    obj = Route("route.csv")
    print("This is the route of the bus =", obj.read_route())
    print("This is the timetable of the bus =",obj.timetable())
    obj.plot_map()
    cc = obj.route_cc()
    print((f"The bus route is described by this chain code:\n{cc}"))
    print(obj.check_error())
import pandas as pd
import numpy as np
from IPython.display import display
import matplotlib.pyplot as plt

class Route:
    def __init__(self, filename):
        self.filename = filename
    
    def read_route(self):
        df = pd.read_csv(self.filename, names=['x1','y1','stop'])
        # Fill nan values with 0
        df.fillna(0,inplace=True)       
        # Make collapsed columns for positional dat
        df['x1, y1, stop'] = list(zip(df['x1'],df['y1'],df['stop']))
        # Make output list
        data_out = [(df.iloc[i]['x1, y1, stop']) for i in range(len(df))]
        return data_out

    def plot_map(self):
        route = self.read_route()
        max_x = max([n[0] for n in route]) + 5 # adds padding
        max_y = max([n[1] for n in route]) + 5
        grid = np.zeros((max_y, max_x))
        for x,y,stop in route:
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
    def timetable(self):
        '''
        Generates a timetable for a route as minutes from its first stop.
        '''
        route1 = self.read_route()
        time = 0
        stops = {}
        for step in route1:
            if step[2]:
                stops[step[2]] = time
            time += 10
        return stops

if __name__ == "__main__":
    obj = Route("route.csv")
    print("This is the route of the bus =", obj.read_route())
    print("This is the timetable of the bus =",obj.timetable())
    print(obj.plot_map())

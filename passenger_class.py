import pandas as pd
import numpy as np
from IPython.display import display

class Passenger:
    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0
    speed = 0
    time = 0
    # Not sure where to put passenger reading function
    def __init__(self, start, end, speed):# filename):
        self.x1 , self.y1 = start
        self.x2 , self.y2 = end
        self.speed = speed
#         self.filename = filename
    def walk_time(self):
        self.time = np.sqrt((self.x2-self.x1)**2
                       + (self.y2-self.y1)**2) * self.speed
        print(f"The amount of time the passenger will walk for to get from starting location {self.x1 , self.y1},"
              f" to the end location {self.x2 , self.y2},"
              f" with speed {self.speed} is : {self.time :3.2f} minutes")
    def display(self):
        print(f"start =  {self.x1 , self.y1}")
        print(f"end =  {self.x2 , self.y2}")
        print(f"speed =  {self.speed}")
        
#     def read_passengers(self):
#         df = pd.read_csv(self.filename, names=['x1','y1','x2','y2','speed'])
#         # Make collapsed columns for positional dat
#         df['x1, y1'] = list(zip(df['x1'],df['y1']))
#         df['x2, y2'] = list(zip(df['x2'],df['y2']))
#         # Make output list
#         data_out = [(df.iloc[i]['x1, y1'], df.iloc[i]['x2, y2']
#                     ,(df.iloc[i]['speed'])) for i in range(len(df))]
#         return data_out
if __name__ == "__main__":
    obj = Passenger((1,2),(3,4),5)#,"passenger.csv")
    print(obj.display())
    print(obj.walk_time())
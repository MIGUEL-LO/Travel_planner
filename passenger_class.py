import pandas as pd
import numpy as np
from IPython.display import display
# class MysteryError(Exception):
#     pass

class Passenger:
    def __init__(self, start, end, speed):
        self.x1, self.y1 = start
        self.x2, self.y2 = end
        self.speed = speed
    def walk_time(self):
        '''
        Calculates the time it would take a passenger to reach the final destination
        from their starting location.
        '''
        self.time = np.sqrt((self.x2-self.x1)**2
                           + (self.y2-self.y1)**2) * self.speed

        return self.time
    
    def return_values(self):
        # if type(self.x1) or type(self.x2) or type(self.y1) or type(self.y2) or type(self.speed) == str:
        if type(self.x1) == str:
            raise Exception
        elif type(self.x2) == str:
            raise Exception
        elif type(self.y1) == str:
            raise Exception
        elif type(self.y2) == str:
            raise Exception
        elif type(self.speed) == str:
            raise Exception
        
        return((self.x1, self.y1), (self.x2, self.y2), self.speed)


if __name__ == "__main__":
    obj = Passenger((1,2),(3,4),5)
    print(obj.walk_time())
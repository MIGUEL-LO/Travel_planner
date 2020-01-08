import pandas as pd
import numpy as np


class Passenger:
    def __init__(self, start, end, speed):
        self.x1, self.y1 = start
        self.x2, self.y2 = end
        self.speed = speed

        if type(self.x1) == str:
            raise Exception('x_1 coordinate should not be a letter but a number.'
                            'The value of x_1 was: {}'.format(self.x1))
        elif type(self.x2) == str:
            raise Exception('x_2 coordinate should not be a letter but a number.'
                            'The value of x_2 was: {}'.format(self.x2))
        elif type(self.y1) == str:
            raise Exception('y_1 coordinate should not be a letter but a number.'
                            'The value of y_1 was: {}'.format(self.y1))
        elif type(self.y2) == str:
            raise Exception('y_2 coordinate should not be a letter but a number.'
                            'The value of y_2 was: {}'.format(self.y2))
        elif type(self.speed) == str:
            raise Exception('speed should not be a letter but a number.'
                            'The value of speed was: {}'.format(self.speed))
        
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

        return((self.x1, self.y1), (self.x2, self.y2), self.speed)


if __name__ == "__main__":
    obj = Passenger((1,2),(3,4),5)
    new_obj = Passenger((1,'one'),(3,4),5)
    print(obj.walk_time())
    print(new_obj.walk_time())
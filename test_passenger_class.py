from passenger_class import Passenger
import numpy as np
import pytest

class Test_passenger_class:

    @pytest.mark.parametrize(
        'start, end, speed', [
            ((1,2),(3,4),5),
            ((6,7),(8,9),10),
            ((-11,12),(13,14),-15),
        ]
    ) 
    def test_Passenger_return_values(self,start, end, speed):
        passenger = Passenger(start, end, speed)
        assert passenger.return_values() == (start, end, speed)

    @pytest.mark.parametrize(
        'start_str, end_str, speed_str', [
            (('one',2),(3,4),5),
            ((6,7),('eight',9),10),
            ((-11,12),(13,14),'-fifteen')
        ]
    )
    def test_Passenger_return_values_type_error(self,start_str, end_str, speed_str):
        with pytest.raises(Exception):
            Passenger(start_str, end_str, speed_str).return_values()
            
    @pytest.mark.parametrize(
        'start, end, speed', [
            ((1,2),(3,4),5),
            ((6,7),(8,9),10),
            ((-11,12),(13,14),-15),
        ]
    )
    def test_walk_time(self,start, end, speed):
        passenger = Passenger(start, end, speed)
        assert passenger.walk_time() ==  np.sqrt((start[0]-end[0])**2 \
                                        + (start[1]-end[1])**2) * speed

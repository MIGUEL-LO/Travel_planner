import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from passenger_class import Passenger
import pytest


def test_Passenger_return_values():
    passenger = Passenger((1,2),(3,4),5)
    assert passenger.return_values() == ((1,2),(3,4),5)

def test_Passenger_return_values_type_error():
    with pytest.raises(Exception):
        Passenger((1,2),('three',4),5).return_values()

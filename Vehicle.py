from datetime import datetime


class Vehicle(object):

    def __init__(self, vid):
        self.car_plate = vid
        self.travel_time = []

    def __str__(self):
        return self.car_plate

    def street_time(self, street, pos):
        st = {"street": street, "entry_time": datetime.now(), "entry_pos": pos}
        self.travel_time.append(st)

    def get_last_street_entry(self):
        return self.travel_time[-1]['entry_time'], self.travel_time[-1]['entry_pos']


def print_usage():
    """Print a guide on how to use the program."""
    print("USAGE: python [3] traffic.py [-b B] [-c C] [-t T]")
    print("where:")
    print("-b: sets the probability of braking. It should be")
    print("a number between 0 and 1.")
    print("-c: sets the collision probability. It should be")
    print("a number between 0 and 1.")
    print("-t: set the number of iterations to perform")
    print("the simulation.")

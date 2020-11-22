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

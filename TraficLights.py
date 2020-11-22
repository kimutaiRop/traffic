import random
from datetime import datetime, timedelta


class Lights:
    def __init__(self):
        self.road = None
        self.side = None
        self.color = 'orange'
        self.last_change = datetime.now()
        self.exp_time = 0.2

    def change_color(self, color="orange"):
        time = random.random()
        if color == "orange":
            time = 0.8
        elif color == "green":
            time = 1 + time  # will be changed by model
        elif color == "red":
            time = 1 + time
        else:
            print('[ERROR] color not recognized')

        self.count_down(time)

    def get_color(self):
        return self.color

    def count_down(self, time_):
        if self.color == "orange":
            if (datetime.now() - self.last_change) >= timedelta(seconds=self.exp_time):
                self.color = "green"
        elif self.color == "red":
            if (datetime.now() - self.last_change) >= timedelta(seconds=self.exp_time):
                self.color = "orange"
        elif self.color == "green":
            if (datetime.now() - self.last_change) >= timedelta(seconds=self.exp_time):
                self.color = "red"
        else:
            print('[ERROR] color not recognized')

        if (datetime.now() - self.last_change) >= timedelta(seconds=self.exp_time):
            self.exp_time = time_
            self.last_change = datetime.now()

    def start_traffic(self):
        self.change_color('orange')

    def update_light(self):
        if (datetime.now() - self.last_change) >= timedelta(seconds=self.exp_time):
            if self.color == "orange":
                self.change_color("green")
            elif self.color == "red":
                self.change_color("orange")
            elif self.color == "green":
                self.change_color("red")

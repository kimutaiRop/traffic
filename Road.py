import random
from datetime import datetime

from data_maker import car_data_maker
from trafic_controler import *

roads = [{
    "id": 1,  # id of the road
    "name": "moi av",  # ane  of the road
    "prob": [0.2, 0.3, 0.3, 0.2],  # probabilities of the (entering) key happening
    "entering": [3, 4, 0, -1],  # eg. (entering road id 3 or 4, 0-exiting the city traffic, 1- being packed)
    # directly from this street
    'side': [0, 1]  # from which side does the cars join entry roads (1-> right, 0-> left)
},
    {
        "id": 2,
        "name": "tom mb",
        "prob": [0.2, 0.3, 0.25, 0.25],
        "entering": [3, 1, 0, -1],
        'side': [1, 0]
    },
    {
        "id": 3,
        "name": "ronald",
        "prob": [0.2, 0.3, 0.3, 0.2],
        "entering": [2, 1, 0, -1],
        'side': [1, 0]
    },
    {
        "id": 4,
        "name": "uni way",
        "prob": [0.2, 0.2, 0.2, 0.4],
        "entering": [2, 1, 0, -1],
        'side': [1, 0]
    }
]

ROADS = []


class Road:
    def __init__(self, id_):
        self.cars_left = []
        self.cars_right = []
        self.road = roads[id_ - 1]
        self.lights = {
            "left": None,
            "right": None
        }
        self.stopping = []

    def __str__(self):
        return self.road['name']

    def set_light(self, key_, val):
        self.lights[key_] = val

    def add_car(self, car, position):
        ls = []
        if position == "left":
            ls = self.cars_left
        elif position == "right":
            ls = self.cars_right
        ls.append(car)
        return ls

    def assign_direction(self, car, pos):
        ls = self.add_car(car, pos)
        car.street_time(self, len(ls))
        # print(f"[MOVE] CAR {car} to road {road}-{pos}")

    def get_num(self, position):
        ls = 0
        if position == "left":
            ls = len(self.cars_left)
        elif position == "right":
            ls = len(self.cars_right)
        return ls

    def get_light(self, side):
        light = getattr(self, 'lights')
        return light[side]

    def get_road(self):
        return self.road

    def update_street_cars(self, remove, side):
        moved = []
        if side == "left":
            moved = self.cars_left[:remove]
            self.cars_left = self.cars_left[remove:]

        elif side == "right":
            moved = self.cars_right[:remove]
            self.cars_right = self.cars_right[remove:]

        for car in moved:
            road = random.choices(self.road['entering'],
                                  self.road['prob'], k=1)[0]
            data = {
                'car': car,
                'street': self.road['name'],
                'side': side,
                'entry_pos': car.get_last_street_entry()[1],
                'entry_time': car.get_last_street_entry()[0],
                'num_cars_current_street': self.get_num(side),
                'exit_time': datetime.now(),
                'num_cars_next_street': None,
                'next_road': "",
                'next_road_light': None,
            }
            if road > 0:
                next_road = get_next_road(self, side)
                next_road = ROADS[next_road]
                next_road_light = check_road_join(next_road, side)
                next_road.assign_direction(car, side)
                data['num_cars_next_street'] = next_road.get_num(side)
                data['next_road'] = next_road
                data['next_road_light']: next_road_light
            else:
                if road == 0:
                    pass
                else:
                    self.stopping.append(car)
            car_data_maker(data)

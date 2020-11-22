import random
import threading
import time
from datetime import datetime, timedelta
from queue import Queue

import pandas as pd
from IPython.display import clear_output
from termcolor import colored

from Road import Road, ROADS
from TraficLights import Lights
from Vehicle import Vehicle
from data_maker import DATA

queue = Queue()

T_MAX = 50
VEL_MAX = 9
POS_MAX = 13
BRAKE_PROB = 0.4
COLLISION_PROB = 0.1
PLATES = [""]
FULL_DAY = 86400
PROG_TIME = 219
CAR_RATES = [0.00279, 0.03012, 0.09021, 0.002007, 0.003004]
PROGRAM_START = datetime.now()
N_VEHICLES = 8000
NUMBER_OF_THREADS = 8


def get_rate():
    el_time = datetime.now() - PROGRAM_START
    if el_time < timedelta(seconds=PROG_TIME / 5):
        rate = CAR_RATES[0]
    elif el_time < timedelta(seconds=PROG_TIME / 4):
        rate = CAR_RATES[1]
    elif el_time < timedelta(seconds=PROG_TIME / 3):
        rate = CAR_RATES[2]
    elif el_time < timedelta(seconds=PROG_TIME / 2):
        rate = CAR_RATES[3]
    else:
        rate = CAR_RATES[4]
    return rate


def create_roads():
    print("[STARTING....] creating roads")
    for i in range(0, 4):
        rd = Road(i)
        ROADS.append(rd)
        print("[CREATING] ==> creating road {}".format(rd))

        for pos in ['left', 'right']:
            lt = Lights()
            lt.start_traffic()
            rd.set_light(pos, lt)
            print(colored("[ADDED]", "green"), f" traffic light to {rd}-{pos}")

    print(colored('[DONE]', 'green'), " Roads created")


def simulate_cars():
    print(f"[TRAFFIC SIMULATION] starting...")
    for i in range(0, N_VEHICLES):
        rate = get_rate()
        plate = ""
        while plate in PLATES:
            for x in random.choices("503qwertyu89pasdfghjklzxc47vb2nm",
                                    k=3):
                plate += x
        car = Vehicle(plate)
        road = ROADS[random.randint(0, 3)]
        pos = random.choice(['left', 'right'])
        # print(f"[{i}] NEW CAR {car} for road {road}-{pos}")
        road.assign_direction(car, pos)
        time.sleep(rate)


def move_cars(street, side):
    light = street.get_light(side)
    if light.get_color() == 'green':
        street.update_street_cars(6, side)
    light.update_light()
    time.sleep(0.2)


def print_highway():
    rds = ['road | ']
    for r in ROADS:
        for side in ['left', 'right']:
            rds.append('{} {} | '.format(r, side[0]))
    format_row = "{:>12}" * (len(rds) + 1)
    print(format_row.format("", *rds))
    while True:
        traffic = [" | "]
        for r in ROADS:
            for side in ['left', 'right']:
                light = r.get_light(side)
                color = light.get_color()
                if color == "orange":
                    color = 33
                if color == "red":
                    color = 31
                else:
                    color = 32
                traffic.append("{} | ".format(r.get_num(side)))
                # traffic.append("\033[1;{}m {} | ".format(color, r.get_num(side)))
        print(format_row.format("", *traffic))
        time.sleep(0.2)


def work():
    while True:
        st = queue.get()
        move_cars(st['road'], st['side'])
        queue.task_done()


def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


def plot_graph():
    while True:
        try:
            df = pd.DataFrame(DATA)
            df.to_csv('./car_data.csv')
            # df['exit_time'] = pd.to_datetime(df['exit_time'])
            # df['entry_time'] = pd.to_datetime( df['entery_time'])
            #
            # df['total_time'] = df['exit_time'] - df['entery_time']
            # plt.plot(df['index'],df['total_time'])
            # plt.pause(0.05)
            time.sleep(3)
        except:
            pass


# Each queued link is a new job
def create_jobs():
    for road in ROADS:
        for side in ['left', 'right']:
            d = {"road": road, "side": side}
            queue.put(d)
    queue.join()
    create_jobs()


if __name__ == "__main__":
    print("TRAFFIC UPDATE")
    create_roads()
    create_workers()
    try:
        t0 = threading.Thread(target=simulate_cars)
        t1 = threading.Thread(target=create_jobs)
        t2 = threading.Thread(target=plot_graph)
        t3 = threading.Thread(target=print_highway)
        t0.start()
        t1.start()

        t2.start()
        t3.start()
    except:
        print("exiting...")

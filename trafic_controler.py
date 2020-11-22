def check_road_join(road, side):
    light = road.get_light(side)
    return light.get_color()


def get_next_road(road, side):
    if side == "left":
        side = 0
    else:
        side = 1
    join_roads = road.get_road()['entering'][:-2]
    entry_side_ind = road.get_road()
    entry_side_ind = entry_side_ind['side'].index(side)
    next_road_ind = join_roads[entry_side_ind] - 1
    return next_road_ind

from route import Route
from app import calculate_costs
MAX_DISTANCE = 100

def countSort2(houses):
    """
    Takes a list containing tuples containing the length to a battery and
    the corresponding house. Returns the same list ordered by length
    """
    count = []
    for i in range(0, MAX_DISTANCE):
        count.append([0, []])

    for tuple in houses:
        length = tuple[0]
        count[length-1][0] += 1
        count[length-1][1].append(tuple)

    for i in range(1, len(count)):
        count[i][0] += count[i - 1][0]

    sorted = []

    for i in range(1, len(count)):
        if count[i][0] != count[i-1][0]:
            for house in count[i][1]:
                sorted.append(house)
    return sorted

def switch(route1, route2):
    battery1 = route1.get_battery()
    battery2 = route2.get_battery()
    battery1.remove_route(route1)
    battery2.remove_route(route2)
    house1 = route1.get_house()
    house2 = route2.get_house()
    house1.add_route(battery2)
    house2.add_route(battery1)
    battery1.connect_house(house2)
    battery2.connect_house(house1)
    return (house1.get_route().get_length(), house1.get_route()), (house2.get_route().get_length(), house2.get_route())

def check_switch(route1, route2):
    battery1 = route1.get_battery()
    battery2 = route2.get_battery()
    house1 = route1.get_house()
    house2 = route2.get_house()
    length1 = route1.get_length()
    length2 = route2.get_length()
    total_length1 = length1 + length2
    route3 = Route(house2, battery1)
    route4 = Route(house1, battery2)
    length3 = route3.get_length()
    length4 = route4.get_length()
    total_length2 = length3 + length4
    change = total_length1 - total_length2
    cap_left1 = battery1.get_capacity() - battery1.get_used_cap() + house1.get_output() 
    cap_left2 = battery2.get_capacity() - battery2.get_used_cap() + house2.get_output()
    if total_length2 < total_length1 and house2.get_output() < cap_left1 and house1.get_output() < cap_left2:
        #print("cap_left1: ", cap_left1, house2.get_output(), "capleft2: ", cap_left2, house1.get_output())
        return True, change
    else:
        return False


def check_switch_cap(route_1, route_2):
    battery_2 = route_2.get_battery()
    house_1 = route_1.get_house()
    house_2 = route_2.get_house()
    difference = house_1.get_output() - house_2.get_output()
    if difference > 0:
        return (battery_2.get_used_cap() + difference) < battery_2.get_capacity()

def check_cross_houses(houses, batteries):
        count = 0
        for battery in batteries:
            count1 = 0
            for route in battery.get_routes():
                for house in houses:
                    house_coordinate = (house.get_x(), house.get_y())
                    if house_coordinate in route.get_coordinates():
                        count += 1
                        count1 += 1 
        return count
from helpers import countSort1
from route import Route


def connect_basic(batteries, houses):
    """
    Goes through each battery, adding houses if possible
    """
    houses = houses
    batteries = batteries
    connected_houses = []

    # returns true if all houses connected, false otherwise
    for battery in batteries:
        while battery.get_used_cap() < battery.get_capacity():
            cap_left = battery.get_capacity() - battery.get_used_cap()
            for house in houses:
                if house.get_output() < cap_left:
                    battery.connect_house(house)
                    connected_houses.append(house)
                    houses.remove(house)
            break
    return len(houses) == 0


def connect_greedy(batteries, houses):
    houses = houses

    for battery in batteries:
        connected_houses = []
        sorted_houses = []
        for house in houses:
            route = Route(house, battery)
            sorted_houses.append((route.get_length(), house))
        sorted_houses = countSort1(sorted_houses)

        for i in sorted_houses:
            houses = i[1]
            for house in houses:
                battery.connect_house(house)
                connected_houses.append(house)
                houses.remove(house)
    return len(houses) == 0


def connect_greedy_hillclimb(batteries, houses):
    return "TODO"


def constraint_relaxation(batteries, houses):
    """
    Connects all houses greedily, then switches everything until constraints
    are satisfied
    """
    houses = houses
    batteries = batteries
    distances = []
    for battery in batteries:
        sorted_houses = []
        for house in houses:
            route = Route(house, battery)
            sorted_houses.append((route.get_length(), house))
        sorted_houses = countSort1(sorted_houses)
        distances.append(sorted_houses)
    while len(houses) >= 0:
        i = 0
        for battery in batteries:
            closest_house = distances[i][0][1]
            print(distances)
            battery.connect_house(closest_house)
            houses.remove(closest_house)
            for d in distances:
                d.remove(closest_house)
            i += 1
    return len(houses) == 0


def new_algorithm():
    return "TODO"

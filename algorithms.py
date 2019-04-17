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
    for i in range(0, len(batteries)):
        battery = batteries[i]
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
            sorted_houses.append((route.get_length(), house ))
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


def constraint_relaxation():
    return "TODO"


def new_algorithm():
    return "TODO"

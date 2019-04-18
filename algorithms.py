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
    "TODO"


def connect_greedy_hillclimb(batteries, houses):
    "TODO"


def constraint_relaxation(batteries, houses):
    """
    Connects all houses greedily, then switches everything until constraints
    are satisfied
    """
    houses = houses
    batteries = batteries
    connected_houses = []
    for i in range(0, len(batteries)):
        battery = batteries[i]
        for house in houses:
            "Do stuff"
    for battery in batteries:
        while battery.get_used_cap > battery.get_capacity:
            
    return True


def new_algorithm():
    "TODO"

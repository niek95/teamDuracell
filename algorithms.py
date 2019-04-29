from helpers import countSort2
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
        sorted_houses = countSort2(sorted_houses)

        for i in sorted_houses:
            houses = i[1]
            for house in houses:
                battery.connect_house(house)
                connected_houses.append(house)
                houses.remove(house)
    return len(houses) == 0


def connect_greedy_hillclimb(batteries, houses):
    # List of all the connected houses
    connected_houses = []
    # List of sorted houses
    sorted_houses = []

    # Iterate over the batteries and houses
    for battery in batteries:
        for house in houses:
            route = Route(house, battery)
            sorted_houses.append((route.get_length(), house))
        sorted_houses = countSort2(sorted_houses)

        # Connect huizen random en kijk of afstand van huis naar batterij de kortste is dmv sorted2, zo ja: append aan connected_houses, anders connect nieuw huis

    return "TODO"


def constraint_relaxation(batteries, houses):
    """
    Keeps connecting the closest house and battery, then switches routes until
    constraints are satisfied
    """
    houses = houses
    batteries = batteries
    distances = []
    for battery in batteries:
        unsorted = []
        for house in houses:
            route = Route(house, battery)
            unsorted.append((route.get_length(), house))
        sorted_houses = countSort2(unsorted)
        distances.append(sorted_houses)

    while len(houses) > 0:
        closest = distances[0][0]
        id = 0
        for i in range(len(distances)):
            if distances[i][0][0] < closest[0]:
                closest = distances[i][0]
                id = i
        batteries[id].connect_house(closest[1])
        houses.remove(closest[1])
        for d in distances:
            for tuple in d:
                if tuple[1] == closest[1]:
                    d.remove(tuple)
    return len(houses) == 0


def turn_by_turn(batteries, houses):
    """
    Goes through each battery turn by turn, adding the closest house possible
    afterwards routes should be switched until constraints are satisfied
    Still have to do the last part
    """
    houses = houses
    batteries = batteries
    distances = []
    for battery in batteries:
        unsorted = []
        for house in houses:
            route = Route(house, battery)
            unsorted.append((route.get_length(), house))
        sorted_houses = countSort2(unsorted)
        distances.append(sorted_houses)

    while len(houses) > 0:
        for i in range(len(distances)):
            closest_house = distances[i][0]
            batteries[i].connect_house(closest_house[1])
            houses.remove(closest_house[1])
            for d in distances:
                for house in d:
                    if house[1] == closest_house[1]:
                        d.remove(house)
            i += 1
    return len(houses) == 0


def new_algorithm():
    return "TODO"

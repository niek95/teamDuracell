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
    """
    Goes through each battery, adding the most nearby houses if possible
    """
    houses = houses
    batteries = batteries
    counter = 0
    for house in houses:
        sorted_batteries = []
        for battery in batteries:
            route = Route(house, battery)
            cap_left = battery.get_capacity() - battery.get_used_cap()
            if house.get_output() < cap_left:
                sorted_batteries.append((route.get_length(), battery))

        sorted_batteries = countSort2(sorted_batteries)
        sorted_batteries[0][1].connect_house(house)

    return len(houses) == 150


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
    # distances contains a number of lists, one for each battery,
    # containing tuples of houses and distances to the corresponding battery
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
            # check the first element of eacht list if it is closer than the
            # previous one
            if distances[i][0][0] < closest[0]:
                closest = distances[i][0]
                id = i
        # connect the closest house
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

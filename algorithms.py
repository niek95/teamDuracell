from helpers import countSort2
from route import Route
import random
from helpers import check_switch_cap
from helpers import switch


def connect_basic(batteries, houses):
    """
    Goes through each battery, adding houses if possible
    """
    houses = houses
    batteries = batteries
    connected_houses = []

    # returns true if all houses connected, false otherwise
    for battery in batteries:
        connected_houses = []
        for house in houses:
            cap_left = battery.get_capacity() - battery.get_used_cap()
            if house.get_output() < cap_left:
                print("connecting")
                battery.connect_house(house)
                connected_houses.append(house)
        for house in connected_houses:
            houses.remove(house)
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
    return apply_constraints(batteries)


def apply_constraints(batteries):
    """
    Randomly removes routes from over capacity batteries
    until constraints are satisfied
    """
    # check which batteries are still over cap
    SWITCH_THRESHOLD = 0.05
    over_cap = []
    under_cap = []
    for battery in batteries:
        if battery.get_over_cap():
            over_cap.append(battery)
        else:
            under_cap.append(battery)
    # until constraints are satisfied, take random route from the over_cap
    # battery and try to find a place for it in an under_cap battery
    while not check_satisfied(batteries):
        for battery in over_cap:
            routes = battery.get_routes()
            house = routes[random.randrange(len(routes))].get_house()
            battery_2 = under_cap[random.randrange(len(under_cap))]
            if (battery_2.get_capacity() - battery_2.get_used_cap()) > house.get_output():
                battery.remove_route(house.get_route())
                battery_2.connect_house(house)
        # remove batteries from over_cap if they satisfy constraints
        for battery in over_cap:
            if not battery.get_over_cap():
                over_cap.remove(battery)
                under_cap.append(battery)
        if check_satisfied(batteries):
            return True
        # check if batteries are close enough to capacity to start switching
        within_range = True
        for battery in batteries:
            if (battery.get_used_cap() - battery.get_capacity()) > battery.get_capacity() * SWITCH_THRESHOLD:
                within_range = False
        if within_range is True:
            return switch_constraints(over_cap, under_cap)


def switch_constraints(over_cap, under_cap):
    # keep checking if the constraints are satisfied
    while check_satisfied(over_cap) is False:
        # pick two random routes to switch, and do so if it helps the cap
        for battery in over_cap:
            routes_1 = battery.get_routes()
            route_1 = routes_1[random.randrange(len(routes_1))]
            routes_2 = under_cap[random.randrange(len(under_cap))].get_routes()
            route_2 = routes_2[random.randrange(len(routes_2))]
            if check_switch_cap(route_1, route_2):
                switch(route_1, route_2)
    return check_satisfied(over_cap)

def check_satisfied(batteries):
    for battery in batteries:
        if battery.get_used_cap() > battery.get_capacity():
            return False
    return True


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
    apply_constraints(batteries)

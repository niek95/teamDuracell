from helpers import countSort2, switch, check_switch
from route import Route
from app import calculate_costs

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
    houses = houses
    batteries = batteries
    routes = []
    counter = 0
    for house in houses:
        sorted_batteries = []
        for battery in batteries:
            route = Route(house, battery)
            routes.append((route.get_length(), route))
            cap_left = battery.get_capacity() - battery.get_used_cap()
            if house.get_output() < cap_left:
                sorted_batteries.append((route.get_length(), battery))

        sorted_batteries = countSort2(sorted_batteries)        
        sorted_batteries[0][1].connect_house(house)
    
    sorted_routes = countSort2(routes)
    costs_before = calculate_costs(batteries)
    i = 0
    while i < 150:
        route1 = sorted_routes[len(sorted_routes) - (i + 1)][1]
        route2 = sorted_routes[i][1]
        if check_switch(route1, route2):
            sorted_routes.remove((route1.get_length(), route1))
            sorted_routes.remove((route2.get_length(), route2))
            routes1 = switch(route2, route1)
            route1 = routes1[0]
            route2 = routes1[1]
            sorted_routes.append((route1.get_length(), route1))
            sorted_routes.append((route2.get_length(), route2))
            sorted_routes = countSort2(sorted_routes)
            i = 0
        else:
            i += 1
    return len(houses) == 150


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

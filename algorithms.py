from helpers import countSort2, switch, check_switch
from route import Route
import random
from helpers import check_switch_cap, switch



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
    connected_house = []

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

def hillclimb(batteries, houses):
    # first get all the routes from the previous algorithm

    batteries = batteries
    houses = houses
    routes = []

    for battery in batteries:
        for route in battery.routes:
            routes.append((route.get_length(), route))

    # sort all those routes
    sorted_routes = countSort2(routes)
    i = 0
    changed = 0
    # keep going through the whole list of routes untill the end
    while i < len(sorted_routes):
        route1 = sorted_routes[len(sorted_routes) - (i + 1)]
        j = 0
        lowest_save = 0
        permanent_route1 = None
        while j < len(sorted_routes):
            route2 = sorted_routes[j]
            if check_switch(route1[1], route2[1]):
                if check_switch(route1[1], route2[1])[1] > lowest_save:
                    permanent_route1 = route1
                    permanent_route2 = route2
                    lowest_save = check_switch(route1[1], route2[1])[1]
            if j == (len(sorted_routes) - (i + 1)) and permanent_route1 is not None:
                sorted_routes.remove(permanent_route1)
                sorted_routes.remove(permanent_route2)
                routes = switch(permanent_route1[1], permanent_route2[1])
                route1 = routes[0]
                route2 = routes[1]
                sorted_routes.append(route1)
                sorted_routes.append(route2)
                sorted_routes = countSort2(sorted_routes)
                j = -1
                i = 0
                changed += 1
                permanent_route1 = None
            j += 1
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


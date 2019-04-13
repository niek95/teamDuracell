def connect_basic(batteries, houses):
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
    "TODO"


def connect_greedy_hillclimb(batteries, houses):
    "TODO"

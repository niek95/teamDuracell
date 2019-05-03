import sys
import algorithms
from battery import Battery
from house import House
import matplotlib.pyplot as plt

ROUTE_COST = 9


def main():
    switcher = {
        "1": ("Data/wijk1_batterijen.txt", "Data/wijk1_huizen.txt"),
        "2": ("Data/wijk2_batterijen.txt", "Data/wijk2_huizen.txt"),
        "3": ("Data/wijk3_batterijen.txt", "Data/wijk3_huizen.txt")
    }
    batteries = import_batteries(switcher[sys.argv[1]][0])
    houses = import_houses(switcher[sys.argv[1]][1])
    # run algorithm of choice
    if sys.argv[2] == "1":
        connected = algorithms.connect_basic(batteries, houses)
    elif sys.argv[2] == "2":
        connected = algorithms.connect_greedy(batteries, houses)
    elif sys.argv[2] == "3":
        connected = algorithms.connect_greedy_hillclimb(batteries, houses)
    elif sys.argv[2] == "4":
        connected = algorithms.turn_by_turn(batteries, houses)
    elif sys.argv[2] == "5":
        connected = algorithms.constraint_relaxation(batteries, houses)
    else:
        print("we haven't implemented that yet")
        sys.exit(1)
    # print true if all houses connected, and total price
    print(connected)
    for battery in batteries:
        print(battery.get_used_cap())
    print(calculate_costs(batteries))
    visualize(batteries)


def import_batteries(file):
    batteries = []
    try:
        with open(file, "r") as f:
            id = 0
            for line in f:
                lines = line.split(',')
                x_battery = lines[0]
                y_battery = lines[1]
                max_input = lines[2].strip()
                max_input = float(max_input)
                battery = Battery(id, x_battery, y_battery, max_input)
                batteries.append(battery)
                id += 1
    except IOError:
        print("Couldn't open battery file")
        sys.exit
    return batteries


def import_houses(file):
    houses = []
    try:
        with open(file, "r") as f:
            id = 0
            for line in f:
                house_info = line.split(',')
                x_house = int(house_info[0])
                y_house = int(house_info[1])
                out_put = float(house_info[2])
                house = House(id, x_house, y_house, out_put)
                houses.append(house)
                id += 1

    except IOError:
        print("Couldn't open house file")
        sys.exit
    return houses


def calculate_costs(batteries):
    cost = 0
    for battery in batteries:
        for route in battery.routes:
            cost += route.get_length()*ROUTE_COST

    return cost


def visualize(batteries):
    # Iterate over the batteries to find the route with the corresponding house
    for battery in batteries:
        plt.plot(battery.get_x(),battery.get_y() ,'X', color = 'black', markersize=12)
        for route in battery.routes:
            length = route.get_length()
            # Retrieve the route between battery and house
            if length < 40:
                routes = [(tup1, tup2) for tup1, tup2 in route.get_coordinates()]
                plt.plot(*zip(*routes), linewidth = 1, linestyle = 'solid', marker = 'o', markersize = 1, color = 'blue')
            else:
                routes = [(tup1, tup2) for tup1, tup2 in route.get_coordinates()]
                plt.plot(*zip(*routes), linewidth = 1, linestyle = 'solid', marker = 'o', markersize = 1, color = 'red')
    # Show the route in a grid
    plt.grid()
    plt.show()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: app.py neighbourhood_no algorithm_no")
        sys.exit(1)
    main()

import sys
import algorithms
from battery import Battery
from house import House
import matplotlib.pyplot as plt

ROUTE_COST = 9


def main():
    batteries = import_batteries(sys.argv[1])
    houses = import_houses(sys.argv[2])
    # run algorithm of choice
    if sys.argv[3] == "1":
        connected = algorithms.connect_basic(batteries, houses)
    elif sys.argv[3] == "2":
        connected = algorithms.connect_greedy(batteries, houses)
    elif sys.argv[3] == "3":
        connected = algorithms.connect_greedy_hillclimb(batteries, houses)
    elif sys.argv[3] == "4":
        connected = algorithms.turn_by_turn(batteries, houses)
    else:
        print("we haven't implemented that yet")
        sys.exit(1)
    # print true if all houses connected, and total price
    print(connected)
    for battery in batteries:
        print(battery.get_used_cap())
    print(calculate_costs(batteries))


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
            for i in route.get_coordinates():
                #print(i[0], i[1])
                plt.plot(i[1] ,i[0] , 'ro--')
    plt.show()
    return cost


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: app.py battery_file house_file algorithm_no")
        sys.exit(1)
    main()

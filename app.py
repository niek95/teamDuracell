import sys
import algorithms
import route_settings
from battery import Battery
from house import House
from route import Route
import matplotlib.pyplot as plt
import helpers

ROUTE_COST = 9


def main():
    switcher = {
        "1": ("Data/wijk1_batterijen.txt", "Data/wijk1_huizen.txt"),
        "2": ("Data/wijk2_batterijen.txt", "Data/wijk2_huizen.txt"),
        "3": ("Data/wijk3_batterijen.txt", "Data/wijk3_huizen.txt")
    }
    houses = import_houses(switcher[sys.argv[1]][1])
    route_settings.init()
    for house in houses:
        route_settings.house_coordinates.append((house.get_x(), house.get_y()))
    batteries = import_batteries(switcher[sys.argv[1]][0], houses)

    for house in houses:
        plt.plot(house.get_x(),house.get_y() ,'o', color = 'black', markersize=2)
    # run algorithm of choice
    if sys.argv[2] == "1":
        connected = algorithms.connect_basic(batteries, houses)
    elif sys.argv[2] == "2":
        connected = algorithms.connect_greedy(batteries, houses)
    elif sys.argv[2] == "3":
        connected = algorithms.constraint_relaxation(batteries, houses)
    elif sys.argv[2] == "4":
        connected = algorithms.a_ster(batteries, houses)
    else:
        print("we haven't implemented that yet")
        sys.exit(1)
    try:
        if sys.argv[3] == "0" or sys.argv[3] is None:
            print("no third algorithm")
        elif sys.argv[3] == "1":
            connected1 = algorithms.hillclimb(batteries, houses)
        else:
            print("we haven't implemented that yet")
            sys.exit(1)
    except:
        print("no third algorithm")

    if connected:
        print("Alle huizen zijn verbonden")
    else:
        print("Er zijn een aantal huizen niet verbonden")
    print("Hoeveel huizen kruizen al onze routes =", helpers.check_cross_houses(houses, batteries))
    print("kosten van het plaatsen van de verbindingen =", calculate_costs(batteries))
    visualize(batteries, houses)
    plt.show()


def import_batteries(file, houses):
    batteries = []
    try:
        with open(file, "r") as f:
            coordinates = algorithms.change_batteries(houses)
            prompt = input("wilt u de batterijen verplaatsen met k-means? y / n ?")
            id = 0
            for line in f:
                lines = line.split(',')

                if "y" in prompt:
                    for house in houses:
                        center1 = round(coordinates[id][0], 0)
                        center2 = round(coordinates[id][1], 0)
                        if house.get_x() == center1 and house.get_y() == center2:
                            center1 += 1
                            center2 += 1
                        x_battery = center1
                        y_battery = center2
                else:
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


def visualize(batteries, houses):
    # Iterate over the batteries to find the route with the corresponding house

    for battery in batteries:
        plt.plot(battery.get_x(),battery.get_y() ,'X', color = 'black', markersize=12)
        for route in battery.get_routes():

            length = route.get_length()
            # Retrieve the route between battery and house
            optimal = True
            for battery in batteries:
                test = Route(route.get_house(), battery)
                if test.get_length() < length:
                    optimal = False
            if optimal:
                routes = [(tup1, tup2) for tup1, tup2 in route.get_coordinates()]
                plt.plot(*zip(*routes), linewidth = 1, linestyle = 'solid', marker = 'o', markersize = 1, color = 'blue')
                plt.pause(0.1)
            else:
                routes = [(tup1, tup2) for tup1, tup2 in route.get_coordinates()]
                plt.plot(*zip(*routes), linewidth = 1, linestyle = 'solid', marker = 'o', markersize = 1, color = 'red')
                plt.pause(0.1)

    # Show the route in a grid
    plt.grid()

if __name__ == "__main__":
    main()

import sys
import algorithms
import route_settings
from battery import Battery
from house import House
from route import Route
import matplotlib.pyplot as plt
import helpers
import matplotlib.animation as animation
import numpy as np

ROUTE_COST = 9


def main():
    try:
        map = sys.argv[1]
    except IndexError:
        print("Please specify map parameter")
        sys.exit(1)
    try:
        algorithm = sys.argv[2]
    except IndexError:
        print("Please specify algorithm parameter")
        sys.exit(1)
    try:
        hillclimb = sys.argv[3]
    except IndexError:
        print("Please specify hillclimb")
        sys.exit(1)
    try:
        runs = int(sys.argv[4])
    except IndexError:
        print("Please specify amount of runs")
    # Choose battery and house map
    switcher = {
        "1": ("Data/wijk1_batterijen.txt", "Data/wijk1_huizen.txt"),
        "2": ("Data/wijk2_batterijen.txt", "Data/wijk2_huizen.txt"),
        "3": ("Data/wijk3_batterijen.txt", "Data/wijk3_huizen.txt")
    }
    try:
        houses = import_houses(switcher[map][1])
        route_settings.init()
        batteries = import_batteries(switcher[map][0], houses)
    except IOError:
        print("Can't open files")
        sys.exit(1)

    results = []
    # Run algorithm of choice
    if algorithm == "1":
        print("Connecting houses using random algorithm")
        for _ in range(runs):
            connected = algorithms.connect_basic(batteries, houses)
            if connected:
                apply_hillclimb(hillclimb, batteries, houses)
                results.append(calculate_costs(batteries))
            if runs > 1:
                clear_routes(batteries)
    elif algorithm == "2":
        print("Connecting houses using greedy algorithm")
        for _ in range(runs):
            connected = algorithms.connect_greedy(batteries, houses)
            apply_hillclimb(hillclimb, batteries, houses)
            results.append(calculate_costs(batteries))
            if runs > 1:
                clear_routes(batteries)
    elif algorithm == "3":
        print("Connecting houses using constraint relaxation algorithm")
        for _ in range(runs):
            connected = algorithms.constraint_relaxation(batteries, houses)
            apply_hillclimb(hillclimb, batteries, houses)
            results.append(calculate_costs(batteries))
            # re-add houses, as they seem to disappear
            for battery in batteries:
                for route in battery.get_routes():
                    houses.append(route.get_house())
            if runs > 1:
                clear_routes(batteries)
    else:
        print("We haven't implemented that yet")
        sys.exit(1)
  

    print(min(results))
    # Print relevant info and plot
    if runs == 1:
        if connected:
            print("All houses connected")
        else:
            print("Some houses not connected")
        print("Houses crossed by routes =",
              helpers.check_cross_houses(houses, batteries))
        print("Total costs:",
              calculate_costs(batteries))
        visualize(batteries, houses)
    plt.show()

def apply_hillclimb(hillclimb, batteries, houses):
    # Apply hillclimbing
    try:
        if hillclimb == "0":
            print("Don't apply hillclimb")
        elif hillclimb == "1":
            print("Applying hillclimb")
            algorithms.hillclimb(batteries, houses)
        else:
            print("Hillclimb parameter should be 0 or 1")
    except IndexError:
        print("Please specify hillclimb parameter")
        sys.exit(1)


def import_batteries(file, houses):
    """
    Imports batteries from map, or places them based on house clusters
    """
    batteries = []
    try:
        with open(file, "r") as f:
            coordinates = algorithms.change_batteries(houses)
            prompt = input("wilt u de batterijen verplaatsen met k-means of 17 clusters plaatsen? y / n / k ?")
            id = 0
            for line in f:
                lines = line.split(',')
                x_battery = None
                if "y" in prompt:
                    for house in houses:
                        center1 = round(coordinates[id][0], 0)
                        center2 = round(coordinates[id][1], 0)
                        if house.get_x() == center1 \
                           and house.get_y() == center2:
                            center1 += 1
                            center2 += 1
                        x_battery = center1
                        y_battery = center2
                elif "n" in prompt:
                    x_battery = lines[0]
                    y_battery = lines[1]
<<<<<<< HEAD
                if x_battery is not None:
                    max_input = lines[2].strip()
                    max_input = float(max_input)
                    battery = Battery(id, x_battery, y_battery, max_input)
                    batteries.append(battery)
                    id += 1
=======
                max_input = lines[2].strip()
                max_input = float(max_input)
                battery = Battery(id, x_battery, y_battery, max_input)
                batteries.append(battery)
                id += 1
>>>>>>> refs/remotes/origin/master

            if "k" in prompt:
                coordinates = algorithms.change_batteries1(houses)
                for i in range(0, len(coordinates)):
                    max_input = 1800
                    max_input = float(max_input)
                    for house in houses:
                        center1 = round(coordinates[i][0], 0)
                        center2 = round(coordinates[i][1], 0)

                        if house.get_x() == center1 and house.get_y() == center2:
                            center1 += 1
                            center2 += 1
                        x_battery = center1
                        y_battery = center2
<<<<<<< HEAD
                    print(x_battery, y_battery)
=======
>>>>>>> refs/remotes/origin/master
                    battery = Battery(i, x_battery, y_battery, max_input)
                    batteries.append(battery)

    except IOError:
        print("Couldn't open battery file")
        sys.exit(1)
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
        sys.exit(1)
    return houses


def calculate_costs(batteries):
    cost = 0
    for battery in batteries:
        for route in battery.routes:
            cost += route.get_length()*ROUTE_COST
    return cost


def visualize(batteries, houses):
    # Show the route in a grid
    mng = plt.get_current_fig_manager()
    mng.full_screen_toggle()
    plt.grid()
    for house in houses:
        plt.plot(house.get_x(), house.get_y(),
                 'o', color='black', markersize=2)
    # Iterate over the batteries to find the route with the corresponding house
    for battery in batteries:
        plt.plot(battery.get_x(), battery.get_y(),
                 'X', color='black', markersize=12)
        for route in battery.get_routes():
            # Check if the route selected is optimal, or if the house has
            # a battery closer by
            length = route.get_length()
            optimal = True
            for battery in batteries:
                test = Route(route.get_house(), battery)
                if test.get_length() < length:
                    optimal = False
            if optimal:
                routes = [(tup1, tup2) for tup1,
                          tup2 in route.get_coordinates()]
                plt.plot(*zip(*routes), linewidth=1, linestyle='solid',
                         marker='o', markersize=1, color='blue')
                plt.pause(0.1)
            else:
                routes = [(tup1, tup2) for tup1,
                          tup2 in route.get_coordinates()]
                plt.plot(*zip(*routes), linewidth=1, linestyle='solid',
                         marker='o', markersize=1, color='red')
                plt.pause(0.1)

def clear_routes(batteries):
    for battery in batteries:
        battery.clear_all()

<<<<<<< HEAD
def save(batteries, houses):
    plt.rcParams['animation.ffmpeg_path'] = r'C:\Users\Joost Bankras\Anaconda3\Lib\site-packages\ffmpeg-20190527-3da8d04-win64-static\bin\ffmpeg.exe'
    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
    fig2 = plt.figure()
    
    ims = []
    ims1 = []
    for house in houses:
        plt.plot(house.get_x(), house.get_y(),
                 'o', color='black', markersize=2)
    # Iterate over the batteries to find the route with the corresponding house
    for battery in batteries:
        plt.plot(battery.get_x(), battery.get_y(),
                 'X', color='black', markersize=12)
        for route in battery.get_routes():
            # Check if the route selected is optimal, or if the house has
            # a battery closer by
            length = route.get_length()
            optimal = True
            for battery in batteries:
                test = Route(route.get_house(), battery)
                if test.get_length() < length:
                    optimal = False
            if optimal:
                routes = [(tup1, tup2) for tup1,
                          tup2 in route.get_coordinates()]
                ims.append(plt.plot(*zip(*routes), linewidth=1, linestyle='solid',
                         marker='o', markersize=1, color='blue'))
            else:
                routes = [(tup1, tup2) for tup1,
                          tup2 in route.get_coordinates()]
                ims.append(plt.plot(*zip(*routes), linewidth=1, linestyle='solid',
                         marker='o', markersize=1, color='red'))
            ims1.append(ims)

    im_ani = animation.ArtistAnimation(fig2, ims, interval=300, frames=1)
    im_ani.save('im1.mp4', writer=writer)
    
=======
>>>>>>> refs/remotes/origin/master
if __name__ == "__main__":
    main()
    
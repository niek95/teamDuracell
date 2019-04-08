import sys
from batteries import Batteries
from houses import House

def main():
    batteries = []
    houses = []

    if len(sys.argv) not 3:
        print("Usage: app.py house_file battery_file")
        sys.exit

    import_batteries(sys.argv[2])
    import_houses(sys.argv[1])

    for i in range(0,len(houses)):
        print(houses[i].routes)

def import_batteries(file):
    try:
        with open(file, "r") as f:
            id = 0
            for line in f:
                lines = line.split(',')
                x_battery = lines[0]
                y_battery = lines[1]
                max_input = lines[2].strip()
                max_input = float(max_input)
                battery = Batteries(id, x_battery, y_battery, max_input)
                batteries.append(battery)
                id += 1
    except IOerror:
        print("Couldn't open battery file")
        sys.exit

def import_houses(file):
    try:
        with open(file, "r") as f:
            id = 0
            for line in f:
                house_info = house.split(',')
                x_house = int(house_info[0])
                y_house = int(house_info[1])
                out_put = float(house_info[2])
                house = House(id, x_house, y_house, out_put)
                houses.append(house)
                id += 1
                for battery in batteries:
                    house.add_route(battery.id, battery.x_bat, battery.y_bat)




if __name__ == "__main__":
    main()

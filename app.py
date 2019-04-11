import sys
from batteries import Battery
from houses import House


class App():

    def __init__(self, b_file, h_file):
        self.batteries = self.import_batteries(b_file)

        self.houses = self.import_houses(h_file)

    def main(self):
        self.connected_houses = self.connect_houses()

    def import_batteries(self, file):
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

    def import_houses(self, file):
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

    def connect_houses(self):
        houses = self.houses
        connected_houses = []

        for i in range(0, len(self.batteries)):
            battery = self.batteries[i]
            while battery.get_used_cap() < battery.get_capacity():
                cap_left = battery.get_capacity() - battery.get_used_cap()
                for house in houses:
                    if house.get_output() < cap_left:
                        battery.connect_house(house)
                        connected_houses.append(house)
                        houses.remove(house)
                break
        return connected_houses


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: app.py battery_file house_file")
        sys.exit(1)
    app = App(sys.argv[1], sys.argv[2])
    app.main()

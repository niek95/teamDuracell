from batteries import Batteries
from houses import House

with open("Huizen&Batterijen/wijk1_batterijen.txt", "r") as f:
    batteries = []
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

with open("Huizen&Batterijen/wijk1_huizen.txt", "r") as g:
    houses = []
    id = 0
    for house in g:
        house_info = house.split(',')
        x_house = int(house_info[0])
        y_house = int(house_info[1])
        out_put = float(house_info[2])
        house = House(id, x_house, y_house, out_put)
        houses.append(house)
        id += 1
        for battery in batteries:
            house.add_route(battery.id, battery.x_bat, battery.y_bat)

for i in range(0,len(houses)):
    print(houses[i].routes)

from batteries import Batteries
from houses import House

with open("Huizen&Batterijen/wijk1_batterijen.txt", "r") as f: 
    batteries = {}
    id = 0
    for line in f:
        lines = line.split(',')
        x_battery = lines[0]
        y_battery = lines[1]
        max_input = lines[2].strip()
        max_input = float(max_input)
        batterie = Batteries(id, x_battery, y_battery, max_input)
        batteries[id] = batterie
        id += 1

with open("Huizen&Batterijen/wijk1_huizen.txt", "r") as g:
    houses = {}
    id = 0
    for house in g:
        house_info = house.split(',')
        x_house = int(house_info[0])
        y_house = int(house_info[1])
        out_put = float(house_info[2])
        house = House(id, x_house, y_house, out_put)
        houses[id] = house
        id += 1    
        for i in range(0,len(batteries)):
            x_battery = batteries[i].x_bat
            y_battery = batteries[i].y_bat 
            house.add_route(x_battery, y_battery)      
    
for i in range(0,len(houses)):
    print(houses[i].routes)
class Route(object):
    def __init__(self, house, battery):
        self._house = house
        self._battery = battery
        self._coordinates = self.calculate_route()
        self._length = len(self._coordinates)

    def calculate_route1(self):
        """
        calculates the most basic route between battery and house, going
        horizontally first, then vertically, adding coordinates to the list
        """
        route = []
        start_x = min(self._house.get_x(), self._battery.get_x())
        start_y = min(self._house.get_y(), self._battery.get_y())
        end_x = max(self._house.get_x(), self._battery.get_x())
        end_y = max(self._house.get_y(), self._battery.get_y())
        x = start_x
        y = start_y
        length = sum((end_x - start_x, end_y - start_y))
        route.append((x, y))
        length1 = 0
        while length1 < length:
            if x != end_x:
                x += 1
                route.append((x, y))
            elif y != end_y:
                y += 1
                route.append((x, y))
            length1 += 1
        return route

    def calculate_route(self):
        route = []
        start_x = self._house.get_x()
        start_y = self._house.get_y()
        eind_x = self._battery.get_x()
        eind_y = self._battery.get_y()
        delta_x = eind_x - start_x
        delta_y = eind_y - start_y
        if delta_x < 0:
            delta_x *= -1
        if delta_y < 0:
            delta_y *= - 1
        length = delta_x + delta_y
        x = start_x
        y = start_y
        for length1 in range(0, length + 1):
            if x != eind_x:
                if start_x < eind_x:
                    route.append((x, y))
                    x += 1
                    
                else:
                    route.append((x, y))
                    x -= 1
                    
            elif y != eind_y:
                if start_y < eind_y:
                    route.append((x, y))
                    y += 1
                    
                else:
                    route.append((x, y))
                    y -= 1
        route.append((eind_x,eind_y))            
        return route 

    def get_house(self):
        return self._house

    def get_battery(self):
        return self._battery

    def get_coordinates(self):
        return self._coordinates

    def get_length(self):
        return self._length

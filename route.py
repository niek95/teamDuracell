class Route(object):
    def __init__(self, house, battery):
        self._house = house
        self._battery = battery
        self._coordinates = self.calculate_route()
        self._length = len(self._coordinates)

    def calculate_route(self):
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
        for curr_length in range(0, length):
            if x != end_x:
                x += 1
                route.append((x, y))
            else:
                y += 1
                route.append((x, y))
        return route

    def get_house(self):
        return self._house

    def get_battery(self):
        return self._battery

    def get_coordinates(self):
        return self._coordinates

    def get_length(self):
        return self._length

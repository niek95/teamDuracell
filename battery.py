from route import Route


class Battery(object):
    def __init__(self, id, x, y, capacity):
        self.id = id
        self.x_bat = int(x)
        self.y_bat = int(y)
        self.capacity = float(capacity)
        self.used_cap = 0
        self.routes = []

    def connect_house(self, house):
        route = Route(house, self)
        self.routes.append(route)
        house.add_route(route)
        self.used_cap += house.get_output()

    def remove_route(self, route):
        self.routes.remove(route)
        self.used_cap -= route.get_house().get_output()

    def get_x(self):
        return self.x_bat

    def get_y(self):
        return self.y_bat

    def set_x(self, x):
        self.x_bat = x

    def set_y(self, y):
        self.y_bat = y

    def get_capacity(self):
        return self.capacity

    def get_used_cap(self):
        return self.used_cap

    def get_routes(self):
        return self.routes

    def get_over_cap(self):
        return self.used_cap > self.capacity

    def clear_all(self):
        self.routes = []
        self.used_cap = 0

class Battery(object):
    def __init__(self, id, x, y, in_put):
        self.id = id
        self.x_bat = int(x)
        self.y_bat = int(y)
        self.in_put = float(in_put)
        self.routes = []

    def add_route(self, x_house, y_house):
        x_distance = x_house - self.x_bat
        if x_distance < 0:
            x_distance *= -1
        y_distance = y_house - self.y_bat
        if y_distance < 0:
            y_distance *= -1
        total_distance = x_distance + y_distance
        self.routes.append(total_distance)

    def get_x(self):
        return self.x_bat

    def get_y(self):
        return self.y_bat

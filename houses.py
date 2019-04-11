class House(object):
    def __init__(self, id, x, y, output):
        self.id = id
        self.x_house = x
        self.y_house = y
        self.output = output
        self.routes = []

    def add_route(self, x, y):
        x_length = self.x_house - x
        if x_length < 0:
            x_length *= -1
        y_length = self.y_house - y
        if y_length < 0:
            y_length *= -1
        total_length = x_length + y_length
        self.routes.append(total_length)

    def get_x(self):
        return self.x_house

    def get_y(self):
        return self.y_house

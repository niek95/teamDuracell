class House(object):
    def __init__(self, id, x, y, output):
        self.id = id
        self.x_house = int(x)
        self.y_house = int(y)
        self.output = output

    def add_route(self, route):
        self.route = route

    def get_route(self):
        return self.route

    def get_id(self):
        return self.id

    def get_x(self):
        return self.x_house

    def get_y(self):
        return self.y_house

    def get_output(self):
        return self.output

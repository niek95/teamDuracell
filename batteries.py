class Batteries(object):
    def __init__(self, indentification, x, y, in_put):
        self.indentification = indentification
        self.x_bat = int(x)
        self.y_bat = int(y)
        self.in_put = float(in_put)
        self.routes = []
        
    def add_routes(self, x_house, y_house):
        x_distance = x_house - self.x_bat
        if x_distance < 0:
            x_distance *= -1
        y_distance = y_house - self.y_bat
        if y_distance < 0:
            y_distance *= -1
        total_distance = x_distance + y_distance
        self.routes.append(total_distance)
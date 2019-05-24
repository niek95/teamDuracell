import route_settings


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

    def a_ster(self, start, end):
        print("calculating route")
        grid_max = 49;

        class Node():
            """A node class for A* Pathfinding"""
            def __init__(self, parent=None, position=None):
                self.parent = parent
                self.position = position
                if position in route_settings.house_coordinates:
                    self.cost = 5000
                else:
                    self.cost = 9
                self.g = 0
                self.h = 0
                self.f = 0

            def __eq__(self, other):
                return self.position == other.position

        # Initialize open list
        open_list = []

        # Initialize closed list
        closed_list = []

        # Put starting node in the open list, keeping its f at zero
        start_node = Node(None, start)
        start_node.g = start_node.h = start_node.f = 0
        end_node = Node(None, end)
        end_node.g = end_node.h = end_node.f = 0
        open_list.append(start_node)

        # While the open list is not empty
        while len(open_list) > 0:
            current_node = open_list[0]
            current_index = 0
            # Find the node with lowest f, call it current_node and keep track of current index
            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index
            # Pop current node of the open list
            open_list.pop(current_index)
            closed_list.append(current_node)
            # If current node is the end node we have found the goal, quit
            if current_node == end_node:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                return path

            children = []
            for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                node_position = (current_node.position[0] + new_position[0],
                                 current_node.position[1] + new_position[1])
                if node_position[0] > grid_max or node_position[0] < 0 \
                   or node_position[1] > grid_max or node_position[1] < 0:
                    continue
                new_node = Node(current_node, node_position)
                children.append(new_node)

            for child in children:
                if len([closed_child for closed_child in closed_list if closed_child == child]) > 0:
                    continue

                child.g = current_node.g + child.cost
                child.h = abs(child.position[0] - end_node.position[0]) + \
                    abs(child.position[1] - end_node.position[1])
                child.f = child.g + child.h

                if len([open_node for open_node in open_list if child == open_node and child.g > open_node.g]) > 0:
                    continue
                open_list.append(child)

    def get_house(self):
        return self._house

    def get_battery(self):
        return self._battery

    def get_coordinates(self):
        return self._coordinates

    def get_length(self):
        return self._length

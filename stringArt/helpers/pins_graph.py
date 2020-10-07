import math

class PinsGraph:

    def __init__(self, image):
        self.nodes = []
        self.create_graph(image)


    def create_graph(self, image):
        for pin in image.pin_arr:
            self.nodes.append(PinNode(pin))
        for i in range(len(self.nodes)-1):
            pin = self.nodes[i]
            for next_pin in self.nodes[i+1:]:
                if pin.is_neighbor(next_pin, image.PIN_DISTANCE):
                    pin.add_neighbor(next_pin)

class PinNode:

    def __init__(self, coords):
        self.coords = coords
        self.neighbors = []

    def add_neighbor(self, neighbor_node):
        self.neighbors.append(neighbor_node)
        neighbor_node.neighbors.append(self)

    def is_neighbor(self, next_pin, PIN_DISTANCE):
        max_distance = PIN_DISTANCE * 3
        distance = math.sqrt((self.coords[0])**2 + (self.coords[1])**2)
        return distance <= max_distance

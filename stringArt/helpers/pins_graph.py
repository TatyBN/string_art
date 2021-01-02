import math

class PinsGraph:

    # since all this class needs is image.pin_arr and image.PIN_DISTANCE, i'd pass those separately and
    # not the whole image
    def __init__(self, image):
        self.nodes = []
        self.create_graph(image)


    def create_graph(self, image):
        for index, pin in enumerate(image.pin_arr):
            self.nodes.append(PinNode(pin, index))
        # i'd still use `for index, pin in self.nodes:` here, it's easier to understand
        for i in range(len(self.nodes)-1):
            pin = self.nodes[i]
            for next_pin in self.nodes[i+1:]:
                # i like the naming of these methods, it's very clear what's going on
                if pin.is_neighbor(next_pin, image.PIN_DISTANCE):
                    pin.add_neighbor(next_pin)

class PinNode:

    def __init__(self, coords, id):
        # reorder these lines so they correspond to the signature
        self.id = id
        self.coords = coords
        self.neighbors = {}
        self.strings = {}

    def add_neighbor(self, neighbor_node):
        self.neighbors[neighbor_node.id] = neighbor_node
        neighbor_node.neighbors[self.id] = self

    def add_string(self, neighbor_node):
        del self.neighbors[neighbor_node.id]
        self.strings[neighbor_node.id] = neighbor_node
        del neighbor_node.neighbors[self.id]
        neighbor_node.strings[self.id] = self
        

    def is_neighbor(self, next_pin, PIN_DISTANCE):
        # magic number 3 should probably be a constant ;)
        max_distance = PIN_DISTANCE * 3
        # i think you can leave off the math.sqrt here, if you square the max_distance 
        # (calculating sqrt is expensive)
        distance = math.sqrt((self.coords[0] - next_pin.coords[0])**2 + (self.coords[1] - next_pin.coords[1])**2)
        return distance <= max_distance

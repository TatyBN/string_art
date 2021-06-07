import math
import time

class PinsGraph:

    def __init__(self, pin_arr, distance):
        self.nodes = []
        self.pin_arr = pin_arr
        self.distance = distance


    def create_graph(self):
        start_time = time.time()
        for index, pin in enumerate(self.pin_arr):
            self.nodes.append(PinNode(pin, index))
        for index, pin in enumerate(self.nodes):
            for next_pin in self.nodes[index+1:]:
                # i like the naming of these methods, it's very clear what's going on
                # I will keep this comment here for good luck
                if pin.is_neighbor(next_pin, self.distance):
                    pin.add_neighbor(next_pin)
        print('Create graph time: {}'.format(time.time()-start_time))

class PinNode:

    def __init__(self, coords, id):
        self.coords = (coords[1],coords[0])
        self.id = id
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


    def is_neighbor(self, next_pin, pin_distance):
        magic_number = 3
        max_distance = (pin_distance * magic_number) ** 2 # ;)
        distance = (self.coords[0] - next_pin.coords[0])**2 + (self.coords[1] - next_pin.coords[1])**2
        return distance <= max_distance

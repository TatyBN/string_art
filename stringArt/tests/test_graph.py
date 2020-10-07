import numpy as np
import cv2 as cv

def naive_find_neighbors(pin, pin_pic, PIN_DISTANCE):
    neighbors = []
    mask = np.zeros(pin_pic.shape, np.uint8)
    cv.circle(mask, pin, radius=PIN_DISTANCE*3, color=255, thickness=-1)
    for circle_coords in np.argwhere(mask==255):
        if np.any(pin_pic[circle_coords[0], circle_coords[1]] !=0):
            neighbors.append((circle_coords[1], circle_coords[0]))
    return neighbors

def test_graph_neighbors(graph, image):
    pin_img = image.create_pin_img()
    for node in graph.nodes:
        naive_neighbors = np.array(naive_find_neighbors(node.coords, pin_img, image.PIN_DISTANCE).sort())
        graph_neighbors = np.array([neighbor.coords for neighbor in node.neighbors].sort())
        print('pin: {}'.format(node.coords))
        compare = naive_neighbors == graph_neighbors.all()
        if(compare == False):
            print('Naive neighbors: {}'.format(naive_neighbors))
            print('Graph neighbors: {}'.format(graph_neighbors))
            break

import cv2 as cv
import time

from helpers.edgeImage import EdgeImg
from helpers.pinsImg import PinsImg
from helpers.pins_graph import PinsGraph
from helpers.stringImg import StringImg

WINDOW_NAME = 'String Art'

IMAGE_NAME = 'odri.jpg'
IMAGE_PATH = 'stringArt/resources/pics/' + IMAGE_NAME

STRING_IMAGE_NAME = '{}.jpg'.format(time.strftime("%m.%d_%H:%M"))
STRING_IMAGE_PATH = 'stringArt/resources/string_pics/' + STRING_IMAGE_NAME


def main():

    edge_img = EdgeImg(IMAGE_PATH)
    edge_img.create_edge_img()

    pin_img = PinsImg(edge_img.edge_coords, edge_img.edge_img.shape)
    pin_img.create_pin_img()

    graph = PinsGraph(pin_img.pin_arr, pin_img.distance)
    graph.create_graph()

    string_img = StringImg(graph.nodes, edge_img.img)
    string_img.generate_string_img()

    cv.imwrite(STRING_IMAGE_PATH, string_img.img_out)
    string_img.show_img('String Image',string_img.img_out, 0)



if __name__ == '__main__':
    main()

from pathlib import Path
import cv2 as cv

from helpers.pins_graph import PinsGraph
from helpers.image import Image

from tests.test_graph import test_graph_neighbors


def main():

    IMAGE_NAME = 'fashion.jpg'
    IMAGE_PATH = str( Path('stringArt/resources/pics/') / IMAGE_NAME )
    PIN_DISTANCE = 15

    img = Image(IMAGE_PATH, PIN_DISTANCE)
    graph = PinsGraph(img)

    test_graph_neighbors(graph, img)


if __name__ == '__main__':
    main()

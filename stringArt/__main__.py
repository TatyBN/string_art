from pathlib import Path
import cv2 as cv
import time

from helpers.pins_graph import PinsGraph
from helpers.image import Image

from tests.test_graph import test_graph_neighbors

def main():
    start_time = time.time()

    IMAGE_NAME = 'odri.jpg'
    IMAGE_PATH = str( Path('stringArt/resources/pics/') / IMAGE_NAME )
    STRING_IMAGE_NAME = '{}.jpg'.format(time.strftime("%m.%d_%H:%M"))
    STRING_IMAGE_PATHE = str( Path('stringArt/resources/string_pics/') / STRING_IMAGE_NAME )
    PIN_DISTANCE = 15

    img = Image(IMAGE_PATH, PIN_DISTANCE)
    graph = PinsGraph(img)

    img.generate_string_img(graph)

    print('@@@@@@@ {}'.format(time.time()-start_time))

    cv.imwrite(STRING_IMAGE_PATHE, img.img_out)
    img.show_img(img.img_out, 0)



if __name__ == '__main__':
    main()

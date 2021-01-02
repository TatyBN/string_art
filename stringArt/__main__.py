
import cv2 as cv
import time


from helpers.pins_graph import PinsGraph
from helpers.image import Image

# unused import
from tests.test_graph import test_graph_neighbors

def main():
    start_time = time.time()

    # I suppose these are constants? As such, they're usually defined outside of functions...
    WINDOW_NAME = 'String Art'

    IMAGE_NAME = 'odri.jpg'
    IMAGE_PATH = 'stringArt/resources/pics/' + IMAGE_NAME

    STRING_IMAGE_NAME = '{}.jpg'.format(time.strftime("%m.%d_%H:%M"))
    STRING_IMAGE_PATH = 'stringArt/resources/string_pics/' + STRING_IMAGE_NAME


    img = Image(IMAGE_PATH, WINDOW_NAME)
    graph = PinsGraph(img)

    img.generate_string_img(graph)

    print('@@@@@@@ {}'.format(time.time()-start_time))

    cv.imwrite(STRING_IMAGE_PATH, img.img_out)
    img.show_img(img.img_out, 0)



if __name__ == '__main__':
    main()

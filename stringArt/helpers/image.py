import cv2 as cv
import numpy as np
import time

class Image:

    def __init__(self, IMAGE_PATH, PIN_DISTANCE):
        self.img = cv.imread(IMAGE_PATH)
        self.img_height, self.img_width, _ = self.img.shape
        self.PIN_DISTANCE = PIN_DISTANCE
        self.edge_img = None
        self.pin_arr = []
        self.create_edge_img()
        self.create_pin_arr()

    def create_edge_img(self):
        LOW_THRESHOLD = 40
        RATIO = 3
        KERNEL_SIZE = 3

        gray_img = cv.cvtColor(self.img, cv.COLOR_BGR2GRAY)
        blur_img = cv.blur(gray_img, (3,3))
        self.edge_img = cv.Canny(blur_img, LOW_THRESHOLD, LOW_THRESHOLD*RATIO, KERNEL_SIZE)

    def create_pin_arr(self):
        start_time = time.time()
        for x in [i for i in range(self.img_width+1) if i % self.PIN_DISTANCE==0]:
            for y in [i for i in range(self.img_height+1) if i % self.PIN_DISTANCE==0]:
                coords = (x,y)
                mask = np.zeros(self.edge_img.shape, np.uint8)
                cv.circle(mask, coords, radius=self.PIN_DISTANCE//2, color=255, thickness=-1)
                for circle_coords in np.argwhere(mask==255):
                    if np.any(self.edge_img[circle_coords[0], circle_coords[1]] !=0):
                        coords = (circle_coords[1], circle_coords[0])
                        break
                self.pin_arr.append(coords)
        print('@@@@@@@ {}'.format(time.time()-start_time))

    def create_pin_img(self):
        pin_pic = np.zeros(self.edge_img.shape, np.uint8)
        for coords in self.pin_arr:
            pin_pic = cv.circle(pin_pic, coords, radius=0, color=(255, 255, 255), thickness=-1)
        return pin_pic

    def show_img(self, img, time=0):
        WINDOW_NAME = 'Playground'

        cv.imshow(WINDOW_NAME, img)
        cv.waitKey(time)

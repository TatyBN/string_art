import cv2 as cv
import numpy as np
import time

class PinsImg:
    def __init__(self, edge_coords, shape):
        self.edge_coords = edge_coords
        self.shape = shape
        self.window_name = 'Pins locations'
        self.pin_arr = None


    def create_pin_img(self):
        trackbar_name = 'Pins distance'

        cv.namedWindow(self.window_name)
        cv.createTrackbar(trackbar_name, self.window_name, 15, 50, self.adjust_pin_distance)

        self.adjust_pin_distance(15)
        cv.waitKey()
        cv.destroyAllWindows()

    def adjust_pin_distance(self, distance):
        start_time = time.time()
        self.distance = distance
        self.pin_arr = self.edge_coords[0::distance]
        for x in range(0, self.shape[0]+1, distance):
            for y in range(0, self.shape[1]+1, distance):
                self.pin_arr = np.append(self.pin_arr, [[x,y]], axis=0)
        pin_pic = np.zeros(self.shape, np.uint8)
        for coords in self.pin_arr:
            cv.circle(pin_pic, (coords[1], coords[0]), radius=0, color=(255, 255, 255), thickness=-1)
        print('adjust pin time: {}'.format(time.time() - start_time))
        cv.imshow(self.window_name, pin_pic)

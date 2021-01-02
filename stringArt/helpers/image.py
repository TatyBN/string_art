import cv2 as cv
import numpy as np
from skimage.metrics import structural_similarity as ssim
import random

import time


class Image:

    def __init__(self, IMAGE_PATH, WINDOW_NAME):
        self.img = cv.imread(IMAGE_PATH)
        self.WINDOW_NAME = WINDOW_NAME
        self.img_height, self.img_width, _ = self.img.shape
        self.img_out = np.zeros(self.img.shape, np.uint8)
        self.edge_img = None
        self.PIN_DISTANCE = None
        self.pin_arr = []
        self.create_edge_img()
        self.create_pin_img()

    def create_edge_img(self):
        LOW_THRESHOLD = 40
        MAX_THRESHOLD = 100
        TRACKBAR_NAME = 'Threshold'

        cv.imshow(self.WINDOW_NAME, self.img)
        cv.waitKey()

        cv.namedWindow(self.WINDOW_NAME)
        cv.createTrackbar(TRACKBAR_NAME, self.WINDOW_NAME, LOW_THRESHOLD, MAX_THRESHOLD, self.adjust_threshold)

        self.adjust_threshold(LOW_THRESHOLD)
        cv.waitKey()
        cv.destroyAllWindows()


    def adjust_threshold(self, low_threshold):
        RATIO = 3
        KERNEL_SIZE = 3

        gray_img = cv.cvtColor(self.img, cv.COLOR_BGR2GRAY)
        blur_img = cv.blur(gray_img, (3,3))
        self.edge_img = cv.Canny(blur_img, low_threshold, low_threshold*RATIO, KERNEL_SIZE)

        cv.imshow(self.WINDOW_NAME, self.edge_img)


    def create_pin_img(self):
        TRACKBAR_NAME = 'PIN_DISTANCE'

        cv.namedWindow(self.WINDOW_NAME)
        cv.createTrackbar(TRACKBAR_NAME, self.WINDOW_NAME, 15, 50, self.adjust_pin_distance)

        self.adjust_pin_distance(15)
        cv.waitKey()
        cv.destroyAllWindows()

    def adjust_pin_distance(self, distance):
        self.PIN_DISTANCE = distance
        pin_arr = []
        pin_pic = np.zeros(self.edge_img.shape, np.uint8)
        for x in [i for i in range(self.img_width+1) if i % distance==0]:
            for y in [i for i in range(self.img_height+1) if i % distance==0]:
                coords = (x,y)
                mask = np.zeros(self.edge_img.shape, np.uint8)
                cv.circle(mask, coords, radius=distance//2, color=255, thickness=-1)
                for circle_coords in np.argwhere(mask==255):
                    if np.any(self.edge_img[circle_coords[0], circle_coords[1]] !=0):
                        coords = (circle_coords[1], circle_coords[0])
                        break
                pin_arr.append(coords)
                pin_pic = cv.circle(pin_pic, coords, radius=0, color=(255, 255, 255), thickness=-1)
        self.pin_arr = pin_arr
        cv.imshow(self.WINDOW_NAME, pin_pic)

    def generate_string_img(self, pin_graph):
        current_pin = random.choice(pin_graph.nodes)
        best_score = -1
        prev_score = -1

        counter = 1
        alter_counter = 1

        for _ in range(2000):
            best_neighbor = None

            for neighbor in list(current_pin.neighbors.values()): #Is this really the nicest way to delete while iterating? I wonder
                mask = self.img_out.copy()
                cv.line(mask, current_pin.coords, neighbor.coords, color=(255,255,255), thickness=1)
                (score, diff) = ssim(self.img, mask, full=True, multichannel=True)
                if score > best_score :
                    best_score = score
                    best_neighbor = neighbor
                elif score < prev_score:
                    print('Delete: {} {}'.format(current_pin.coords, neighbor.coords))
                    del current_pin.neighbors[neighbor.id]
                    del neighbor.neighbors[current_pin.id]
            if not best_neighbor:
                print('@@@@@@@@@@@Alter root')
                alter_counter += 1
                best_neighbor = random.choice(list(current_pin.strings.values()))
            else:
                current_pin.add_string(best_neighbor)
            print('Current pin: {} Best neighbor: {} counter: {}'.format(current_pin.coords, best_neighbor.coords, counter))
            counter +=1
            cv.line(self.img_out, current_pin.coords, best_neighbor.coords, color=(255,255,255), thickness=1)
            self.show_img(self.img_out, 5)
            current_pin = best_neighbor
            prev_score = best_score
        print('Number of alter roots: {}'.format(alter_counter))


    def show_img(self, img, time=0):

        cv.imshow(self.WINDOW_NAME, img)
        cv.waitKey(time)

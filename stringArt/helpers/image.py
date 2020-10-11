import cv2 as cv
import numpy as np
from skimage.measure import compare_ssim
import random


class Image:

    def __init__(self, IMAGE_PATH, PIN_DISTANCE):
        self.img = cv.imread(IMAGE_PATH)
        self.gray_img = cv.cvtColor(self.img, cv.COLOR_BGR2GRAY)
        self.PIN_DISTANCE = PIN_DISTANCE
        self.img_height, self.img_width = self.gray_img.shape
        self.img_out = np.zeros(self.img.shape, np.uint8)
        self.edge_img = None
        self.pin_arr = []
        self.create_edge_img()
        self.create_pin_arr()

    def create_edge_img(self):
        LOW_THRESHOLD = 40
        RATIO = 3
        KERNEL_SIZE = 3

        blur_img = cv.blur(self.gray_img, (3,3))
        self.edge_img = cv.Canny(blur_img, LOW_THRESHOLD, LOW_THRESHOLD*RATIO, KERNEL_SIZE)

    def create_pin_arr(self):
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

    def create_pin_img(self):
        pin_pic = np.zeros(self.edge_img.shape, np.uint8)
        for coords in self.pin_arr:
            pin_pic = cv.circle(pin_pic, coords, radius=0, color=(255, 255, 255), thickness=-1)
        return pin_pic

    def generate_string_img(self, pin_graph):
        current_pin = pin_graph.nodes[random.randint(0, len(pin_graph.nodes)-1)]
        best_score = -1

        counter = 1
        alter_counter = 1

        for _ in range(4000):
            best_neighbor = None
            av_neighbors = []

            for neighbor in current_pin.neighbors:
                mask = self.img_out.copy()
                cv.line(mask, current_pin.coords, neighbor.coords, color=(255,255,255), thickness=1)
                (score, diff) = compare_ssim(self.img, mask, full=True, multichannel=True)
                if score > best_score :
                    best_score = score
                    best_neighbor = neighbor
                if score == best_score:
                    av_neighbors.append(neighbor)
            if not best_neighbor:
                print('@@@@@@@@@@@Alter root')
                alter_counter += 1
                best_neighbor = av_neighbors[random.randint(0, len(av_neighbors)-1)]
            print('Current pin: {} Best neighbor: {} counter: {}'.format(current_pin.coords, best_neighbor.coords, counter))
            counter +=1
            cv.line(self.img_out, current_pin.coords, best_neighbor.coords, color=(255,255,255), thickness=1)
            self.show_img(self.img_out, 5)
            current_pin = best_neighbor
        print('Number of alter roots: {}'.format(alter_counter))


    def show_img(self, img, time=0):
        WINDOW_NAME = 'Graph'

        cv.imshow(WINDOW_NAME, img)
        cv.waitKey(time)

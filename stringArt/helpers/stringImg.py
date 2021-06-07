import cv2 as cv
import numpy as np
import random
from skimage.metrics import structural_similarity as ssim
import time

class StringImg:

    def __init__(self, pin_nodes, img):
        self.pin_nodes = pin_nodes
        self.img = img
        self.img_out = np.zeros(img.shape, np.uint8)

    def generate_string_img(self): ########Working on it
        start_time = time.time()
        current_pin = random.choice(self.pin_nodes)
        best_score = -1
        prev_score = -1

        counter = 1
        alter_counter = 1

        for _ in range(2000):
            best_neighbor = None

            for neighbor in list(current_pin.neighbors.values()): #Is this really the nicest way to delete while iterating? I wonder
                mask = self.img_out.copy()
                cv.line(mask, current_pin.coords, neighbor.coords, color=(255,255,255), thickness=1)
                # this is probably what makes the whole thing slow... i think it should be possible to
                # make it faster by only running it on a single channel (since this is all grayscale) and
                # not running with full=True (the result of which is discarded anyway)...
                score = ssim(self.img, mask, multichannel=True)
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
            self.show_img('String Image', self.img_out, 5)
            current_pin = best_neighbor
            prev_score = best_score
        print('Number of alter roots: {}'.format(alter_counter))
        print('String time: {}'.format(time.time()-start_time))

    def show_img(self, window_name, img, time=0):
        cv.imshow(window_name, img)
        cv.waitKey(time)

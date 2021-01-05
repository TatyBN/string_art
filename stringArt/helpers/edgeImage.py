import cv2 as cv
import numpy as np

class EdgeImg:

    def __init__(self, image_path):
        self.window_name = 'Edges Image'
        self.img = cv.imread(image_path)
        self.edge_img = None
        self.edge_coords = None

    def create_edge_img(self):
        min_threshold = 40
        max_threshold = 100
        trackbar_name = 'Threshold'

        cv.namedWindow(self.window_name)
        cv.createTrackbar(trackbar_name, self.window_name, min_threshold, max_threshold, self.adjust_threshold)

        self.adjust_threshold(min_threshold)
        cv.waitKey()
        cv.destroyAllWindows()
        self.edge_coords = np.argwhere(self.edge_img == 255)


    def adjust_threshold(self, low_threshold):
        ratio = 3
        kernel_size = 3

        gray_img = cv.cvtColor(self.img, cv.COLOR_BGR2GRAY)
        blur_img = cv.blur(gray_img, (3,3))
        self.edge_img = cv.Canny(blur_img, low_threshold, low_threshold*ratio, kernel_size)

        cv.imshow(self.window_name, self.edge_img)

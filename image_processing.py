from operator import index
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import numpy as np

import cv2 as cv

TRIMMING_THERSHOLD = 100
GAP_WINDOW_THERSHOLD = 50
FILL_GAP_BORDERS = 2
STEEP_THRESHOLD = 40
LOWPASS_FILTER = 1

class ImageProcessing:
    def __init__(self, path):
        self.path = Path(path)

        if not self.path.exists():
            raise Exception(f'File {self.path} does not exist.')

        self.image = cv.imread(str(self.path))
        self.image = cv.cvtColor(self.image, cv.COLOR_BGR2GRAY)

        # laplacian = cv.Laplacian(self.image,cv.CV_64F)
        img_blur = cv.GaussianBlur(self.image, (3,3), 0)
        edges = cv.Canny(image=img_blur, threshold1=25, threshold2=25)
        kernel = np.ones((3,3), np.uint8)

        img_dilation = cv.dilate(edges, kernel, iterations=10)
        img_erosion = cv.erode(img_dilation, kernel, iterations=10)
        image_width = np.shape(img_erosion)[1]

        self.height_bounds = []
        for i in range(image_width):
            column = img_erosion[:, i]
            indexes = np.where(column == 255)
            if np.size(indexes) > 0:
                min_val, max_val = np.amin(indexes), np.amax(indexes)
                self.height_bounds.append((min_val, max_val))
            else:
                self.height_bounds.append((0, 0))


    def _show_image(self, image):
        plt.imshow(image, cmap="gray")
        plt.show()


    def show_image(self):
        self.show_image(self.image)


    def _trim_begining(self, heights):
        index = 0
        for height in heights:
            if height > TRIMMING_THERSHOLD:
                break
            index = index + 1

        return heights[index:]


    def _trim_end(self, heights):
        index = 0
        for height in reversed(heights):
            if height > TRIMMING_THERSHOLD:
                break
            index = index + 1

        return heights[:(len(heights)-index)]


    def _compute_heights(self, height_bounds):
        heights = []
        for (lower, upper) in height_bounds:
            heights.append(upper-lower)

        return heights


    def _fill_gaps(self, heights):

        for i in range(len(heights)):
            gap_length = 0
            if heights[i] == 0:
                while heights[i+gap_length] == 0:
                    gap_length = gap_length + 1

            if gap_length > 0 and gap_length < GAP_WINDOW_THERSHOLD:
                for index in range(gap_length):
                    sum = 0
                    divisor = 0

                    for left in range(-FILL_GAP_BORDERS,0):
                        it = i + left
                        if it >= 0:
                            sum += heights[it]
                            divisor = divisor + 1

                    for right in range(0, FILL_GAP_BORDERS):
                        it = i + gap_length + right
                        if it <= len(heights):
                            sum += heights[it]
                            divisor = divisor + 1

                    heights[i+index] = sum/divisor

        return heights


    def _smooth_values(self, heights):
        length = len(heights)

        for i in range(1, length - 1):
            derivative = heights[i] - heights[i-1]
            if derivative > STEEP_THRESHOLD:
                heights[i] = max(heights[i-1], heights[i+1])

        return heights

    def _find_lowest_point(self, heights):
        filtered_heights = []

        for i in range(1, len(heights) - 1):
            filtered_heights.append(np.sum(heights[i-LOWPASS_FILTER:i+LOWPASS_FILTER + 1])/(LOWPASS_FILTER*2+1))

        return min(filtered_heights)


    def find_min_height(self):
        self.heights = self._compute_heights(self.height_bounds)
        self.heights = self._trim_begining(self.heights)
        self.heights = self._trim_end(self.heights)
        self.heights = self._fill_gaps(self.heights)
        self.heights = self._smooth_values(self.heights)
        return np.round(self._find_lowest_point(self.heights), 2)
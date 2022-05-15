import cv2
import numpy as np


class SegmentedImage:

    def __init__(self):
        pass

    def get_segmented_image(self, image):
        """
        Creates a segmented image of chosen image.

        Used source: https://machinelearningknowledge.ai/image-segmentation-in-python-opencv/
        :param image:
        :return segmented image:
        """
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pixel_values = image.reshape((-1, 3))
        pixel_values = np.float32(pixel_values)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        k = 12
        _, labels, center = cv2.kmeans(pixel_values, k, None, criteria, 10, cv2.KMEANS_PP_CENTERS)
        center = np.uint8(center)

        labels = labels.flatten()
        segmented_image = center[labels.flatten()]
        segmented_image = segmented_image.reshape(image.shape)

        return cv2.cvtColor(segmented_image, cv2.COLOR_RGB2BGR)

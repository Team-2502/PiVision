import cv2
import numpy as np
import Utils

on = Utils.getCurrentFrameMultiplier(0.5, 0.5)
off = Utils.getCurrentFrameMultiplier(0.5, 0.5)

sub = cv2.subtract(on, off);
hsv = cv2.cvtColor(sub, cv2.COLOR_BGR2HSV)

while True:
    kernel = np.ones((3, 3), np.uint8)
    lowerBound = np.array([50, 100, 20])
    upperBound = np.array([255, 255, 255])
    mask = cv2.inRange(hsv, lowerBound, upperBound)
    output = cv2.bitwise_and(sub, sub, mask=mask)

    threshold = Utils.modifyThreshold(output, 10)
    outputThreshold = cv2.cvtColor(threshold, cv2.COLOR_GRAY2BGR)
    erode = cv2.erode(outputThreshold, kernel, iterations=1)
    erode2 = cv2.erode(threshold, kernel, iterations=1)

    image, contours, hierarchy = cv2.findContours(erode2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contoursOut = Utils.filterContours(contours, 400)

    
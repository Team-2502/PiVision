import cv2
import numpy as np
import Util
import EdgeTest as edge

#on = Util.getCurrentFrameMultiplier(0.5, 0.5)
#off = Util.getCurrentFrameMultiplier(0.5, 0.5)

#sub = cv2.subtract(on, off);
#hsv = cv2.cvtColor(sub, cv2.COLOR_BGR2HSV)

# Make 7 windows
Util.nw('0')
Util.nw('1')
# Util.nw('2')
# Util.nw('3')
# Util.nw('4')
# Util.nw('5')
Util.nw('6')
Util.nw('7')
Util.nw('8')

def null(_):
    return

# Place a bunch of trackbars onto window 6
cv2.createTrackbar('0', '6', 0, 255, null)
cv2.createTrackbar('1', '6', 0, 255, null)
cv2.createTrackbar('2', '6', 0, 255, null)

cv2.createTrackbar('3', '6', 255, 255, null)
cv2.createTrackbar('4', '6', 255, 255, null)
cv2.createTrackbar('5', '6', 255, 255, null)

# Make a 3 by 3 matrix filled with ones
kernel = np.ones((3, 3), np.uint8)

#lowerBound = np.array([50, 100, 20])
#upperBound = np.array([255, 255, 255])

frame = cv2.imread('VL0_G.png')
frame = cv2.bitwise_not(frame)

# define our boundary for red in BGR
# THE COLORS ARE IN [BLUE, GREEN, RED]
# DO NOT FORGET!
boundary = [
    ([56, 0, 209],[136, 50, 255])
]

while True:
#    on = Util.getCurrentFrameMultiplier(0.5, 0.5)
#    off = Util.getCurrentFrameMultiplier(0.5, 0.5)
    frame = Util.getCurrentFrameMultiplier(0.5, 0.5)
    grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    lowerBound = np.array([cv2.getTrackbarPos('0', '6'), cv2.getTrackbarPos('1', '6'), cv2.getTrackbarPos('2', '6')])
    upperBound = np.array([cv2.getTrackbarPos('3', '6'), cv2.getTrackbarPos('4', '6'), cv2.getTrackbarPos('5', '6')])

    on = Util.getCurrentFrameMultiplier(0.25, 0.25)
    off = Util.getCurrentFrameMultiplier(0.25, 0.25)

    #sub = cv2.subtract(on, off)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower = np.array(boundary[0][0], dtype = "uint8")
    upper = np.array(boundary[0][1], dtype = "uint8")

    mask_hsv = cv2.inRange(hsv, lower, upper)
    filtered_hsv = cv2.bitwise_and(hsv, hsv, mask = mask_hsv)
    frame_edges = cv2.Canny(filtered_hsv, 290, 100)

    # mask = cv2.inRange(hsv, lowerBound, upperBound)
    # output = cv2.bitwise_and(frame, frame, mask=mask)

    # threshold = Util.modifyThreshold(output, 10)
    # outputThreshold = cv2.cvtColor(threshold, cv2.COLOR_GRAY2BGR)
    # erode = cv2.erode(outputThreshold, kernel, iterations=1)
    # erode2 = cv2.erode(threshold, kernel, iterations=5)

    image, contours, hierarchy = cv2.findContours(erode2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#    cv2.imshow('Vid Cap', threshold)
#    cv2.imshow('Vid Cap', outputThreshold)


    cv2.imshow('0', frame)
    cv2.imshow('1', hsv)
    # cv2.imshow('2', mask)
    # cv2.imshow('3', threshold)
    # cv2.imshow('4', erode)
    # cv2.imshow('5', erode2)
    cv2.imshow('7', frame_edges)
    cv2.imshow('8', filtered_hsv)

    # if edge.isGear(frame_edges):
    #     print("gear")
    # elif edge.isBoiler(frame_edges):
    #     print("boiler")
    # else:
    #     print("neither")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

Util.cleanUp()
#lowerBound = np.array([50, 100, 20])
#upperBound = np.array([255, 255, 255])

import cv2
import numpy as np
import Util
import EdgeTest as edge

Util.nw('1') # frame edges


# define our boundary for red in BGR
# THE COLORS ARE IN [BLUE, GREEN, RED]
# DO NOT FORGET!

boundary = [
    ([120, 133, 0],[255, 255, 255])
]

while True:
    # frame = Util.getCurrentFrameMultiplier(0.5, 0.5)
    frame = cv2.imread("testimg2.png")

    lower = np.array(boundary[0][0], dtype = "uint8")
    upper = np.array(boundary[0][1], dtype = "uint8")

    frame_mask = cv2.inRange(frame, lower, upper)
    filtered_frame = cv2.bitwise_and(frame, frame, mask = frame_mask)
    frame_edges = cv2.cvtColor(filtered_frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow('1', frame_edges)

    print("Midpoint: " + str(edge.middle(frame_edges)))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

Util.cleanUp()

"""Vision module for 2017. Sends dimensions and location of reflective tape."""
import cv2
import numpy as np
import Util
import EdgeTest as edge
import logging
from networktables import NetworkTables


# turn into a client to connect to a robot
# The robot should have a static IP
NetworkTables.initialize(server='10.25.02.2')

# Enable logging on our Pi
logging.basicConfig(level=logging.DEBUG)

# open the table
visionTable = NetworkTables.getTable("vision")

# define our boundary for red in BGR
# THE COLORS ARE IN [BLUE, GREEN, RED]
# DO NOT FORGET!
boundary = [
    ([120, 133, 0], [255, 255, 255])
]


while True:
    # grab frame
    frame = Util.getCurrentFrameMultiplier(0.5, 0.5)

    # set color boundaries
    lower = np.array(boundary[0][0], dtype="uint8")
    upper = np.array(boundary[0][1], dtype="uint8")

    # filter unwanted colors out of frame
    frame_mask = cv2.inRange(frame, lower, upper)
    filtered_frame = cv2.bitwise_and(frame, frame, mask=frame_mask)
    frame_edges = cv2.Canny(filtered_frame, 290, 100)

    # get dimensions
    dimensions = edge.objdimensions(frame_edges)
    middle = edge.middle(frame_edges)

    # write relevant data to NetworkTables
    visionTable.putNumber("offset", middle)
    visionTable.putValue("dimensions-px-x", dimensions[0])
    visionTable.putValue("dimensions-px-y", dimensions[1])

    print("Offset: " + str(middle))
    print("dimensions: " + str(dimensions))

    # print("Midpoint: " + str(edge.middle(frame_edges)))
    # print(" :" + str(edge.objdimensions(frame_edges)))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

Util.cleanUp()

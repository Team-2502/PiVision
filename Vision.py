"""Vision module for 2017. Sends dimensions and location of reflective tape."""
import cv2
import numpy as np
import Util
import EdgeTest as edge
import logging
from networktables import NetworkTables
import asyncio

EVENT_LOOP = asyncio.get_event_loop()

# turn into a client to connect to a robot
# The robot should have a static IP
NetworkTables.initialize(server='10.25.2.91')

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

async def putData(middle, dimensions, shouldBeLogging):
    # write relevant data to NetworkTables
    visionTable.putNumber("offset", -1 * middle)  # we multiply by -1 because the roborio needs to move backwards
    visionTable.putValue("dimensions-px-x", dimensions[0])
    visionTable.putValue("dimensions-px-y", dimensions[1])

    if shouldBeLogging:
        print("Offset: " + str(middle))
        print("dimensions: " + str(dimensions))

def processFrame():
    global EVENT_LOOP

    # grab frame
    frame = Util.getCurrentFrameMultiplier(0.5, 0.5)

    # set color boundaries
    lower = np.array(boundary[0][0], dtype="uint8")
    upper = np.array(boundary[0][1], dtype="uint8")

    # get dimensions
    dimensions = edge.objdimensions(frame_edges)
    middle = edge.middle(frame_edges)
    EVENT_LOOP.ensure_future(putData(middle, dimensions, True))

EVENT_LOOP.ensure_future(processFrame())
EVENT_LOOP.run_forever()

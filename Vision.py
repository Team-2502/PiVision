import cv2
import numpy as np
from Utils import PiCamera
import EdgeTest as edge
from networktables import NetworkTables
import time
import sys

MULTIPLIER = 0.5

# define our boundary for red in BGR
# THE COLORS ARE IN [BLUE, GREEN, RED]
# DO NOT FORGET!
boundary = [
    ([120, 133, 0], [255, 255, 255])
]

lower = np.array(boundary[0][0], dtype="uint8")
upper = np.array(boundary[0][1], dtype="uint8")

starttime = None
begintime = time.time()
endtime = None

# Connect to RoboRIO via networktable
NetworkTables.initialize(server='roborio-2502-frc.local')
visionTable = NetworkTables.getTable('PiVision')

oldtime = time.time()
sequence = 0

offset = None

currentFPS = None

averageFPS = None

camera = PiCamera(0)

def getFrame():
    return np.rot90(camera.getCurrentFrameMultiplier(MULTIPLIER, MULTIPLIER))


frame = getFrame()
frame_mask = np.zeros(frame.shape)

while True:
    starttime = time.time()

    frame = getFrame()

    cv2.inRange(frame, lower, upper, frame_mask)

    offset = edge.middle(frame_mask)

    endtime = time.time()

    sequence += 1

    currentFPS = (1 / (endtime - starttime))
    averageFPS = (sequence / (endtime - begintime))

    if len(sys.argv) > 1:
        print("offset:", offset)
        print("fps:", currentFPS)
        print("avgfps:", averageFPS)
        print()

    if len(sys.argv) > 2:
        cv2.imshow("vision", frame_mask)

    if len(sys.argv) > 3:
        cv2.imshow("camera", frame)

    visionTable.putNumber("robot_offset", float(offset))
    visionTable.putNumber("fps", currentFPS)
    visionTable.putNumber("avgfps", averageFPS)
    visionTable.putNumber("offset", float(offset))



Utils.cleanUp()

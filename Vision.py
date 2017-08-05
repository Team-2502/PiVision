import cv2
import numpy as np
from Utils import PiCamera
import EdgeTest as edge
from networktables import NetworkTables
from Utils import nones
import Utils
from EdgeTest import overlay
import time

# define our boundary for red in BGR
# THE COLORS ARE IN [BLUE, GREEN, RED]
# DO NOT FORGET!
boundary = [
    ([120, 133, 0], [255, 255, 255])
]

lower = np.array(boundary[0][0], dtype="uint8")
upper = np.array(boundary[0][1], dtype="uint8")

cams = [PiCamera(0)]
##### How many cameras are we looking a
camnum = 1
#####
# for x in range(camnum):
#    cams.append(PiCamera(x))



# Initalize variables
base = nones(camnum)
frames = base
frame_mask = base
filtered_frame = base
frame_edges = base

# Connect to RoboRIO via networktable
NetworkTables.initialize(server='roborio-2502-frc.local')
visionTable = NetworkTables.getTable('PiVision')

oldtime = time.time() * 1000
sequence = 0
starttime = oldtime
height = (None, None)
offset = (None, None)
while True:
    # open eyes
    for x, cam in enumerate(cams):
        frames[x] = np.rot90(cam.getCurrentFrameMultiplier(0.5, 0.5), 3)

    # think about what i am seeing
    for camnum, frame in enumerate(frames):
        # ignore irrelevant colors
        frame_mask[camnum] = cv2.inRange(frame, lower, upper)
        offset = edge.middle(frame_mask[camnum], True)
        height = edge.height(frame_mask[camnum], True)

        # print(offset[0])
        # cv2.imshow(str(camnum), frames[camnum])

        # print("Midpoint: " + str(edge.middle(frame_edges[camnum])))
    currenttime = time.time() * 1000
    for x, frame_edge in enumerate(frame_mask):
        visionTable.putNumber("offset", float(offset[0]))
        visionTable.putNumber("sequence", float(sequence))
        visionTable.putNumber("time", float(currenttime - starttime))
        visionTable.putNumber("timeelapsed", float(currenttime - oldtime))
        visionTable.putNumber("height", float(height[0]))
        oldtime = currenttime
        # pass
    sequence += 1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

Utils.cleanUp()

import cv2
import numpy as np
from Utils import PiCamera
import EdgeTest as edge
from networktables import NetworkTables
from Utils import nones

# define our boundary for red in BGR
# THE COLORS ARE IN [BLUE, GREEN, RED]
# DO NOT FORGET!
boundary = [
    ([120, 133, 0],[255, 255, 255])
]

lower = np.array(boundary[0][0], dtype = "uint8")
upper = np.array(boundary[0][1], dtype = "uint8")

cams = [PiCamera(0)]
##### How many cameras are we looking a
camnum = 1
#####
#for x in range(camnum):
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

while True:
    # open eyes
    for x, cam in enumerate(cams):
        frames[x] = cam.getCurrentFrameMultiplier(0.5, 0.5)

    # think about what i am seeing
    for camnum, frame in enumerate(frames):
        # ignore irrelevant colors
        frame_mask[camnum] = cv2.inRange(frame, lower, upper)
        filtered_frame[camnum] = cv2.bitwise_and(frame, frame, mask = frame_mask[camnum])
        frame_edges[camnum] = cv2.cvtColor(filtered_frame[camnum], cv2.COLOR_BGR2GRAY)
        
        offset = edge.middle(frame_edges[camnum])
        print(offset)
        cv2.imshow(str(camnum), frame_edges[camnum])
        
        # print("Midpoint: " + str(edge.middle(frame_edges[camnum])))

    for x, frame_edge in enumerate(frame_edges):
        #visionTable.putNumber("offset", edge.middle(frame_edge))
        pass

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

Util.cleanUp()

import cv2
import numpy as np
from Utils import PiCamera
import EdgeTest as edge
from networktables import NetworkTables
from Utils import nones
import Utils
from EdgeTest import overlay
import time
import sys

enableLiveFeed = False
enableTerminalLogging = False
if len(sys.argv) > 1:
    enableLiveFeed = True

if len(sys.argv) > 2:
    enableTerminalLogging = True


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
starttime = oldtime/1000
height = (None, None)
offset = (None, None)

def getFrame():
    multiplier = 0.5
    return np.rot90(cam.getCurrentFrameMultiplier(0.125, 0.125), 3)
while True:
    if sequence % 1000 == 1:
        print("Still running good")
    # open eyes
    for x, cam in enumerate(cams):
        if sequence == 0:
            try:
                frames[x] = getFrame()
            except AttributeError:
                print("ERROR: Another vision process is running.\nTo fix this error, run\n$ killall python")
                sys.exit()
        frames[x] = getFrame()

    # think about what i am seeing
    for camnum, frame in enumerate(frames):
        # ignore irrelevant colors
        frame_mask[camnum] = cv2.inRange(frame, lower, upper)
        offset = edge.middle(frame_mask[camnum], False) # Biggest drain on FPS
        height = edge.height(frame_mask[camnum], False) # Also probably a big drain

        # print(offset[0])
        if enableLiveFeed:
            cv2.imshow(str(camnum), frames[camnum])
	if enableTerminalLogging:
            print("Height:" , height)
            print("Offset:", offset)
            print("###")

        # print("Midpoint: " + str(edge.middle(frame_edges[camnum])))
    currenttime = time.time() * 1000
    for x, frame_edge in enumerate(frame_mask):
        visionTable.putNumber("robot_offset", float(offset))
        visionTable.putNumber("fps", float(sequence/(time.time() - starttime)))
        visionTable.putNumber("height", float(height))
        visionTable.putNumber("offset", float(offset))
        # visionTable.putNumber("fps", float(sequence / (time.time() - starttime)))
        oldtime = currenttime
        # pass
    sequence += 1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

Utils.cleanUp()

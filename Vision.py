import cv2
import numpy as np
from grip import GripPipeline
import time
import asyncio
from networktables import NetworkTables
import EdgeTest as edge
cap0 = cv2.VideoCapture(0)
cap1 = cv2.VideoCapture(1)
pipeline = GripPipeline()

NetworkTables.initialize(server='10.25.2.91')
table = NetworkTables.getTable('PiTable')


def putData(cam1data, cam2data):

    table.putNumber("offset1", cam1data)
    print(cam1data)
    print(cam2data)
    table.putNumber("offset2", cam2data)

def translateContours(contours):
    pic_contours = np.zeros((240, 320))
    for contour in contours:
        for pixel in contour:
            for x, y in pixel:
                pic_contours[x, y] = 255
    return pic_contours
    
def interpretData():
    _, frame0 = cap0.read()
    _, frame1 = cap1.read()
    pipeline.process(frame0, frame1)

    contours0_array = translateContours(pipeline.filter_contours_0_output)
    contours1_array = translateContours(pipeline.filter_contours_1_output)
    
    
    mid0 = edge.middle(contours0_array)
    mid1 = edge.middle(contours1_array)

    putData(mid0, mid1)
    time.sleep(0.5)
    
while True:
    interpretData()
    cv2.imshow("1", pic_contours_1)
    cv2.waitKey(5000)
    cv2.destroyAllWindows()

cap0.release()
cap1.release()

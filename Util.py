import cv2
import numpy as np

# Initialize a camera capture.
capture = cv2.VideoCapture(0)


# Capture a few frames to get the camera used to the light.
i = 0
while(i < 10):
    # @var ret - Returns whether or not the frame was read properly.
    # @var frame - The current frame.
    ret, frame = capture.read()
    i = i + 1

def isDataReady():
#    return ser.inWaiting() > 0
    return False

def sendData(data):
#    ser.write(data)
    return

def getData():
#    return ser.read(1)
    return 0

def getCurrentFrame():
    ret, frame = capture.read()
    return frame

def getCurrentFrameResized(x, y):
    return cv2.resize(getCurrentFrame(), (x, y))

def getCurrentFrameMultiplier(x, y):
    frame = getCurrentFrame()
    height, width, channels = frame.shape
    return cv2.resize(frame, (int(width * x), int(height * y)))
#    return cv2.resize(frame, (frame.get(3) * x, frame.get(4) * y))

def modifyThreshold(frame, value):
    ret, threshold = cv2.threshold(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), value, 255, cv2.THRESH_BINARY)
    return threshold

def filterContours(countours, size):
    countours2 = np.empty(0)
    for countour in countours:
        if cv2.countourArea(countour) > size:
            countours2 = np.append(countour)
    return countours2

def cleanUp():
#    ser.close()
    capture.release()
    cv2.destroyAllWindows()

def nw(name):
    #cv2.namedWindow(name, cv2.WINDOW_NORMAL)
    cv2.namedWindow(name, cv2.WINDOW_NORMAL)

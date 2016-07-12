import cv2
import serial
import numpy as np

# Initialize a camera capture.
capture = cv2.VideoCapture(0)
# Initialize the serial connection for communication between the RPi and the RoboRio.
ser = serial.Serial(port='/dev/ttyAMA0', 
                    baudrate=14400, 
                    parity=serial.PARITY_NONE, 
                    stopbits=serial.STOPBITS_ONE, 
                    bytesyze=serial.EIGHTBITS)

# Open the connection.
ser.open()

# Capture a few frames to get the camera used to the light.
i = 0
while(i < 30):
    # @var ret - Returns whether or not the frame was read properly.
    # @var frame - The current frame.
    ret, frame = capture.read()

def isDataReady():
    return ser.inWaiting() > 0

def sendData(data):
    ser.write(data)

def getData():
    return ser.read(1)

def getCurrentFrame():
    ret, frame = capture.read()
    return frame

def getCurrentFrameResized(x, y):
    return cv2.resize(getCurrentFrame(), (x, y))

def getCurrentFrameMultiplier(x, y):
    frame = getCurrentFrame()
    return cv2.resize(frame, (frame.get(3) * x, frame.get(4) * y))

def modifyThreshold(frame, value):
    ret, threshold = cv2.threshold(cv2.cvtColor(x, cv2.COLOR_BGR2GRAY), y, 255, cv2.THRESH_BINARY)
    return threshold

def filterContours(countours, size):
    countours2 = np.empty(0)
    for countour in countours:
        if cv2.countourArea(countour) > size:
            countours2 = np.append(countour)
    return countours2

def cleanUp():
    ser.close()
    cap.release()
    cv2.destroyAllWindows()

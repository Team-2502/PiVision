import cv2
import numpy as np

# Calculate the average of a list of numbers
def avgCalc(widths):
    avg = 0
    for width in widths:
        avg = avg + width
    return avg/len(widths)

# take in a numpy array that represents the edge detection as run on an image and calculates the average width of the reflective tape
# this is useful because the boiler's reflective tape is wider than the gear's reflective tape

def widthCalc(img):
    widths = []
    for rownum, row in enumerate(img):
        if np.sum(row) != 0:
            counter = []
            for col, pixel in enumerate(img[rownum]):
                if pixel > 100:
                    counter.append(col)
            if len(counter) >= 2:
                widths.append(counter[-1] - counter[0])
    return widths

# Load tape.jpg unchanged
img = cv2.imread('tape.jpg', -1)

# Run the Canny Edge Detection Algorithm
edges = cv2.Canny(img,100,200)

# Turn the edge detected image on its side
edgesSide = np.rot90(edges)

avg_width = avgCalc(widthCalc(edges))
avg_height = avgCalc(widthCalc(edgesSide))

print(avg_width)
print(avg_height)

if avg_width > avg_height:
    print("gear")
else:
    print("boiler")

cv2.imshow("edges", edges)
cv2.imshow("edges rotated 90 degrees", edgesSide)




cv2.waitKey(0)
cv2.destroyAllWindows()

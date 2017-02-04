import cv2
import numpy as np

TEST_IMGS = ['HC0_N.png','VC0_C.png','VL0_G.png', 'tape.jpg']

# When using edge detection, follow these 2 tips
# 1. Grayscale helps reduce falsely detected edges
# 2. 283 as the x value and 100 as the y value in cv2.Canny(img, x, y) works well to also reduce falsely detected images

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

def isGear(img):
    # Run the Canny Edge Detection Algorithm
    edges = cv2.Canny(img,283,100)

    # Turn the edge detected image on its side
    edgesSide = np.rot90(edges)

    avg_width = avgCalc(widthCalc(edges))
    avg_height = avgCalc(widthCalc(edgesSide))
    print("Average width: " + str(avg_width))
    print("Average height: " + str(avg_height))

    if avg_width < avg_height:
        return True
    else:
        return False

def isBoiler(img):
    # Run the Canny Edge Detection Algorithm
    edges = cv2.Canny(img, 283, 100)

    # Turn the edge detected image on its side
    edgesSide = np.rot90(edges)

    avg_width = avgCalc(widthCalc(edges))
    avg_height = avgCalc(widthCalc(edgesSide))

    if avg_width > avg_height:
        return True
    else:
        return False

if __name__ == "__main__":
    for image in TEST_IMGS:
        # Load tape.jpg unchanged
        image_matrix = cv2.imread(image, 0)
        cv2.imshow(image, cv2.Canny(image_matrix, 283, 100))
        boiler = isBoiler(image_matrix)
        gear = isGear(image_matrix)
        if boiler:
            print(image + " is a boiler")
        elif gear:
            print(image + " is a gear holder")
        else:
            print(image + " is neither")

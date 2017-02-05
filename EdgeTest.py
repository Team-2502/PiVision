import cv2
import numpy as np

TEST_IMGS = ['HC0_N.png','VC0_C.png','VL0_G.png', 'tape.jpg']

# When using edge detection, follow these 2 tips
# 1. Grayscale helps reduce falsely detected edges
# 2. 283 as the x value and 100 as the y value in cv2.Canny(img, x, y) works well to also reduce falsely detected images

# Calculate the average of a list of numbers
def avgCalc(widths):
    try:
        avg = 0
        for width in widths:
            avg = avg + width
        return avg/len(widths)
    except:
        return 0

# take in a numpy array that represents the edge detection as run on an image and calculates the average width of the reflective tape
# this is useful because the boiler's reflective tape is wider than the gear's reflective tape

def genBoundary(img):
    boundaries = []
    for rownum, row in enumerate(img):
        if np.sum(row) != 0:
            counter = []
            for col, pixel in enumerate(img[rownum]):
                if pixel > 100:
                    counter.append(col)
            if len(counter) > 2:
                boundaries.append((counter[0], counter[-1]))
    return boundaries

def widthCalc(img):
    boundaries = genBoundary(img)
    widths = []
    for (l_boundary, r_boundary) in boundaries:
        widths.append(r_boundary - l_boundary)
    return widths


def objdimensions(img):
    # Run the Canny Edge Detection Algorithm
    edges = cv2.Canny(img,283,100)

    # Turn the edge detected image on its side
    edgesSide = np.rot90(edges)

    avg_width = avgCalc(widthCalc(edges))
    avg_height = avgCalc(widthCalc(edgesSide))

    return [avg_width, avg_height]

def middle(img):
    midpoint = int(img.shape[1]/2)
    boundaries = genBoundary(img)
    widths = widthCalc(img)
    mid_widths = []
    for num, (l_bound, r_bound) in enumerate(boundaries):
        mid_widths.append(r_bound - 0.5*widths[num])

    mid_width = avgCalc(mid_widths)
    return mid_width - boundaries


if __name__ == "__main__":
    for image in TEST_IMGS:
        # Load tape.jpg unchanged
        image_matrix = cv2.imread(image, 0)
        cv2.imshow(image, cv2.Canny(image_matrix, 283, 100))
        dimensions = objdimensions(image_matrix)
        print(image + " is " + str(middle(image_matrix)) + " off center")
        if dimensions[0] > dimensions[1]:
            print(image + " is a boiler")
        elif dimensions[0] < dimensions[1]:
            print(image + " is a gear holder")
        else:
            print(image + " is neither")

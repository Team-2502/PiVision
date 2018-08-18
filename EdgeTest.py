import cv2
import numpy as np
import random

TEST_IMGS = ['HC0_N.png','VC0_C.png','VL0_G.png', 'tape.jpg', 'testimg1.png', 'testimg2.png']

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


def widthCalc(img, debug=False):
    boundaries = genBoundary(img)
    widths = []
    for (l_boundary, r_boundary) in boundaries:
        widths.append(r_boundary - l_boundary)
    if debug:
        return (widths, boundaries)
    return widths


def genBoundary(img, row_min = 500):
    boundaries = []
    for y, row in enumerate(img):
        if np.sum(row) > row_min:
            counter = []
            for x, pixel in enumerate(img[y]):
                if pixel > 100:
                    counter.append(x)
            if len(counter) > 2:
                boundaries.append((counter[0], counter[-1]))
    return boundaries


def height(mask, debug=False):
    """Feed me only masks!"""

    maskside = np.rot90(mask)

    widths, boundaries = widthCalc(maskside, True)

    avg_height = avgCalc(widths)

    if debug:
        l_bounds = [l_boundary for (l_boundary, r_boundary) in boundaries]
        r_bounds = [r_boundary for (l_boundary, r_boundary) in boundaries]
        l_bound = (0.5 * (sum(l_bounds) / len(boundaries)) + 0.5 * min(l_bounds))
        r_bound = (0.5 * (sum(r_bounds) / len(boundaries)) + 0.5 * max(r_bounds))
        # l_bound = min(l_bounds)
        # r_bound = max(r_bounds)

        print(l_bound)
        print(r_bound)

        max_lbound_graph = [l_bound for _ in range(maskside.shape[1] - 2)]
        max_rbound_graph = [r_bound for _ in range(maskside.shape[1] - 2)]
        return avg_height, np.fliplr(draw_graph(max_rbound_graph, draw_graph(max_lbound_graph, maskside.T, False).T, False).T)

    return avg_height

def dist_score(optimal_height, mask):
    """
    :param optimal_height: How high we can expect the tape to be (in pixels) for best shooting 
    :param mask: The colour mask
    :return: Shows how off target we are. Smaller = further, bigger = closer, 1 = perfect
    """
    current_height = height(mask)
    return current_height / optimal_height

def overlay(edge, image):
    for x, row in enumerate(image):
        for y, pixel in enumerate(row):
            x = x-1
            y = y-1
            try:
                if edge[x, y] != 0:
                    image[x, y] = edge[x,y]
            except IndexError:
                pass
    return image

def draw_graph(list, image, color):
    """Draws on image using the values inside list"""
    image = image.T
    plate = np.zeros(image.shape)
    print(plate.shape)
    for x, y in enumerate(list):
        if color:
            plate[x, y] = np.array([255,255,255])
        elif not color:
            plate[int(x), int(y)] = 255
    image = image
    return overlay(plate, image)

def middle(img, debug=False):
    # add up all the values in each column, put into 1d numpy array
    avg = 0
    graph = np.zeros(img.shape[1])
    for x, column in enumerate(img.T):
        graph[x] = np.sum(column)/np.sum(img)
    
    # weighted average of values in numpy array. Value: x val; Weight: sum
    for x, val in enumerate(graph):
        avg += x * val
    
    avg = avg - (img.shape[1]/2)
    if not debug:
        return avg
    else:
        return [avg, draw_graph(graph, img, False)]


if __name__ == "__main__":

    boundary = [
        ([120, 133, 0], [255, 255, 255])
    ]

    lower = np.array(boundary[0][0], dtype="uint8")
    upper = np.array(boundary[0][1], dtype="uint8")
    for image in TEST_IMGS:
        # Load tape.jpg unchanged
        image_matrix = cv2.imread(image)
        # graph = []
        # graph.append(random.randrange(1, image_matrix.shape[0]))
        # for _ in range(image_matrix.shape[1]-2):
        #     if graph[-1]+1 >= image_matrix.shape[0]-2:
        #         graph.append(1)
        #     else:
        #         graph.append(graph[-1]+1)
        # print(len(graph))
        # print(max(graph))

        # graph.append(image_matrix.shape[0]/2)

        filtered = cv2.inRange(image_matrix, lower, upper)
        heightnum, displaythingy = height(filtered, True)
        # cv2.imshow(image, draw_graph(graph, filtered, False).T)
        cv2.imshow(image, displaythingy)
        cv2.waitKey()
        print(image + " is " + str(middle(image_matrix)) + " off center")
        print(image + " height is " + str(heightnum))

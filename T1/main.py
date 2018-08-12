import cv2 as cv
import numpy as np
import collections as col

THRESHOLD = 150
T = 0.5 # args[]


# Creates an auxiliar 2Dimensional array which will be used for pixel labelling
def createsAuxMatrix(width, height):
    Pixel = col.namedtuple('Pixel', 'x, y, label')
    row = []
    cols = []

    for y in range(height):
        for x in range(width):
            p = Pixel(x, y, -1)
            row.append(p)

        cols.append(row)
        row = []

    return cols


def main():
    # Loads an image
    img = cv.imread('./img/yui.jpg') # args[]
    width, height, channel = img.shape

    img = binarization(img, width, height, THRESHOLD, channel)

    # Save modified image
    cv.imwrite('./img/yuibinarizado2.png', img) # args[]


# Apply binarization 
def binarization(img, width, height, threshold, channel):
    for h in range(height):
        for w in range(width):
            pixel = img[w, h]

            # BGR or grayscale?
            if channel == 3:
                # s = (int(pixel[0]) + int(pixel[1]) + int(pixel[2])) / 3                   # Simple conversion
                s = (int(0.114 * pixel[0]) + int(0.587 * pixel[1]) + int(0.299 * pixel[2]))  # Right conversion
            else:
                s = int(pixel[0])

            # Within threshold?
            if s > threshold:
                pixel = [255, 255, 255]
            else:
                pixel = [0, 0, 0]

            img[w, h] = pixel

    return img


# Calculates the distance in color spectrum between two pixels for BGR channels. Neighborhood 4
def calculateDistance(img, p, width, height, direction):
    pixelroot = img[p.y][p.x] 

    if direction == 'top' and p.y - 1 >= 0 :
        pixelchild = img[p.y - 1][p.x]

    return spectrumDifference(pixelroot, pixelchild)
    

# Returns the difference in spectrum between two 3 channels pixels 
def spectrumDifference(pixelroot, pixelchild):
    return abs(pixelroot[0] - pixelchild[0]) + abs(pixelroot[1] - pixelchild[1]) + abs(pixelroot[2] - pixelchild[2])


def blobdetection(img, width, height):
    pixels = createsAuxMatrix(width, height)
    label = 0
    stack = []

    for y in range(height):
        for x in range(width):
            
            # Does this pixel was visited before?
            if pixels[y][x].label == -1
                pixels[y][x].label = label
                
                stack.append(pixels[y][x])

                # While stack is not empty, verify neighbors from pixel
                while len(stack) != 0:
                    p = stack.pop()

                    # Does its neighboard pixels belongs to the same blob/label?
                    # Top
                    if p.y - 1 >= 0:
                        dist = calculateDistance(img, p, width, height, 'top')
                        if dist <= T: #Yes
                            pixels[p.y-1][p.x].label = label
                            stack.append(pixels[p.y-1][p.x])
                    # Right

                    # Bottom

                    # Left

                
                label++




# Initializes execution
main()
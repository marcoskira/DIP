import cv2 as cv
import numpy as np
import collections as col
import random as rand

# Classes
from classes import Pixel
from classes import Blob

MAXCHANNELVALUE = 255
QTYCHANNEL = 3
THRESHOLD = 0.5

blobs = [] #Blobs queue


# Receive a pixel in BGR and returns a conversion to grayscale
def convertsToGrayscale(pixel):
    return (int(0.114 * pixel[0]) + int(0.587 * pixel[1]) + int(0.299 * pixel[2]))



# Creates an auxiliar 2Dimensional array which will be used for pixel labelling
def createsAuxMatrix(width, height):
    row = []
    cols = []

    for y in range(height):
        for x in range(width):
            p = Pixel(x, y, -1)
            row.append(p)

        cols.append(row)
        row = []

    return cols


# Calculates the distance in color spectrum between two pixels for BGR channels. Neighborhood 4
def calculateDistance(img, seed_x,seed_y, child_x, child_y):
    seed_pixel = img[seed_y][seed_x] 
    child_pixel = img[child_y][child_x]

    return abs(seed_pixel[0] - child_pixel[0]) + abs(seed_pixel[1] - child_pixel[1]) + abs(seed_pixel[2] - child_pixel[2]) / (MAXCHANNELVALUE * QTYCHANNEL)



# Detects and labells all blobs in a given image and returns a 2Dimensional array mapping this blobs
def blobdetection(img, width, height):
    pixels = createsAuxMatrix(width, height)
    label = 0
    pixels_per_blob = 0
    stack = []

    for y in range(height):
        for x in range(width):
            
            # Does this pixel was visited before?
            if pixels[y][x].label == -1:
                pixels[y][x].label = label

                
                stack.append(pixels[y][x]) # Seed pixel
                b = Blob(label) # New blob is found

                # While stack is not empty, verify neighbors from pixel
                while len(stack) != 0:
                    p = stack.pop()

                    # Add it to blob's pixel queue
                    b.pixels_list.append(p)
                    pixels_per_blob += 1

                    # Evaluates if seed pixel neighbors belongs to the same blob:
                    # Verifies if X and Y axis are within range of image
                    # Top 
                    if p.y - 1 >= 0:
                         # Neighbor pixel was already labelled?
                        if pixels[p.y-1][p.x].label == -1:
                            dist = calculateDistance(img, p.x, p.y, p.x, p.y-1)
                            if dist <= THRESHOLD: 
                                pixels[p.y-1][p.x].label = label
                                stack.append(pixels[p.y-1][p.x])
                    # Right
                    if p.x + 1 < width:
                        if pixels[p.y][p.x+1].label == -1:
                            dist = calculateDistance(img, p.x, p.y, p.x+1, p.y)
                            if dist <= THRESHOLD:
                                pixels[p.y][p.x+1].label = label
                                stack.append(pixels[p.y][p.x+1])
                    # Bottom
                    if p.y + 1 < height:
                        if pixels[p.y+1][p.x].label == -1:
                            dist = calculateDistance(img, p.x, p.y, p.x, p.y+1)
                            if dist <= THRESHOLD:
                                pixels[p.y+1][p.x].label = label
                                stack.append(pixels[p.y+1][p.x])
                    # Left
                    if p.x - 1 >= 0:
                        if pixels[p.y][p.x-1].label == -1:
                            dist = calculateDistance(img, p.x, p.y, p.x-1, p.y)
                            if dist <= THRESHOLD:
                                pixels[p.y][p.x-1].label = label
                                stack.append(pixels[p.y][p.x-1])

                # If there is no more pixels in the stack. then all pixels from the blob was found
                b.pixels_qty = pixels_per_blob
                blobs.append(b)
                
                # Reset values for next iteration
                pixels_per_blob = 0
                label += 1
                #labelcolor = [rand.randint(0,255), rand.randint(0,255), rand.randint(0,255)]

    return pixels




# Initializes execution
print len(blobs)
img = cv.imread('./img/yui.jpg') # args[]
width, height, channel = img.shape

blob_mapping = blobdetection(img, width, height)

print len(blobs)
import cv2 as cv
import numpy as np
import collections as col


height = 2
width = 3

Pixel = col.namedtuple('Pixel', 'x, y, label')

row = []
cols = []

for y in range(height):
    for x in range(width):
        p = Pixel(x, y, -1)
        row.append(p)

    cols.append(row)
    row = []


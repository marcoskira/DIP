import cv2 as cv
import time

# Classes
from classes import Pixel
from classes import Blob


INPUT_IMAGE = "./img/arroz.jpg"

# Ajuste estes parametros
NEGATIVO = 1
THRESHOLD = 200
ALTURA_MIN = 5
LARGURA_MIN = 5
N_PIXELS_MIN = 20
FOREGROUND = 0
BACKGROUND = 255

list_of_blobs = []



def drawRectangle(img):
    print "Blobs qty: ", len(list_of_blobs)

    for i in xrange(0, len(list_of_blobs)):
        #print "Blobs qty: ", len(list_of_blobs)
        last_pos = (len(list_of_blobs[i].pixels_list) - 1)
        cv.rectangle(img, (list_of_blobs[i].pixels_list[0].x, list_of_blobs[i].pixels_list[0].y), (list_of_blobs[i].pixels_list[last_pos].x, list_of_blobs[i].pixels_list[last_pos].y), (0,0,255), 2)

        #print "Pixel: ", list_of_blobs[i].pixels_list[0].x, list_of_blobs[i].pixels_list[0].y, list_of_blobs[i].pixels_list[last_pos].x, list_of_blobs[i].pixels_list[last_pos].y

    return img



# Calculates the distance in color spectrum between two pixels for BGR channels. Neighborhood 4
def calculateDistance(img, seed_x, seed_y, child_x, child_y):
    seed_pixel = img[seed_y][seed_x]
    child_pixel = img[child_y][child_x]

    return abs(int(seed_pixel[0]) - int(child_pixel[0])) + abs(int(seed_pixel[1]) - int(child_pixel[1])) + abs(int(seed_pixel[2]) - int(child_pixel[2]))


# Creates an auxiliar 2Dimensional array which will be used for pixel labelling
def createsAuxMatrix(width, height):
    row = []
    cols = []

    for y in xrange(height):
        for x in xrange(width):
            p = Pixel(x, y, -1)
            row.append(p)

        cols.append(row)
        row = []

    #print "X: ", cols[20][25].x, "Y: ", cols[20][25].y

    return cols


def binariza (img, threshold, height, width, channel):

    for h in xrange(height):
        for w in xrange(width):
            pixel = img[h, w]

            # BGR or grayscale?
            if channel == 3:
                s = (int(0.114 * pixel[0]) + int(0.587 * pixel[1]) + int(0.299 * pixel[2]))
            else:
                s = int(pixel[0])

            # Within threshold?
            if s  > threshold:
                pixel = [BACKGROUND, BACKGROUND, BACKGROUND]
            else:
                pixel = [FOREGROUND, FOREGROUND,FOREGROUND]

            img[h, w] = pixel

    return img



def rotula(img, largura_min, altura_min, n_pixels_min, height, width):

    pixels = createsAuxMatrix(width, height)
    label = 0
    n_componentes = 0
    pixels_per_blob = 0
    stack = []

    for y in xrange(height):
        for x in xrange(width):
            

            pix = img[y,x]
            # Does this pixel was visited before AND is this a foreground?
            if pixels[y][x].label == -1 and pix[0] == FOREGROUND:
                pixels[y][x].label = label

                
                stack.append(pixels[y][x]) # Seed pixel
                b = Blob(label) # New blob is found

                # While stack is not empty, verify neighbors from pixel
                while len(stack) != 0:
                    p = stack.pop()

                    # Add it to blob's pixel queue
                    b.pixels_list.append(p)
                    pixels_per_blob += 1

                    # Top 
                    if p.y - 1 >= 0:
                         # Neighbor pixel was already labelled?
                        if pixels[p.y-1][p.x].label == -1:
                            dist = calculateDistance(img, p.x, p.y, p.x, p.y-1)
                            if dist <= THRESHOLD: 
                                pixels[p.y-1][p.x].label = label
                                stack.append(pixels[p.y-1][p.x])
                                #pixels_per_blob += 1
                    # Right
                    if p.x + 1 < width:
                        if pixels[p.y][p.x+1].label == -1:
                            dist = calculateDistance(img, p.x, p.y, p.x+1, p.y)
                            if dist <= THRESHOLD:
                                pixels[p.y][p.x+1].label = label
                                stack.append(pixels[p.y][p.x+1])
                                #pixels_per_blob += 1
                    # Bottom
                    if p.y + 1 < height:
                        if pixels[p.y+1][p.x].label == -1:
                            dist = calculateDistance(img, p.x, p.y, p.x, p.y+1)
                            if dist <= THRESHOLD:
                                pixels[p.y+1][p.x].label = label
                                stack.append(pixels[p.y+1][p.x])
                                #pixels_per_blob += 1
                    # Left
                    if p.x - 1 >= 0:
                        if pixels[p.y][p.x-1].label == -1:
                            dist = calculateDistance(img, p.x, p.y, p.x-1, p.y)
                            if dist <= THRESHOLD:
                                pixels[p.y][p.x-1].label = label
                                stack.append(pixels[p.y][p.x-1])
                                #pixels_per_blob += 1

                # If there is no more pixels in the stack. then all pixels from the blob was found
                b.pixels_qty = pixels_per_blob
                
                # If blob doesn't have minimum qty of pixels, ignore it
                if b.pixels_qty >= N_PIXELS_MIN:
                    list_of_blobs.append(b)

                    print "Blob pixels qty: ", b.pixels_qty
                else:
                    label -= 1 #returns label
                
                # Reset values for next iteration
                pixels_per_blob = 0
                label += 1
                
    return len(list_of_blobs)


def negativeTransformation(img):
    return 255 - img

def paintBlobs(img):
    for i in xrange(len(list_of_blobs)):
        for j in xrange(len(list_of_blobs[i].pixels_list)):
            img[list_of_blobs[i].pixels_list[j].y, list_of_blobs[i].pixels_list[j].x] = [50]
    
    return img

def main ():

    img = cv.imread(INPUT_IMAGE)
    height, width, channel = img.shape


    # Image binarization
    imgout = binariza (img, THRESHOLD, height, width, channel)

    cv.imshow('Bin', imgout)
    cv.waitKey(0)
    cv.destroyAllWindows()

    if(NEGATIVO):
        img = negativeTransformation(img)


    cv.imshow('Negative', imgout)
    cv.waitKey(0)
    cv.destroyAllWindows()

    # n_componentes = rotula (imgout, LARGURA_MIN, ALTURA_MIN, N_PIXELS_MIN, height, width)
    # print n_componentes

    # #imgout = drawRectangle(img)
    # imgout = paintBlobs(imgout)
    # cv.imwrite('./img/02-binarizada.jpg', imgout)



main()

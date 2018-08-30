import cv2 as cv

# Classes
from classes import Pixel
from classes import Blob


INPUT_IMAGE = "./img/example.jpg"
WINDOWSIZE = 9


# Draws a rectangle around every detected blob
def drawsRectangle(img, height, width, list_of_blobs):

    for blob in list_of_blobs:

        min_x = width - 1
        min_y = height - 1
        max_x = 0
        max_y = 0


        for pixel in blob.pixels_list:     

            # Mininum X and Y
            if pixel.x < min_x:
                min_x = pixel.x

            if pixel.y < min_y:
                min_y = pixel.y
            
            # Maximum X and Y
            if pixel.x > max_x:
                max_x = pixel.x

            if pixel.y > max_y:
                max_y = pixel.y

        cv.rectangle(img,(min_x,min_y),(max_x,max_y),(0,0,255),2)
        
        # Reset values for next blob evaluation
        min_x = width - 1
        min_y = height - 1
        max_x = 0
        max_y = 0


    return img


# Calculates the distance in color spectrum between two pixels for BGR channels.
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

    return cols


# Apply binarization on a given image
def imgBinarization (img, threshold, height, width, channel):

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


# Detects blobs on a given image
def blobDetection(img, min_width, min_height, min_pixels_n, height, width):
    stack = []
    list_of_blobs = []
    pixels = createsAuxMatrix(width, height)
    label = 0
    pixels_per_blob = 0

    for y in xrange(height):
        for x in xrange(width):
            
            pix = img[y,x]
            # Does this pixel was never visited before AND is this a foreground? If yes, then we found a seed pixel of a blob
            if pixels[y][x].label == -1 and pix[0] == FOREGROUND:
                pixels[y][x].label = label
         
                stack.append(pixels[y][x]) # Seed pixel in put inside a stack
                b = Blob() 

                # While stack is not empty, verify neighbors from pixel which was never visited before
                while len(stack) != 0:
                    p = stack.pop()

                    # Add it to blob's pixel list
                    b.pixels_list.append(p)
                    pixels_per_blob += 1

                    # Neighboard 4
                    # Top 
                    if p.y - 1 >= 0:
                        if pixels[p.y-1][p.x].label == -1:
                            dist = calculateDistance(img, p.x, p.y, p.x, p.y-1)
                            if dist == 0: 
                                pixels[p.y-1][p.x].label = label
                                stack.append(pixels[p.y-1][p.x])
                    # Right
                    if p.x + 1 < width:
                        if pixels[p.y][p.x+1].label == -1:
                            dist = calculateDistance(img, p.x, p.y, p.x+1, p.y)
                            if dist == 0:
                                pixels[p.y][p.x+1].label = label
                                stack.append(pixels[p.y][p.x+1])
                    # Bottom
                    if p.y + 1 < height:
                        if pixels[p.y+1][p.x].label == -1:
                            dist = calculateDistance(img, p.x, p.y, p.x, p.y+1)
                            if dist == 0:
                                pixels[p.y+1][p.x].label = label
                                stack.append(pixels[p.y+1][p.x])
                    # Left
                    if p.x - 1 >= 0:
                        if pixels[p.y][p.x-1].label == -1:
                            dist = calculateDistance(img, p.x, p.y, p.x-1, p.y)
                            if dist == 0:
                                pixels[p.y][p.x-1].label = label
                                stack.append(pixels[p.y][p.x-1])


                # If there is no more pixels in the stack, then all pixels from this blob was found
                b.pixels_qty = pixels_per_blob

                
                # If blob doesn't have minimum qty of pixels, ignore it
                if b.pixels_qty >= min_pixels_n:
                    list_of_blobs.append(b)
                else:
                    label -= 1 #returns label
                
                # Reset values for next iteration
                pixels_per_blob = 0
                label += 1
                
    return list_of_blobs


# Paints pixels within a list of blobs in a image
def paintBlobs(img, list_of_blobs):
    for blob in list_of_blobs:
        for pixel in blob.pixels_list:
                img[pixel.y, pixel.x] = [0, 255, 0]

    return img

def blur1(img_original, img_blur, height, width, wsize):

    for h in xrange(height):
        for w in xrange(width):
            sum = [0,0,0]

            # Verifica se janela nao ultrapassa margens
            if (width - wsize/2 >= 0 and height - wsize/2 >= 0) and (width + wsize/2 < width and height + wsize/2 < height):
                # Percorre janela
                for h_window in xrange(height - wsize/2, height + wsize/2)
                    for w_window in xrange(width - wsize/2, width + wsize/2)
                        # Se for o pixel seed, ignora na soma
                        #if h_window != h and w_window != w:
                        pix = img_original[h_window][w_window]
                        sum[0] += pix[0]
                        sum[1] += pix[1]
                        sum[2] += pix[2]

            img_blur[h][w] = [sum[0] / (wsize * wsize), sum[1] / (wsize * wsize), sum[2] / (wsize * wsize)]
            sum = [0,0,0]

    return img_blur          






def main ():

    img_original = cv.imread(INPUT_IMAGE)
    img_blur = cv.imread(INPUT_IMAGE)
    height, width, channel = img_original.shape


    img_blur = blur1(img_original, img_blur, height, width, WINDOWSIZE)

    cv.imwrite('./img/01-blur.bmp', img_blur)



main()

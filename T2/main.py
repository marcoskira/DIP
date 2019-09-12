import cv2 as cv
import math

from classes import Pixel

INPUT_IMAGE = "./img/img.png"
WINDOWSIZE = 15

def create_integral_image(img, height, width):
    intimg = [[Pixel(0,0,0) for x in range(width)] for y in range(height)]

    for h in range(height):
        for w in range(width):

            # apply sum to all pixels, except the first one
            if w == 0 and h == 0:
                    intimg[h][w].b, intimg[h][w].g, intimg[h][w].r = int(img[h, w][0]), int(img[h, w][1]), int(img[h, w][2])
            else:
                # first row
                if h == 0:
                    intimg[h][w].b = int(img[h, w][0]) + intimg[h][w-1].b
                    intimg[h][w].g = int(img[h, w][1]) + intimg[h][w-1].g
                    intimg[h][w].r = int(img[h, w][2]) + intimg[h][w-1].r

                # first column
                elif w == 0:
                    intimg[h][w].b = int(img[h, w][0]) + intimg[h-1][w].b
                    intimg[h][w].g = int(img[h, w][1]) + intimg[h-1][w].g
                    intimg[h][w].r = int(img[h, w][2]) + intimg[h-1][w].r
                # others pixels
                else:
                    intimg[h][w].b = int(img[h][w][0]) + intimg[h-1][w].b + intimg[h][w-1].b - intimg[h-1][w-1].b
                    intimg[h][w].g = int(img[h][w][1]) + intimg[h-1][w].g + intimg[h][w-1].g - intimg[h-1][w-1].g
                    intimg[h][w].r = int(img[h][w][2]) + intimg[h-1][w].r + intimg[h][w-1].r - intimg[h-1][w-1].r

    return intimg


def meanfilter_simple(img_original, img_blur, height, width, wsize):
    sum = [0,0,0]

    for h in range(height):
        for w in range(width):
            # Check if window size don't exceeds image margins
            if (w - int(math.floor(wsize/2)) >= 0 and h - int(math.floor(wsize/2)) >= 0) and (w + int(math.floor(wsize/2)) < width and h + int(math.floor(wsize/2)) < height):

                # Analyze every pixel on window
                for h_window in range(h - int(math.floor(wsize/2)), h + int(math.floor(wsize/2))):
                    for w_window in range(w - int(math.floor(wsize/2)), w + int(math.floor(wsize/2))):
                        pix = img_original[h_window][w_window]
                        sum[0] += pix[0]
                        sum[1] += pix[1]
                        sum[2] += pix[2]

            # Apply blur on every channel
            img_blur[h][w] = [sum[0] / (wsize * wsize), sum[1] / (wsize * wsize), sum[2] / (wsize * wsize)]
            sum = [0,0,0]

    return img_blur


def meanfilter_integral(intimg, imgblur, height, width, wsize):
    wsize2 = int(math.floor(wsize/2))

    for h in range(height):
        for w in range(width):

            # Check if window size don't exceeds image margins
            if w - wsize2 >= 0 and h - wsize2 >= 0 and w + wsize2 < width and h + wsize2 < height:
                # finds the mean of all the 3 channels within window size

                imgblur[h, w][0] = round((intimg[h + wsize2][w + wsize2].b - intimg[h - wsize2][w + wsize2].b - intimg[h + wsize2][w - wsize2].b + intimg[h - wsize2][w - wsize2].b) / (wsize * wsize))
                imgblur[h, w][1] = round((intimg[h + wsize2][w + wsize2].g - intimg[h - wsize2][w + wsize2].g - intimg[h + wsize2][w - wsize2].g + intimg[h - wsize2][w - wsize2].g) / (wsize * wsize))
                imgblur[h, w][2] = round((intimg[h + wsize2][w + wsize2].r - intimg[h - wsize2][w + wsize2].r - intimg[h + wsize2][w - wsize2].r + intimg[h - wsize2][w - wsize2].r) / (wsize * wsize))
            
            else:
                # if window size exceeds image margins, apply a black background
                imgblur[h, w] = [0, 0, 0]

    return imgblur


def main ():
    img_original = cv.imread(INPUT_IMAGE)
    img_simple = cv.imread(INPUT_IMAGE)
    img_integral = cv.imread(INPUT_IMAGE)
    height, width, channel = img_original.shape

    # Apply simple mean filter
    img_simple = meanfilter_simple(img_original, img_simple, height, width, WINDOWSIZE)
    cv.imwrite('./img/01-simple.png', img_simple)

    # Apply divisible mean filter

    # Apply integral image mean filter
    auxintegral = create_integral_image(img_original, height, width)
    img_integral = meanfilter_integral(auxintegral, img_integral, height, width, WINDOWSIZE)
    cv.imwrite('./img/03-integral.png', img_integral)


main()
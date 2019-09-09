import cv2 as cv
import math

from classes import Pixel

INPUT_IMAGE = "./img/img.bmp"
WINDOWSIZE = 3

def create_integral_image(img, height, width):
    intimg = [[Pixel(0,0,0) for x in range(width)] for y in range(height)]

    for h in range(height):
        for w in range(width):

            # apply channel sum to all pixels, except que first one
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
                    intimg[h][w].g = int(img[h][w][0]) + intimg[h-1][w].g + intimg[h][w-1].g - intimg[h-1][w-1].g
                    intimg[h][w].r = int(img[h][w][0]) + intimg[h-1][w].r + intimg[h][w-1].r - intimg[h-1][w-1].r

    return intimg


def meanfilter(img_original, img_blur, height, width, wsize):

    for h in range(height):
        for w in range(width):
            sum = [0,0,0]

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
    wsize2 = math.floor(wsize/2)

    for h in range(height):
        for w in range(width):

            # Check if window size don't exceeds image margins
            if w - wsize2 >= 0 and h - wsize2 >= 0 and w + wsize2 < width and h + wsize2 < height:
                # finds the mean of all the 3 channels

                imgblur[h, w][0] = (intimg[h + wsize2][w + wsize2].b - intimg[h - wsize2][w + wsize2].b - intimg[h + wsize2][w - wsize2].b + intimg[h - wsize2][w - wsize2].b) / (wsize * wsize)
                imgblur[h, w][1] = (intimg[h + wsize2][w + wsize2].g - intimg[h - wsize2][w + wsize2].g - intimg[h + wsize2][w - wsize2].g + intimg[h - wsize2][w - wsize2].g) / (wsize * wsize)
                imgblur[h, w][2] = (intimg[h + wsize2][w + wsize2].r - intimg[h - wsize2][w + wsize2].r - intimg[h + wsize2][w - wsize2].r + intimg[h - wsize2][w - wsize2].r) / (wsize * wsize)


    return imgblur





def main ():
    img_original = cv.imread(INPUT_IMAGE)
    img_blur = cv.imread(INPUT_IMAGE)
    height, width, channel = img_original.shape



    #img_blur = meanfilter(img_original, img_blur, height, width, WINDOWSIZE)
    img_integral = create_integral_image(img_original, height, width)

    for h in range(height):
        for w in range(width):
            print (img_integral[h][w].b, " ", end='')

        print(", ")

    print("-------------------------------------------")
    for h in range(height):
        for w in range(width):
            print (img_original[h, w][0], " ", end='')

        print(", ")

    img_blur = meanfilter_integral(img_integral, img_blur, height, width, WINDOWSIZE)
    cv.imwrite('./img/01-img.bmp', img_blur)



main()

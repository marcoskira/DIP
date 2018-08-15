LIMIT = 150 


def main():
    # Loads an image
    img = cv.imread('./img/yui.jpg') # args[]
    width, height, channel = img.shape

    img = binarization(img, width, height, LIMIT, channel)

    # Save modified image
    cv.imwrite('./img/yuibinarizado2.png', img) # args[]


# Apply binarization 
def binarization(img, width, height, limit, channel):
    for h in range(height):
        for w in range(width):
            pixel = img[w, h]

            # BGR or grayscale?
            if channel == 3:
                # s = (int(pixel[0]) + int(pixel[1]) + int(pixel[2])) / 3                   # Simple conversion
                s = (int(0.114 * pixel[0]) + int(0.587 * pixel[1]) + int(0.299 * pixel[2]))  # Right conversion
            else:
                s = int(pixel[0])

            # Within limit?
            if s > limit:
                pixel = [255, 255, 255]
            else:
                pixel = [0, 0, 0]

            img[w, h] = pixel

    return img

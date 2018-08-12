import cv2 as cv
import numpy as np

THRESHOLD = 150


def main():
    # Carrega imagem
    img = cv.imread('./img/yui.jpg')
    width, height, channel = img.shape

    # Cria modelo de matriz
    model = np.zeros((height, width))

    # Copiar quadrante
    pica = img[200:250, 200:250]

    # img[:, :, 1] = 0
    # pixel = img[0, 0]
    # print pixel

    img = binariza(img, width, height, THRESHOLD, channel)

    cv.imwrite('./img/yuibinarizado2.png', img)


# Binariza imagem
def binariza(img, width, height, threshold, channel):
    for h in range(height):
        for w in range(width):
            pixel = img[w, h]

            # BGR ou grayscale?
            if channel == 3:
                # s = (int(pixel[0]) + int(pixel[1]) + int(pixel[2])) / 3                   #Conversao simples
                s = (int(0.114 * pixel[0]) + int(0.587 * pixel[1]) + int(0.299 * pixel[2]))  # Conversao adequada
            else:
                s = int(pixel[0])

            # Dentro ou fora do limiar?
            if s > threshold:
                pixel = [255, 255, 255]
            else:
                pixel = [0, 0, 0]

            img[w, h] = pixel

    return img


# Inicia o programa aqui
main()
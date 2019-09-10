import cv2 as cv
import math


INPUT_IMAGE = "./img/teste.png"

def normalizes(img, height, width, min, max, newmin, newmax):
	#f = (max - min)/(newmax - newmin) #negative
	max = int(img[0, 0]);
	min = int(img[0, 0]);
	
	for h in range(height):
		for w in range(width):
			if int(img[h, w]) > max:
				max = int(img[h, w])
			elif int(img[h, w] < min):
				min = int(img[h, w])
	
	print(min, max)

	#					0,00840336134453781512605042016807
	# max * f(y,x) * ( (maxN - minN) / (max - min) ) 
	f = (newmax - newmin)/float(max - min)

	for h in range(height):
		for w in range(width):
			img[h, w] = round((max * (img[h, w] * f)));  

	return img
	

def main ():
	img_original = cv.imread(INPUT_IMAGE)
	img_norm = cv.imread(INPUT_IMAGE, 0)
	height, width, channel = img_original.shape
	
	img_norm = normalizes(img_norm, height, width, 0, 255, 0, 1)
	cv.imwrite('./img/01-normalized.png', img_norm)


main()
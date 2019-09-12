import cv2 as cv

INPUT_IMAGE = "./img/img.jpg"

def creates_histogram(img, height, width):
	hist = [0 for x in range(256)]

	# fills in histogram
	for h in range(height):
		for w in range(width):
			hist[int(img[h, w])] += 1

	return hist

def remove_pixels(height, width, perc):
    n = round((height * width) * perc)
    removed = 0

    # removes from the end of color spectrum

    # removes from the beginning of color spectrum



def normalizes(img, height, width, oldmax, oldmin):
	newmax = int(img[0, 0]);
	newmin = int(img[0, 0]);

	# finds max and min values in color spectrum within an image
	for h in range(height):
		for w in range(width):
			if int(img[h, w]) > newmax:
				newmax = int(img[h, w])
			elif int(img[h, w] < newmin):
				newmin = int(img[h, w])


	# normalize an image using max and min values found
	for h in range(height):
		for w in range(width):
			img[h, w] = round(((int(img[h, w]) - newmin)/ float(newmax - newmin)) * (oldmax - oldmin)+0)

	return img
	

def main ():
	img_original = cv.imread(INPUT_IMAGE)
	img_norm = cv.imread(INPUT_IMAGE, 0)
	height, width, channel = img_original.shape
	
	#img_norm = normalizes(img_norm, height, width, 0, 255)
	creates_histogram(img_norm, height, width)
	#cv.imwrite('./img/01-normalized.jpg', img_norm)


main()

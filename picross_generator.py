from typing import Dict, Tuple, List, Union
import itertools
import random
import sys
import copy
import os
import numpy as np
import cv2

# This function open the image as grayscale with opencv from the given filepath
# Then it threshold it to make sure to have a black and white only image
# It return the array of RGB value of the picture
def get_black_and_white_image(filepath:str) :

	try :
		img = cv2.imread(filepath, 0)
		ret, img_black_white = cv2.threshold(img,127,255,cv2.THRESH_BINARY)

	except Exception as err :
		print(f"An error occured while attempting to open {filepath} : {err}")
		exit(1)

	return img_black_white

if __name__ == "__main__" : 

	if len(sys.argv) < 2 :
		print("Argument error : no source image provided")
		print("Please provide the path to your source image to the script")
		exit(1)

	filepath = sys.argv[1]

	img_black_white = get_black_and_white_image(filepath)

	cv2.imshow("Grayscale Image", img_black_white)
	cv2.waitKey(0)

	# destroying all windows
	cv2.destroyAllWindows()
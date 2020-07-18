from typing import Dict, Tuple, List, Union
import itertools
import random
import sys
import copy
import os
import numpy
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

# This function go through the black and white image and count vertically and horizontaly the number of blacks blocks there is and thier length
# It return a tuple composed of two lists : the first one is the length of blocks per line and the second one is the length of blocks per columns
def count_blocks(img:List[List]) -> Tuple[List, List] :

	height = len(img)
	width = len(img[0])

	line_blocks = [[] for y in range(width)]
	col_blocks = [[] for y in range(height)]

	# The array indicate if I incremented the column previously, indicating when I quit/enter a block
	am_i_counting_col = [False for y in range(height)]

	for i in range(height) :
		
		block_line_length = 0
		for j in range(width) :

			if img[i][j] == 0 : # If it's black
				block_line_length += 1
				
				if not am_i_counting_col[j] : # If I am not already couting a block in the col
					col_blocks[j].append(1) # We initialize the counter
				else :
					col_blocks[j][-1] += 1 # We increment the last counter

				am_i_counting_col[j] = True

			else : # If it's white 
				if block_line_length > 0 : # If I've been counting row blocks
					line_blocks[i].append(block_line_length)
					block_line_length = 0

				if am_i_counting_col[j] : # If i've been counting a col block
					am_i_counting_col[j] = False

		if block_line_length > 0 : # If there is a block at the end of the line
			line_blocks[i].append(block_line_length)
			block_line_length = 0

	return (line_blocks, col_blocks)

if __name__ == "__main__" : 

	if len(sys.argv) < 2 :
		print("Argument error : no source image provided")
		print("Please provide the path to your source image to the script")
		exit(1)

	filepath = sys.argv[1]

	img_black_white = get_black_and_white_image(filepath)

	for row in img_black_white: 
		print(row)

	line, col = count_blocks(img_black_white)

	height = len(img_black_white)
	width = len(img_black_white[0])

	case_length = 30 # Every pixel of my src img will be represented by height/width * x pixel case on my result image

	img = numpy.zeros((height*case_length+200,width*case_length+200, 3),numpy.uint8)
	img.fill(255)

	cumulated_case_length = 0	
	offset = int(len(img)*3/20) # value, in pixel, of the grid translation from (0, 0)
	for row in range(len(img_black_white)+1) :

		x_start = offset + cumulated_case_length
		y_start = offset
		
		x_end = offset + cumulated_case_length 
		y_end = case_length * len(img_black_white) + offset

		start_point = (x_start, y_start)
		end_point = (x_end, y_end)
		cv2.line(
			img,
			start_point,
			end_point,
			(0, 0, 0),
			1
		)

		cumulated_case_length += case_length

	cumulated_case_length = 0	
	for column in range(len(img_black_white[0])+1) :

		x_start = offset 
		y_start = offset + cumulated_case_length
		
		x_end = case_length * len(img_black_white[0]) + offset
		y_end = offset + cumulated_case_length

		start_point = (x_start, y_start)
		end_point = (x_end, y_end)
		cv2.line(
			img,
			start_point,
			end_point,
			(0, 0, 0),
			1
		)

		cumulated_case_length += case_length

	position = (10, 30)
	cv2.putText(
		img, #numpy array on which text is written
		"Python Examples", #text
		position, #position at which writing has to start
		cv2.FONT_HERSHEY_SIMPLEX, #font family
		0.5, #font size
		(0, 0, 0, 0), #font color
		1 #font stroke
	)


	cv2.imwrite('picross.png', img)
	cv2.imshow('image',img)
	cv2.waitKey(0)

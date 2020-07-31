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

# This function encapsulate the function cv2.line() to reduce the number of parameter needed
# The line drawn will be always 1 pixel large and black
# It returns nothing
def draw_line(img:List[List], start_point:Tuple[int, int], end_point:Tuple[int, int]) :

	cv2.line(
			img,
			start_point,
			end_point,
			(0, 0, 0),
			1
		)

# This function encapsulate the function cv2.putText() to reduce the number of parameter needed
# The text written will always have 0.5 font size, 1 font stoke and it will be written in black colored Hershey Simplex
# It returns nothing
def write_text(img:List[List], text:str, text_position:Tuple[int, int]) :
	cv2.putText(
					img, # numpy array on which text is written
					text, #text
					text_position, # position at which writing has to start
					cv2.FONT_HERSHEY_SIMPLEX, # font family
					0.5, # font size
					(0, 0, 0, 0), # font color
					1 # font stroke
				)

def draw_multiple_lines(target_img:List[List], is_row_lines:bool, offset:int, lines_in_img:int, case_length:int):
	
	cumulated_case_length = 0	
	
	for line in range(lines_in_img+1) :

		x_start = y_start = x_end = y_end = offset

		if is_row_lines : # are we drawing the columns or the rows of the grid ?
			x_start += cumulated_case_length

			x_end += cumulated_case_length 
			y_end += case_length * lines_in_img
		else :
			y_start += cumulated_case_length
		
			x_end += case_length * lines_in_img
			y_end += cumulated_case_length

		start_point = (x_start, y_start)
		end_point = (x_end, y_end)
		draw_line(target_img, start_point, end_point)

		cumulated_case_length += case_length

# This function return the length of the longest list element within a list
# If the list of list is empty, it will return -1
# It returns an integer
def get_list_element_max_length (lists:List[List]) -> int :

	if len(lists) == 0 :
		return -1

	max_length = len(lists[0])
	for l in lists :

		if len(l) > max_length :
			max_length = len(l)

	return max_length

def draw_numbers (isCol:bool, idx:int, number_size:int, x_start:int, y_start:int, case_length:int, blocks_number:List[List], target_img:List[List]) :

	x_start_number = x_start + int(case_length*1.1/4)
	y_start_number = y_start + int(case_length*1.8/3)
	for black_blocks_in_line in blocks_number[idx] :
		
		text_position = (x_start_number, y_start_number)
		write_text(
			target_img, # numpy array on which text is written
			str(black_blocks_in_line), #text
			text_position, # position at which writing has to start
		)

		if isCol :
			y_start_number += number_size
		else :
			x_start_number += number_size

def draw_one_picross_outline (isCol:bool, number_size:int, blocks_number:List[List], target_img:List[List], case_length:int, offset:int) :

	max_length = get_list_element_max_length(blocks_number)

	if isCol : # Am I drawing the numbers on the top (isCol = True) or the numbers on the left ? (isCol = False)
		y_end = offset
		y_start = offset - (max_length * number_size)
	else :
		x_end = offset
		x_start = offset - (max_length * number_size)

	cumulated_case_length = 0
	
	for idx in range(len(blocks_number)+1) :
		
		if isCol :
			x_start = x_end = offset + cumulated_case_length
		else :
			y_start = y_end = offset + cumulated_case_length

		start_point = (x_start, y_start)
		end_point = (x_end, y_end)
		draw_line(target_img, start_point, end_point)

		cumulated_case_length += case_length

		if idx < len(blocks_number) : # if i am not drawing the last line
			
			draw_numbers(
				isCol, 
				idx, 
				number_size, 
				x_start, 
				y_start, 
				case_length, 
				blocks_number, 
				target_img
			)


def draw_picross_outlines (offset:int, row_blocks:List[List], col_blocks:List[List], target_img:List[List], case_length:int) :

	number_size = 25 # size in pixel of a number character on the img
	
	draw_one_picross_outline(True, number_size, col_blocks, target_img, case_length, offset)
	draw_one_picross_outline(False, number_size, row_blocks, target_img, case_length, offset)

def draw_picross_grid(img_black_white:List[List], counted_blocks:Tuple[List, List], target_img:List[List], case_length:int) :
	offset = int(len(target_img)*3/20) # value, in pixel, of the grid translation from (0, 0)
	
	draw_multiple_lines(target_img, True, offset, len(img_black_white), case_length) # drawing the lines
	draw_multiple_lines(target_img, False, offset, len(img_black_white[0]), case_length) # drawing the columns

	draw_picross_outlines(offset, counted_blocks[0], counted_blocks[1], target_img, case_length)

if __name__ == "__main__" : 

	if len(sys.argv) < 2 :
		print("Argument error : no source image provided")
		print("Please provide the path to your source image to the script")
		exit(1)

	filepath = sys.argv[1]

	img_black_white = get_black_and_white_image(filepath)

	for row in img_black_white: 
		print(row)

	counted_blocks = count_blocks(img_black_white)

	height = len(img_black_white)
	width = len(img_black_white[0])

	case_length = 30 # Every pixel of my src img will be represented by height/width * x pixel case on my result image

	img = numpy.zeros((height*case_length+200,width*case_length+200, 3),numpy.uint8)
	img.fill(255)

	draw_picross_grid(img_black_white, counted_blocks, img, case_length)

	cv2.imwrite('picross.png', img)

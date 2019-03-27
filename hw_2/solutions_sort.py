#Karthikeya Sharma P
# HW-2
# Code to sort the solutions from other txt files
import numpy as np
import ast


def xy_to_location_no(x, y):

	# function converts given (x,y) location on the board to a unique sequential number starting from 1
	return x*7 + y + 1



if __name__ == "__main__":

	solutions_number_board = {}

	for init_piece in range(8, 14):

		Line = []
		j= 0
		
		solutions_number_board[init_piece] = np.zeros((7,7), dtype=np.int)

		f = open("solution_w_initial_{}.txt".format(init_piece),'r')

		for i, line in enumerate(f):

			if all([(i-2)%12, (i-3)%12, (i-4)%12, (i-5)%12, (i-6)%12, (i-7)%12, (i-8)%12]) == 0:
					
					Line.append(line)
			
			if (i-9)%12 == 0:

				for row in range(0,7):
					for column in range(2, 16,2):
						if int(Line[row][column]) == 0:
							solutions_number_board[init_piece][row][int(column/2 -1)] += 1

				j += 1

				Line = []
		
		print("The no. of solutions with zero only at corresponding locations starting with piece {} is as follows: \n".format(init_piece), solutions_number_board[init_piece])
# HW - 2
# P. Karthikeya Sharma
# Block puzzle arrangement

import numpy as np
import multiprocessing as mp

class Block_puzzle():

	def __init__(self):
		self.path = {}

		self.init_pieces()
		self.run_algorithm()

	def init_pieces(self,):
		# define the shapes of self.pieces

		self.pieces = {}
		self.pieces[0] = np.ones((2,1), dtype=np.int) 
		
		self.pieces[1] = np.ones((4,2), dtype=np.int)
		self.pieces[1][0][0] = self.pieces[1][3][0] = 0
		
		self.pieces[2] = np.ones((5,1), dtype=np.int)
		
		self.pieces[3] = np.ones((3,4), dtype=np.int)
		self.pieces[3][0][0] = self.pieces[3][0][3] = self.pieces[3][2][0] = self.pieces[3][1][3] = 0
		
		self.pieces[4] = np.ones((3,3), dtype=np.int)
		self.pieces[4][0][1] = self.pieces[4][0][2] = self.pieces[4][1][2] = 0

		self.pieces[5] = np.ones((3,3), dtype=np.int)
		self.pieces[5][0][2] = self.pieces[5][1][0] = self.pieces[5][2][0] =self.pieces[5][2][1] = 0

		self.pieces[6] = np.ones((2,3), dtype=np.int)
		self.pieces[6][0][0] = self.pieces[6][0][2] = 0

		self.pieces[7] =  np.ones((3,3), dtype=np.int)
		self.pieces[7][0][2] = self.pieces[7][2][2] = 0

		self.pieces[8] = np.ones((2,4), dtype=np.int)
		self.pieces[8][1][0] = self.pieces[8][1][1] = self.pieces[8][1][3] = 0
		
		for i in range(9, 18):

			self.pieces[i] = self.rotate_piece_90_deg(self.pieces[i-9])
		
		for i in range(18, 27):

			self.pieces[i] = self.rotate_piece_90_deg(self.pieces[i-9])

		for i in range(27, 36):

			self.pieces[i] = self.rotate_piece_90_deg(self.pieces[i-9])
				
		self.n_solutions = 0


	def rotate_piece_90_deg(self, piece):

		# rotate given piece by 90 degrees clockwise
		M = piece.shape[0]
		temp = np.zeros(piece.shape, dtype=np.int).transpose()

		for i in range(M):
			
			temp[:, M-i-1] = piece[i]

		piece = temp

		return piece

	def run_algorithm(self,):

		processes = []
		for i in self.pieces:
			# eliminate the pieces that can never fetch the solution looking at its initial orientation
			if i in [6,7,32,33,34,35] :#not in [17, 18, 20, 27, 29, 30, 31]:
				proc = mp.Process(target=self.DFS, args=(i, 0))
				print("Beginning with piece {}".format(i))
				proc.start()
				processes.append(proc)	
				

	def valid_overlap(self, board, piece, i, j, value):

		# The function checks if the overlapping of the given piece at a given location on the given board is valid
		valid_overlap_flag = (self.add_piece(board, piece, i, j) < value).all()

		self.remove_piece(board, piece, i, j)

		return valid_overlap_flag

	def list_identical_pieces(self, n):
		# the pieces obtained  by rotating the existing pieces are deemed to be identical
		m = n%9	
		identical_pieces_list = [m, m+9, m+18, m+27]
	
		return identical_pieces_list

	def DFS(self, initial_piece, d):
		# recursive DFS
		j = 0
		self.path[d] = initial_piece

		# recursion for depth less than 8
		if d < 8:
			for i in self.pieces:

				identical_pieces_list = self.list_identical_pieces(i)
				considered =  any(elem in identical_pieces_list  for elem in list(self.path.values())[0:d+1])
				# avoiding the re-occurence of pieces obtained by rotation of existing pieces
				if not considered:

					board = np.zeros((7,7), dtype=np.int)
					piece_arr_order = []

					# constructing the board to ensure that the latest piece can be added to the board
					for piece_no in list(self.path.values())[0:d+1]:

						feasible, piece_x, piece_y = self.add_feasible_piece(board, piece_no)
						piece_arr_order.append((piece_x, piece_y, piece_no))

						if not feasible:

							break
					if d>=5 and np.count_nonzero(board[0:2][:]) < 13:
						feasible = 0


						
					#zero island is a zero that is surrounded by ones
					single_zero_islands_n, double_zero_islands_n = self.zero_islands_check(board)

					if single_zero_islands_n <= 1 and double_zero_islands_n == 0:
						if feasible:		
							#check if the order of pieces arranged is same as insisted
							order_match  = self.check_insertion_order(piece_arr_order, list(self.path.values())[0:d+1])


						# flush the list
						piece_arr_order = []

						# perform DFS from the current node according to whether it is feasible to add the current piece and 
						# the order of arrangement matches to that of what the tree demands

						if feasible and order_match:
							#print(board, d, self.path)
							self.DFS(i, d+1)
					
		else:

			j += 1	
			board_ = np.zeros((7,7), dtype=np.int)
			
			for i in list(self.path.values())[0:9]:
				
				feasible, piece_x, piece_y = self.add_feasible_piece(board_, i)

				if not feasible:
					#print(board_, d, self.path)
					break

			# we have a solution if the feasibility is satisfied at the leaf or the count of the non-zero elements in the board is 48
			if np.count_nonzero(board_) == 48 or feasible:
				self.n_solutions += 1
				f = open("solution_w_initial_{}.txt".format(self.path[0]), "a")

				f.write("Solution found with the path:"+str(self.path))
				f.write("\n")
				f.write("Board formed:"+"\n"+str(board_))
				f.write("\n")	
				f.write("No. of solutions so far:"+str(self.n_solutions))

				piece_arr_order = []
				board_ = np.zeros((7,7), dtype=np.int)			
				
				for piece_no in list(self.path.values())[0:9]:
					feasible, piece_x, piece_y = self.add_feasible_piece(board_, piece_no)
					piece_arr_order.append((piece_x, piece_y, piece_no))
				
				print("Locations of the arranged pieces", piece_arr_order)
				print("\n")
				print("No. of solutions so far:", self.n_solutions)
				f.write("\n")
				f.write("Locations of the arranged pieces"+str(piece_arr_order)+"\n")
				f.write("------------------------------------------------------------------"+"\n")
				f.close()
				piece_arr_order = []
				
								

	def check_insertion_order(self, piece_arr_order, actual_order):
		# checks if the order insisted by the path from the DFS tree is same as that obtained through add_feasible_piece() function
		assert len(actual_order) == len(piece_arr_order)
		
		piece_arr_order_sorted = sorted(piece_arr_order, key=lambda k: (k[0], k[1]))
		sorted_order = [c for a,b,c in piece_arr_order_sorted]

		for i in range(0, len(actual_order)):

			if actual_order[i] != sorted_order[i]:

				return 0

		return 1		

	def zero_islands_check(self, board):
		# checks for the single and double zeros surrounded by ones
		zero_islands_count = 0
		double_zero_islands_count = 0
		for x in range(0, 7):
			for y in range(0, 7):
				
				if 0<x<6 and 0<y<6:
					
					if board[x][y] == 0 and all([board[x+1][y], board[x][y+1], board[x-1][y], board[x][y-1]]) == 1:

						zero_islands_count += 1

					if 1<x<5 and 1<y<5:	
						
						if board[x][y] == 0 and board[x+1][y] == 0 and all([board[x+2][y], board[x][y+1], board[x-1][y], board[x][y-1], board[x+1][y-1], board[x+1][y+1]]) == 1:

							double_zero_islands_count += 1

						if board[x][y] == 0 and board[x][y+1] == 0 and all([board[x-1][y+1], board[x-1][y], board[x][y+2], board[x+1][y+1], board[x+1][y], board[x][y-1]]) == 1:

							double_zero_islands_count += 1
	
				elif x == 0 and 0<y<6:

					if board[x][y] == 0 and all([board[x+1][y], board[x][y+1], board[x][y-1]]) == 1:

						zero_islands_count += 1



				elif x == 6 and 0<y<6:

					if board[x][y] == 0 and all([board[x-1][y], board[x][y+1], board[x][y-1]]) == 1:

						zero_islands_count += 1

				elif y == 6 and 0<x<6:

					if board[x][y] == 0 and all([board[x][y-1], board[x+1][y], board[x-1][y]]) == 1:

						zero_islands_count += 1

					if 1<x<5:	
						
						if board[x][y] == 0 and board[x+1][y] == 0 and all([board[x][y-1], board[x-1][y], board[x+1][y-1], board[x+2][y]]) == 1:

							double_zero_islands_count += 1
							
				elif y == 0 and 0<x<6:

					if board[x][y] == 0 and all([board[x-1][y], board[x][y+1], board[x+1][y]]) == 1:

						zero_islands_count += 1
					
					if 1<x<5:	
						
						if board[x][y] == 0 and board[x+1][y] == 0 and all([board[x][y+1], board[x-1][y], board[x+1][y+1], board[x+2][y]]) == 1:

							double_zero_islands_count += 1

				elif (x, y) == (0, 0):

					if board[x][y] == 0 and all([board[x+1][y], board[x][y+1]]) == 1:

						zero_islands_count += 1

				elif (x, y) == (0, 6):

					if board[x][y] == 0 and all([board[x][y-1], board[x+1][y]]) == 1:

						zero_islands_count += 1


				elif (x, y) == (6, 0):

					if board[x][y] == 0 and all([board[x-1][y], board[x][y+1]]) == 1:

						zero_islands_count += 1


				elif (x, y) == (6, 6):

					if board[x][y] == 0 and all([board[x-1][y], board[x][y-1]]) == 1:

						zero_islands_count += 1

		return zero_islands_count, double_zero_islands_count

			

	def add_piece(self, board, piece, x, y):
		# add piece to the board at a given location
		board[x:x+piece.shape[0], y:y+piece.shape[1]] += piece

		return board

	def remove_piece(self, board, piece, x, y):
		#remove piece from the board at a given location
		board[x:x+piece.shape[0], y:y+piece.shape[1]] -= piece

		return board

	def add_feasible_piece(self, board, piece_no):
		# add the given piece on the board wherever is possible coming from top left to bottom right
		piece = self.pieces[piece_no]
		for i in range(8-piece.shape[0]):
			for j in range(8-piece.shape[1]):

				value = 2

				if self.valid_overlap(board, piece, i, j, value):
	
					self.add_piece(board, piece, i, j)

					return 1, i, j

		return 0, None, None




if __name__ == "__main__":
	
	Puzzle = Block_puzzle()


#
# py-sudoku
#
# A sudoku solver implemented in Python.
#
# Copyright 2018 Andre Plötze
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from __future__ import division
from __future__ import print_function
from collections import deque
import numpy as np

#
# This class implements a Sudoku grid.
#
class Grid:
	
	#
	# Initialize a 9x9 grid of numbers.
	#
	def __init__(self, grid = None):
		self.__G = np.zeros((9, 9), dtype = np.int8)
	
	#
	# Set the number in a position, specified by row and column number, to
	# a specific value.
	#
	def set_number(self, row, column, value):
		self.__G[row, column] = value
	
	#
	# Return the number assigned to a specific position, specified by row
	# and column number.
	#
	def get_number(self, row, column):
		return self.__G[row, column]
	
	#
	# Sets all entries in this grid to zero (unknown) state.
	#
	def clear(self):
		
		#
		# Iterate over the rows.
		#
		for row in range(9):
			
			#
			# Iterate over the columns.
			#
			for column in range(9):
				self.__G[row, column] = 0
	
	#
	# Set all values in the grid via a NumPy array.
	#
	def set_grid(self, grid):
		
		#
		# Check if the grid is two-dimensional.
		#
		if len(grid.shape) == 2:
			
			#
			# Check if the grid is 9x9.
			#
			if (grid.shape[0] == 9) & (grid.shape[1] == 9):
				self.__G[:, :] = np.copy(grid[:, :])
	
	#
	# Return all values in the grid as a NumPy array.
	#
	def get_grid(self):
		return np.copy(self.__G[:, :])
	
	#
	# Check whether a specific position, specified by row and column
	# number, has a number assigned.
	#
	def is_solved(self, row, column):
		return self.__G[row, column] > 0
	
	#
	# Check whether the Sudoku is completed, that is, every row and column
	# has a number assigned.
	#
	def is_completed(self):
		completed = True
		
		#
		# Iterate over the rows.
		#
		for row in range(9):
			
			#
			# Iterate over the columns.
			#
			for column in range(9):
				
				#
				# If the current cell does not have a number assigned, the Sudoku is
				# not solved.
				#
				if not self.is_solved(row, column):
					completed = False
		
		return completed
	
	#
	# Return a list of all possible numbers for a given position,
	# specified by row and column number.
	#
	def get_possibilities(self, row, column):
		c = self.get_number(row, column)
		
		#
		# If the value of this cell is known, then this is the only possible
		# value for the cell.
		#
		# Otherwise, generate a list of all possible values for this cell, as
		# per the Sudoku constraints.
		#
		if c > 0:
			return np.array([c])
		else:
			current_row = self.__G[row, :]
			current_column = self.__G[:, column]
			x, y = (row // 3) * 3, (column // 3) * 3
			current_square = self.__G[x : x + 3, y : y + 3]
			possible_numbers = [i for i in range(1, 10) if (i not in current_row) & (i not in current_column) & (i not in current_square)]
			return possible_numbers
	
	#
	# Find the most constrained field, i. e. the one with the least
	# possible values.
	#
	def find_most_constrained(self):
		lowest = 10
		field = (-1, -1)
		
		#
		# Iterate over the rows.
		#
		for row in range(9):
			
			#
			# Iterate over the columns.
			#
			for column in range(9):
				
				#
				# If the current cell is not solved, find out how many combinations
				# are allowed.
				#
				if not self.is_solved(row, column):
					possibilities = self.get_possibilities(row, column)
					count = len(possibilities)
					
					#
					# If there are less allowed than in other cells we've seen so far,
					# make this our most constrained cell.
					#
					if count < lowest:
						field = (row, column)
						lowest = count
		
		return field
	
	#
	# Solve the Sudoku iteratively.
	#
	def solve(self):
		abort = False
		queue = deque()
		queue.append(self.get_grid())
		completed = self.is_completed()
		
		#
		# As long as the Sudoku is not solved and there is no other reason to
		# abort (e. g. queue empty), continue.
		#
		while (not completed) & (not abort):
			row, column = self.find_most_constrained()
			possibilities = self.get_possibilities(row, column)
			
			#
			# Try all possibilities.
			#
			for possibility in possibilities:
				self.set_number(row, column, possibility)
				queue.append(self.get_grid())
			
			self.set_grid(queue.popleft())
			completed = self.is_completed()
			
			#
			# Abort if the queue is empty.
			#
			if len(queue) == 0:
				abort = True
	
	#
	# Creates a string representation of this Sudoku grid.
	#
	def to_string(self):
		rows = []
		
		#
		# Iterate over the rows.
		#
		for row in range(9):
			the_row = []
			
			#
			# Insert line separator every three lines.
			#
			if (row % 3 == 0) & (row > 0):
				rows.append("---+---+---")
			
			#
			# Iterate over the columns.
			#
			for column in range(9):
				
				#
				# Insert column separator every three columns.
				#
				if (column % 3 == 0) & (column > 0):
					the_row.append("|")
				
				n = self.get_number(row, column)
				the_row.append(str(n) if n > 0 else "?")
			
			rows.append("".join(the_row))
		
		return "\n".join(rows)
	
	#
	# Override the str() cast operation.
	#
	def __str__(self):
		return self.to_string()

#
# Program entry point.
#
if __name__ == "__main__":
	
	foo = [
		[0, 0, 0, 0, 0, 0, 0, 1, 0],
		[4, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 2, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 5, 0, 4, 0, 7],
		[0, 0, 8, 0, 0, 0, 3, 0, 0],
		[0, 0, 1, 0, 9, 0, 0, 0, 0],
		[3, 0, 0, 4, 0, 0, 2, 0, 0],
		[0, 5, 0, 1, 0, 0, 0, 0, 0],
		[0, 0, 0, 8, 0, 6, 0, 0, 0]
	]
	
	grid = Grid()
	stop = False
	
	#
	# Continue until the user wants to exit.
	#
	while not stop:
		print("> ", end = "")
		user_input = raw_input()
		split_input = str.split(user_input)
		
		#
		# Check if the user entered a command.
		#
		if len(split_input) >= 1:
			command = split_input[0]
			
			#
			# Handle each command.
			#
			if command == "set":
				
				#
				# Check if three arguments were supplied.
				#
				if len(split_input) != 4:
					print("Error: Command 'set' takes exactly 3 arguments.")
				else:
					
					#
					# Try to parse the user input.
					#
					try:
						row = int(split_input[1])
						column = int(split_input[2])
						value = int(split_input[3])
						
						#
						# Check if values are in the correct range.
						#
						if (row >= 1) & (row <= 9) & (column >= 1) & (column <= 9) & (value >= 1) & (value <= 9):
							grid.set_number(row - 1, column - 1, value)
							print()
							print(str(grid))
							print()
						else:
							print("Error: All arguments must be numbers between 1 and 9.")
						
					except ValueError:
						print("Error: Illegal argument.")
				
			elif command == "unset":
				
				#
				# Check if two arguments were supplied.
				#
				if len(split_input) != 3:
					print("Error: Command 'unset' takes exactly 2 arguments.")
				else:
					
					#
					# Try to parse the user input.
					#
					try:
						row = int(split_input[1])
						column = int(split_input[2])
						
						#
						# Check if values are in the correct range.
						#
						if (row >= 1) & (row <= 9) & (column >= 1) & (column <= 9):
							grid.set_number(row - 1, column - 1, 0)
							print()
							print(str(grid))
							print()
						else:
							print("Error: All arguments must be numbers between 1 and 9.")
						
					except ValueError:
						print("Error: Illegal argument.")
			
			elif command == "clear":
				
				#
				# Check if no arguments were supplied.
				#
				if len(split_input) != 1:
					print("Error: Command 'clear' does not take arguments.")
				else:
					grid.clear()
					print()
					print(str(grid))
					print()
			
			elif command == "foo":
				
				#
				# Check if no arguments were supplied.
				#
				if len(split_input) != 1:
					print("Error: Command 'foo' does not take arguments.")
				else:
					grid.set_grid(np.array(foo))
					print()
					print(str(grid))
					print()
					
			elif command == "solve":
				
				#
				# Check if no arguments were supplied.
				#
				if len(split_input) != 1:
					print("Error: Command 'solve' does not take arguments.")
				else:
					grid.solve()
					print()
					print(str(grid))
					print()
				
			elif command == "exit":
				
				#
				# Check if no arguments were supplied.
				#
				if len(split_input) != 1:
					print("Error: Command 'exit' does not take arguments.")
				else:
					stop = True
				
			else:
				print("Error: Unknown command")


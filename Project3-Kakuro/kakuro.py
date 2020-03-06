# Kakuro project

import sys
import re

import utils
import search

from csp import *
from time import time


# Cell class - Store general information for each square we read from input
class Cell():

    def __init__(self, cellType, bottom, right, value, row, column):

        self.type   = cellType          # Cell tyoe (black, grey or white)
        self.bottom = bottom            # Summary of beneath   sequence       (grey)
        self.right  = right             # Summary of righthand sequence       (grey)
        self.value  = value             # Value of current cell               (white)
        self.row    = row               # Row of cell    - indexing in X Axis (all)
        self.column = column            # Column of cell - indexing in Y Axis (all)
        self.sumRow = 0                 # The summary of the row cell lays    (white)
        self.sumCol = 0                 # The summary of the column cell lays (white)


# Our main class - Kakuro
class Kakuro(CSP):

    rows      = 0               # Number of grid rows
    columns   = 0               # Number of grid columns
    grid      = None            # The grid (2D Array) (the output)
    squares   = []              # A list of Cell-class items to store each square's data
    variables = []              # Game Variables list       (k01, k02, etc)
    domains   = {}              # Vars Domains   dictionary (k01:[1,2,..,9] etc)
    neighbors = {}              # Vars Neighbors dictionary (k22:['k21','k23'] etc)
    #dataCSP   = None

    def __init__(self):

        self.initiateVariables()
        self.initiateDomains()
        self.initiateNeighbors()
        CSP.__init__(self, self.variables, self.domains, self.neighbors, self.constraint)


    def initiateVariables(self):
        # Separates input strings from a certain format input file given as parameter in the command line
        # Creates the variable list and the initial grid (as well the assistant square list)

        fileInput = open(sys.argv[1],'r')       # Read from an input representing an initial grid
        firstline = True
        rowItem   = 0

        for line in fileInput:                  # Read every line to understand and store the data given
            line  = line.rstrip('\n')
            words = re.split(' ', line)
            columnItem = 0

            if firstline:                       # The first line informs about the grid size (rows columns)
                self.rows = int(words[0])
                self.columns = int(words[1])
                self.grid = [[0 for x in range(self.columns)] for y in range(self.rows)]
                firstline = False
                continue

            for item in words:                  # Read every square from given grid
                c = None

                if item == 'XXXXX':
                    c = Cell('Black', None, None, None, rowItem, columnItem)            # Black cell, no use in kakuro
                elif item[2] == '\\':
                    if item[0] == 'X':
                        right = int(item[3]+item[4])
                        c = Cell('Grey', None, right, None, rowItem, columnItem)        # Grey cell, shows summary
                    elif item[3] == 'X':                                                # Either for right or beneath cells
                        bottom = int(item[0]+item[1])                                   # Maybe both right and bottom
                        c = Cell('Grey', bottom, None, None, rowItem, columnItem)
                    else:
                        bottom = int(item[0]+item[1])
                        right = int(item[3]+item[4])
                        c = Cell('Grey', bottom, right, None, rowItem, columnItem)
                else:                                                                   # White cell, initially empty
                    c = Cell('White', None, None, 0, rowItem, columnItem)
                self.squares.append(c)                                                  # Store every cell information in square list

                varName = 'k' + str(rowItem) + str(columnItem)          # Create a new variable that represents the current cell
                self.variables.append(varName)
                self.grid[rowItem][columnItem] = item                   # Initialize the grid with the format given in input file
                columnItem += 1
            rowItem += 1



    def initiateDomains(self):
        # Create the domains dictionary (Values that each square can take)
        i = 0
        for item in self.squares:
            if item.type == 'White':
                self.domains[self.variables[i]] = list(range(1,10))     # Main white cells, can be assigned as 1,2,...,9
            elif item.type == 'Grey':
                self.domains[self.variables[i]] = [0]                   # Grey cell, cannot take any value (0 to seperate its type)
            elif item.type == 'Black':
                self.domains[self.variables[i]] = [-1]                  # Black cell, cannot take any value (-1 to seperate its type)
            i += 1
        #print('Domains', self.domains)



    def initiateNeighbors(self):
        # Create the neighbors dictionary (neighbors for each cell that we take care of)
        for cell in self.squares:
            if cell.type == 'Grey' and cell.right:                  # Look for white cells sequences in a row
                rowItemsWhiteList = []
                y = cell.column + 1                                 # The first cell of this sequence is next to a grey cell
                varName = 'k' + str(cell.row) + str(y)
                while (0 not in self.domains[varName] and -1 not in self.domains[varName]):
                    rowItemsWhiteList.append(varName)
                    for item in self.squares:                                                   # Look for varName cell in square list
                        if item.row == int(varName[1]) and item.column == int(varName[2]):      # Assign the summary of row cell lays on
                            item.sumRow = cell.right
                            break
                    y += 1                                          # If the current cell is white, add it in a temporary list
                    if (y >= self.columns):                         # If it is not white, or is after the last one, stop searching
                        break
                    varName = 'k' + str(cell.row) + str(y)
                for item in rowItemsWhiteList:                      # Each cell's neighbors are the other cells in this temporary list
                    tempList = rowItemsWhiteList.copy()             # The list stores the continuous white cells of this row
                    tempList.remove(item)                           # So we create a new list with the rest cells, without the current one
                    self.neighbors[item] = tempList                 # The list is assigned to neighbors dictionary with current cell as key

            if cell.type == 'Black' or cell.type == 'Grey':
                item = 'k' + str(cell.row) + str(cell.column)       # If current cell is grey or black, they are useless squares
                self.neighbors[item] = []                           # As a result, their neighbors list is empty

        for cell in self.squares:
            if cell.type == 'Grey' and cell.bottom:                 # Do the same as above for cell sequences in columns
                columnItemsWhiteList = []
                x = cell.row + 1
                varName = 'k' + str(x) + str(cell.column)
                while (0 not in self.domains[varName] and -1 not in self.domains[varName]):
                    columnItemsWhiteList.append(varName)
                    for item in self.squares:
                        if item.row == int(varName[1]) and item.column == int(varName[2]):
                            item.sumCol = cell.bottom
                            break
                    x += 1
                    if (x >= self.rows):
                        break
                    varName = 'k' + str(x) + str(cell.column)
                for item in columnItemsWhiteList:
                    tempList = columnItemsWhiteList.copy()
                    tempList.remove(item)
                    if item not in list(self.neighbors.keys()):     # A cell may have neighbors both horizontically or vertically
                        self.neighbors[item] = tempList             # So, current cell's neighbors may have been assigned above
                    else:                                           # In this case, we have to append the new items in the current list
                        temp2 = self.neighbors[item].copy()         # Then assign the cells neighbors with this bigger list
                        tempList += temp2
                        self.neighbors[item] = tempList
        #print('Neighbors', self.neighbors)


    def constraint(self, A, a, B, b):
        # Constraint function
        assigned = self.infer_assignment()      # The list of assigned variables from csp algorithm
        #print(assigned)
        returnValue = False
        row = int(A[1])                         # Row of A variable (the second letter, e.g. k02 -> 0)
        col = int(A[2])                         # Column of A variable (the third letter, e.g. k02 -> 2)

        if row == int(B[1]):                    # A and B variables are on the same row
            properSummary = None
            summary = a + b                     # Initialize the summary of row as the addition of the 2 variables given
            for item in self.squares:
                varName = 'k' + str(item.row) + str(item.column)        # Search in the square list for variable A
                if varName == A:                                        # In order to find the summary needed for row
                    properSummary = item.sumRow
                    break
            for item in self.squares:                                   # Now search for the rest neighboring variables
                varName = 'k' + str(item.row) + str(item.column)        # Which lays on the same row and sequence
                if item.row == row and varName in self.neighbors[A]:
                    if varName != B and varName not in assigned:        # If the variable we found isn't B and not assigned before
                        if (properSummary - summary) > 9:               # It must take a temporary value so as to create a summary
                            item.value = 9                              # Look the difference between current summary and the proper one
                        else:                                           # If is bigger than 9, then give the current variable value 9
                            item.value = properSummary - summary        # Else give it the value of the difference left
                        summary += item.value                           # Finally add the temporary value of variable to the summary
                        if item.value == a or item.value == b:
                            returnValue = False                         # If the value given is same with a or b, then wrong value
                    if varName != B and varName in assigned:
                        summary += assigned[varName]                    # If the current variable has been assigned, then add this value
            if summary == properSummary and a != b:
                returnValue = True                                      # A true situation should have proper neighbors summary and a!=b

        if col == int(B[2]):                    # A and B variables are on the same column - do the same as above vertically
            properSummary = None
            summary = a + b
            for item in self.squares:
                varName = 'k' + str(item.row) + str(item.column)
                if varName == A:
                    properSummary = item.sumCol
                    break
            for item in self.squares:
                varName = 'k' + str(item.row) + str(item.column)
                if item.column == col and varName in self.neighbors[A]:
                    if varName != B and varName not in assigned:
                        if (properSummary - summary) > 9:
                            item.value = 9
                        else:
                            item.value = properSummary - summary
                        summary += item.value
                        if item.value == a or item.value == b:
                            returnValue = False
                    if varName != B and varName in assigned:
                        summary += assigned[varName]
            if summary == properSummary and a != b:
                returnValue = True

        return returnValue              # Return True or False


    def printGrid(self, valuesDictionary=None):
        # Print the Grid of kakuro (initial or final, depending on valuesDictionary)
        # Shows square values after (or before if you may) the execution of CSP Algorithms
        print('++++++++++++++++++++++++++++++++++++++++++++++++')
        if valuesDictionary:
            for key in valuesDictionary:                            # An algorithm has been executed, white cells have values
                x = int(key[1])
                y = int(key[2])                                     # Grid position is assigned from key (k23: grid[2][3])
                listBlackOrGrey = [-1, 0]
                digit = valuesDictionary[key]
                if digit not in listBlackOrGrey:                    # If this is not a white cell, then do not change anything
                    self.grid[x][y] = '  ' + str(digit) + '  '
        for x in range(self.rows):
                for y in range(self.columns):
                    print(self.grid[x][y], end = ' ')               # Finally print the grid!!
                print()
        print('++++++++++++++++++++++++++++++++++++++++++++++++')


# Executable part (main)
k = Kakuro()
print()

start = time()
values = backtracking_search(k)                                                                 # BT
finish = time()
print('BT - Execution Time:', finish-start)
k.printGrid(values)
print()

start = time()
values = backtracking_search(k, select_unassigned_variable=mrv)                                 # BT + MRV
finish = time()
print('BT+MRV - Execution Time:', finish-start)
k.printGrid(values)
print()

start = time()
values = backtracking_search(k, inference=forward_checking)                                     # FC
finish = time()
print('FC - Execution Time:', finish-start)
k.printGrid(values)
print()

start = time()
values = backtracking_search(k, select_unassigned_variable=mrv, inference=forward_checking)     # FC + MRV
finish = time()
print('FC+MRV - Execution Time:', finish-start)
k.printGrid(values)
print()


start = time()
values = backtracking_search(k, order_domain_values=lcv)                                        # LCV
finish = time()
print('LCV - Execution Time:', finish-start)
k.printGrid(values)
print()

start = time()
values = backtracking_search(k, inference=mac)                                                  # MAC
finish = time()
print('MAC - Execution Time:', finish-start)
k.printGrid(values)
print()

"""
start = time()
values = min_conflicts(k)                               # Min-Con - Problem sometimes (does not finish)
finish = time()
print('Min-Con - Execution Time:', finish-start)
k.printGrid(values)
"""

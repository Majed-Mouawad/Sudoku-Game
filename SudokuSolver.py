board = [

[3,0,6,5,0,8,4,0,0],
[5,2,0,0,0,0,0,0,0],
[0,8,7,0,0,0,0,3,1],
[0,0,3,0,1,0,0,8,0],
[9,0,0,8,6,3,0,0,5],
[0,5,0,0,9,0,6,0,0],
[1,3,0,0,0,0,2,5,0],
[0,0,0,0,0,0,0,7,4],
[0,0,5,2,0,6,3,0,0],

]


def find_empty_sqaure(current_board):

        # This function iterates over the board to find the first empty square
        # and returns the coordinates of that sqaure.

        for i in range(len(current_board)):
                for j in range(len(current_board[0])):
                        if (current_board[i][j] == 0):
                                return (i,j)
        return None


def legal_placement(current_board, number_to_insert, position):
        
        # This function checks if the number_to_insert can be placed in the sqaure of 
        # of coordinates position following the sudoku rules.

        for i in range(len(current_board[1])):
                if current_board[position[0]][i] == number_to_insert and position[1] != i:
                        return False

        for i in range(len(current_board)):
                if current_board[i][position[1]] == number_to_insert and position[0] != i:
                        return False

        # We will split the board in 9 boxes to check if the placement is legal
        # in the corresponding box. The corresponding box will be determined 
        # depending on the position we want to insert the number in.

        column_of_box = position[1] // 3    
        row_of_box = position[0] // 3

        for i in range (row_of_box*3, row_of_box*3 + 3):
                for j in range(column_of_box*3, column_of_box*3 + 3):
                        if current_board[i][j] == number_to_insert and (i,j) != position:
                                return False

        return True


def solve_board(current_board):

        # This function solves the sudoku board using the backtracking algorithm.

        if find_empty_sqaure(current_board) == None:
                return True
        else:
                empty_square = find_empty_sqaure(current_board)

        for i in range(1,10):
                if legal_placement(current_board, i, empty_square) == True:
                        current_board[empty_square[0]][empty_square[1]] = i

                        if solve_board(current_board):
                                return True

                        current_board[empty_square[0]][empty_square[1]] = 0

        return False


def display_board(current_board):

        # This function prints out the board.
        
        for i in range(len(current_board)):
                if i % 3 == 0 and i != 0:
                        print("- - - - - - - - - - - - - - - - - - -")

                for j in range(len(current_board[1])):
                        if j % 3 == 0 and j != 0:
                                print(" | ", end = "")

                        if j == len(current_board[1])-1: 
                                print(current_board[i][j])
                        else:
                                print(str(current_board[i][j]) + " ", end = "")


display_board(board)
solve_board(board)
print("\n Here is the solved board: \n")
display_board(board)

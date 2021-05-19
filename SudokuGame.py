#Code written by Majed Mouawad 

from SudokuSolver import solve_board, legal_placement, display_board
import pygame
import time
pygame.font.init()


my_font = pygame.font.SysFont("comicsans", 40)

print("""

Here are the rules:

- You have a maximum of 3 false attempts.

- You can put a maximum of 1 number as a draft in each cube at any given time.

---------------------------------------------------------------------------------------------

Here are the controls:

- You need to click on the cube you wish to select (You cannot use the arrow keys).

- After you select a cube, choose the number you want to insert and press the corresponding key on your keyboard.

- After pressing the key of the number you wish to insert, the number will be displayed as a draft.

- Press ENTER to finalize your input. 

- This means that you have to press the key of the number you wish to insert then press ENTER in order to finalize your input.

- Press BACKSPACE if you wish to delete a draft or input another number to replace it immediatly.

Good luck!

""")

easy_board = [
        [0,0,3,0,4,2,0,9,0],
        [0,9,0,0,6,0,5,0,0],
        [5,0,0,0,0,0,0,1,0],
        [0,0,1,7,0,0,2,8,5],
        [0,0,8,0,0,0,1,0,0],
        [3,2,9,0,0,8,7,0,0],
        [0,3,0,0,0,0,0,0,1],
        [0,0,5,0,9,0,0,2,0],
        [0,8,0,2,1,0,6,0,0]
]

intermediate_board = [
        [2,0,0,0,0,0,1,0,0],
        [1,9,0,0,2,0,0,8,3],
        [0,0,3,0,1,0,5,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,7,6,0,0,0,5,0],
        [8,0,4,2,0,1,3,0,0],
        [0,0,0,0,0,3,2,0,0],
        [0,0,1,8,0,2,0,3,0],
        [0,0,0,1,7,0,0,4,9]

]

hard_board = [
        [0,2,0,0,0,0,0,0,0],
        [0,0,0,6,0,0,0,0,3],
        [0,7,4,0,8,0,0,0,0],
        [0,0,0,0,0,3,0,0,2],
        [0,8,0,0,4,0,0,1,0],
        [6,0,0,5,0,0,0,0,0],
        [0,0,0,0,1,0,7,8,0],
        [5,0,0,0,0,9,0,0,0],
        [0,0,0,0,0,0,0,4,0]
]

want_to_play = True
while  want_to_play == True:

        level = input("Choose your level of difficulty: 1, 2 or 3 or press Q to quit: ").strip()
        if level in ("1","2","3"):
                break
        elif level in ("q","Q"):
                want_to_play = False
                break
        else:
                print("Please choose a level or press Q to quit: ")

if want_to_play == False:
        print("Goodbye.")
        exit()

# The part below saves the selected board so that the solver can solve it.

if level == "1":
        chosen_board = easy_board
elif level == "2":
        chosen_board = intermediate_board
elif level == "3":
        chosen_board = hard_board

class Grid: 

        # This class represents the whole board that contains all of small cubes that store the numbers in the sudoku game.

        if level == "1":
                board = easy_board
        elif level == "2":
                board = intermediate_board
        elif level == "3":
                board = hard_board


        def __init__(self, rows, columns, width, height):
                self.rows = rows
                self.cols = columns
                self.width = width
                self.height = height
                self.cubes = [[Cube(self.board[i][j], i ,j ,width, height) for j in range(columns)] for i in range(rows)]
                self.model = None
                self.selected = None

        def new_state_to_check(self):

                """

                This method updates the state of the board everytime a number is added so that the solver can check new inputs accordingly.

                """

                self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

        def place(self, number_to_place):

                """

                This method uses the solver to check if number the user is inputting is correct and places in the board if that is the case. 

                """

                row, column = self.selected
                if self.cubes[row][column].value == 0:
                        self.cubes[row][column].set(number_to_place)
                        self.new_state_to_check()

                        if legal_placement(self.model, number_to_place, (row, column)) == True and solve_board(self.model):
                                return True

                        else:
                                self.cubes[row][column].set(0)
                                self.cubes[row][column].set_draft(0)
                                self.new_state_to_check()
                                return False

        def draw_board(self, window):

                """

                This method is divided in two parts. The first part draws the board and the grid and second part draws the cubes 
                and the border of each cube depending of the state of that cube. 

                """

                # Part that draws the board and the grid.

                area = self.width / 9
                for i in range(self.rows+1):
                        if i % 3 == 0 and i != 0:
                                thickness = 4
                        else:
                                thickness = 1
                        pygame.draw.line(window, (0,0,0), (0, i*area), (self.width, i*area), thickness)
                        pygame.draw.line(window, (0,0,0), (i* area,0), (i*area, self.height), thickness)

                # Part that draws the cubes.

                for i in range(self.rows):
                        for j in range(self.cols):
                                self.cubes[i][j].draw(window)

                for i in range(self.rows):
                        for j in range(self.cols):
                                if self.selected != (i, j):
                                        if self.cubes[i][j].value != 0 and self.selected != None and self.cubes[i][j].value == self.cubes[self.selected[0]][self.selected[1]].value:
                                                self.cubes[i][j].draw_green(window)



        def select_cube(self, row, column):

                """

                This method selects a specified cube in the board.

                """ 
                for i in range(self.rows):
                        for j in range(self.cols):
                                self.cubes[i][j].selected = False

                self.cubes[row][column].selected = True
                self.selected = (row, column)



        def place_draft(self, number_to_place):

                """

                This method inputs a draft number to the selected cube in the board.

                """

                (row, column) = self.selected
                self.cubes[row][column].set_draft(number_to_place)



        def clear_draft(self):

                """

                This method removes the draft from the selected cube in the board.

                """

                (row, column) = self.selected
                if self.cubes[row][column].value == 0:
                        self.cubes[row][column].set_draft(0)


        def click(self, position_clicked):

                """

                This method returns the coordinates of the cube that was clicked on or returns
                None if the position clicked on is not in the board.

                """


                if position_clicked[0] < self.width and position_clicked[1] < self.height:
                        area = self.width / 9
                        column = position_clicked[0] // area
                        row = position_clicked[1] // area
                        return (int(row), int(column))
                else:
                        return None

        def is_complete(self):

                """

                This method checks if the board has been completed.

                """

                for i in range(self.rows):
                        for j in range(self.cols):
                                if self.cubes[i][j].value == 0:
                                        return False
                return True



class Cube:

        # This class represents the small cubes inside of the sudoku board.

        rows = 9
        columns = 9

        def __init__(self, value, row, column, width, height):
                self.value = value
                self.possible_number = 0
                self.row = row
                self.column = column
                self.width = width
                self.height = height
                self.selected = False


        def draw(self, window):

                """

                This method draws the number or the draft inputed inside of the cube and draws a red edge around the selected cube
                to show that it is the one selected.

                """


                my_font = pygame.font.SysFont("comicsans", 40)
                area = self.width / 9
                column = self.column * area
                row = self.row * area



                if self.value == 0 and self.possible_number != 0:
                        num_value = my_font.render(str(self.possible_number), 1, (128,128,128))
                        window.blit(num_value, (column+5, row+5))

                elif not(self.value == 0):
                        num_value = my_font.render(str(self.value), 1,(0,0,0))
                        window.blit(num_value, (column +(area/2 - num_value.get_width()/2), row + (area/2 - num_value.get_height()/2)))

                if self.selected:
                        pygame.draw.rect(window, (255,0,0), (column,row, area, area), 3)

                        
        def draw_green(self, window):

                """

                This method is used to draw a green edge around a cube.

                """

                area = self.width / 9
                column = self.column * area
                row = self.row * area

                pygame.draw.rect(window, (0,255,0), (column,row, area, area), 3)
                        



        def set(self, value):

                """

                This method sets the final value of the cube.

                """
                self.value = value

        def set_draft(self, value):

                """

                This method sets the draft/possible value of the cube.

                """

                self.possible_number = value


def time_format(seconds):

        """

        This method returns the time in the format of minutes:seconds.


        """
        secs = seconds % 60
        minutes = seconds // 60
        if secs < 10:
                display = " " + str(minutes) + ":0" + str(secs)
        else:

                display = " " + str(minutes) + ":" + str(secs)

        return display

def print_time_format(seconds):

        """

        This method return the final playing time.

        """
        secs = seconds % 60
        minutes = seconds // 60
        if minutes < 1:
                display = str(secs)+ " seconds."
        else:

                display = str(minutes)+ " minutes and " + str(secs)+ " seconds."

        return display



def draw_window(window, current_board, time, attempts):

        """

        This method redraws the window every time there is a change to it.

        """
        
        window.fill((255,255,255))
        my_font = pygame.font.SysFont("comicsans", 40)
        time_display = my_font.render("Time: " + time_format(time), 1, (0,0,0))
        window.blit(time_display, (380, 560))
        chances_display = my_font.render("X " * attempts, 1, (255, 0, 0))
        window.blit(chances_display, (20, 560))
        current_board.draw_board(window)

def main():
        window = pygame.display.set_mode((540,600))
        pygame.display.set_caption("Sudoku")
        board = Grid(9,9,540,540)
        pressed_key = None
        running = True
        start = time.time()
        attempts = 0
        while running:
                runtime = round(time.time() - start)
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                running = False


                        if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_1:
                                        pressed_key = 1
                                if event.key== pygame.K_2:
                                        pressed_key = 2
                                if event.key== pygame.K_3:
                                        pressed_key = 3
                                if event.key == pygame.K_4:
                                        pressed_key= 4
                                if event.key== pygame.K_5:
                                        pressed_key = 5
                                if event.key == pygame.K_6:
                                        pressed_key = 6
                                if event.key== pygame.K_7:
                                        pressed_key = 7
                                if event.key== pygame.K_8:
                                        pressed_key= 8
                                if event.key == pygame.K_9:
                                        pressed_key = 9
                                if event.key == pygame.K_BACKSPACE:
                                        board.clear_draft()
                                        pressed_key = None
                                if event.key == pygame.K_RETURN:
                                        i, j = board.selected
                                        if board.cubes[i][j].possible_number != 0:
                                                if board.place(board.cubes[i][j].possible_number):
                                                        print("Correct")
                                                else:
                                                        print("Wrong")
                                                        attempts += 1
                                                        if attempts == 3:
                                                                print("Game over. "+"You lost in: "+print_time_format(runtime))
                                                                solve_board(chosen_board)
                                                                print("Here is the solution: ")
                                                                display_board(chosen_board)
                                                                time.sleep(15)
                                                                running = False
                                                pressed_key = None

                                                if board.is_complete():
                                                        print("You won! Your time: "+ print_time_format(runtime))
                                                        time.sleep(5)
                                                        running = False
                                                
                                                  

                        if event.type == pygame.MOUSEBUTTONDOWN:
                                position = pygame.mouse.get_pos()
                                clicked = board.click(position)
                                if clicked:
                                        board.select_cube(clicked[0], clicked[1])
                                        pressed_key= None

                if board.selected and pressed_key != None:
                        board.place_draft(pressed_key)

                draw_window(window, board, runtime, attempts)
                pygame.display.update()


main()
pygame.quit()






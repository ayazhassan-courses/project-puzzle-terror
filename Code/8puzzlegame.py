import pygame
import random
import numpy as np
import csv
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
import time

#______________________________________________________
def randomly_generate(filename):
    main=[]
    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter = ",")
        for row in readCSV:
            for i in range(0, len(row)): 
                row[i] = int(row[i]) 
            main.append(row) 
    csvfile.close()
    ans=random.randint(0,len(main)-1)
    return main[ans]


def convert_to_array(state): 
    array = []  
    for x in range(0,9,3):
        array.append(state[x:x + 3])
    return array

def is_solvable(digit):
    count = 0
    for i in range(0, 9):
        for j in range(i, 9):
            if digit[i] > digit[j] and digit[i] != 9:
                count += 1
    if count % 2 == 0:
        print("The puzzle is solvable,so solve the puzzle")
        return True
    else:
        print("The puzzle is insolvable,run code again")
        return False

def f(start,goal,level):
    return h(start,goal) + (level + 1)


def h(start,goal):
        """ Calculates the different between the given puzzles """
        temp = 0
        for i in range(0,3):
            for j in range(0,3):
                if start[i][j] != goal[i][j] and start[i][j] != 9:
                    temp += 1
        return temp


def copy(puz):
    temp = []
    for i in range(0,len(puz)):
        x = []
        for j in range(0,len(puz)):
            x.append(puz[i][j])
        temp.append(x)

    return temp


def shuffle(puz,x1,y1,x2,y2):
    puz = copy(puz)
    if x2 >= len(puz) or x2 < 0 or y2 >= len(puz) or y2 < 0:
        return None

    temp = puz[x1][y1]
    puz[x1][y1] = puz[x2][y2]
    puz[x2][y2] = temp

    return puz


def find(puz,char):
    for i in range(0,len(puz)):
        for j in range(0,len(puz)):
            if puz[i][j] == char:
                return i,j

def generate_child(puz):
    x,y = find(puz,9)
    positions = [[x+1,y],
                 [x-1,y],
                 [x,y+1],
                 [x,y-1]]
    children = []

    for pos in positions:
        child = shuffle(puz,x,y,pos[0],pos[1])
        if child != None:
            children.append(child)

    return children


def present(ol,cl,child):
    for i in ol:
        if h(i['puz'],child) == 0:
            return True
    for i in cl:
        if h(i['puz'],child) == 0:
            return True

    return False


"""
f(n) = h(n) + g(n)
"""

def solve(start,goal):
    startlist = []
    for i in start:
        startlist.extend(i)

    open_list = []
    close_list = []
    pathlist = []

    open_list.append(
        {
            'id':0,
            'puz':start,
            'f':f(start,goal,-1),
            'g':0,
            'prev':None
        })
    id = 0
    while len(open_list) != 0:
        single_state = []

        cur_node = open_list[-1]

        for i in cur_node['puz']:
            single_state.extend(i)
        if single_state != startlist:
            pathlist.append(single_state)
        

        if h(cur_node['puz'],goal) == 0:
            break
        children = generate_child(cur_node['puz'])
        temp_list = []
        for child in children:
            if not present(open_list,close_list,child):
                id += 1
                temp_list.append({
                    'id':id,
                    'puz':child,
                    'f':f(child,goal,cur_node['g']),
                    'g':cur_node['g']+1,
                    'prev':cur_node['id']
                    })
        temp_list.sort(key=lambda x:x['f'],reverse=True)
        
        for ele in temp_list:
            open_list.append(ele)

        close_list.append(cur_node)
        open_list.remove(cur_node)
        
    return pathlist




#---------------------------pygame classes---------------------
#____________________________________________
class Button():
    def __init__(self, screen, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.screen = screen

    def draw(self,outline=None):
        #To draw the button on the screen
        if outline:
            pygame.draw.rect(self.screen, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.width, self.height), 0) 

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 30)
            text = font.render(self.text, 1, (0, 51, 51))
            self.screen.blit(text, (
                self.x + int(self.width / 2 - text.get_width() / 2), self.y + int(self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False
#_______________________________________________________________
class HighlightDigit:
    def __init__(self, screen,swapped):
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.screen = screen
        self.blue = (51, 102, 153)
        self.swapped = swapped
        self.highlight_x = 100 
        self.highlight_y = 100
        self.highlight_side = 100

        self.hfont = pygame.font.SysFont('Georgia', 25) #SysFont(name, size, bold=False, italic=False) 
        self.highlight_digit = pygame.draw.rect(self.screen, self.white,
                                                [self.highlight_x, self.highlight_y, self.highlight_side,
                                                 self.highlight_side], 5) #pygame.draw.rect(screen, [red, blue, green], [left, top, width, height], thickness) , left from screen's most left
        self.index = 0
        self.m_count = 0
        self.listofswaps = []
    
    def highlight_digit_to_be_swapped(self, x, y, key, puzzle):



        if self.highlight_digit.x == 100 and self.highlight_digit.y == 100:
            self.index = 0
        elif self.highlight_digit.x == 200 and self.highlight_digit.y == 100:
            self.index = 1
        elif self.highlight_digit.x == 300 and self.highlight_digit.y == 100:
            self.index = 2
        elif self.highlight_digit.x == 100 and self.highlight_digit.y == 200:
            self.index = 3
        elif self.highlight_digit.x == 200 and self.highlight_digit.y == 200:
            self.index = 4
        elif self.highlight_digit.x == 300 and self.highlight_digit.y == 200:
            self.index = 5
        elif self.highlight_digit.x == 100 and self.highlight_digit.y == 300:
            self.index = 6
        elif self.highlight_digit.x == 200 and self.highlight_digit.y == 300:
            self.index = 7
        elif  self.highlight_digit.x == 300 and self.highlight_digit.y == 300:
            self.index = 8

        self.highlight_x = self.highlight_digit.x + x
        self.highlight_y = self.highlight_digit.y + y
        if self.highlight_x < 400 and self.highlight_x >= 100 and self.highlight_y >= 100 and self.highlight_y < 400:
            self.screen.fill(self.black)
            self.highlight_digit = self.highlight_digit.move(x, y) #moving the bordered box
            pygame.draw.rect(self.screen, self.white, self.highlight_digit, 5)
            if key == "LEFT":
                return self.swap(self.index, self.index - 1, puzzle)
            elif key == "RIGHT":
                return self.swap(self.index, self.index + 1, puzzle)
            elif key == "UP":
                return self.swap(self.index, self.index - 3, puzzle)
            elif key == "DOWN":
                return self.swap(self.index, self.index + 3, puzzle)
            else:
                print (":)")
        return False


    def swap(self, index, index2, puzzle):
        if puzzle[index] == 9:
            temp = puzzle[index]
            puzzle[index] = puzzle[index2]
            puzzle[index2] = temp
            self.m_count += 1
            print ("YOUR SWAP: %s" % puzzle)
            self.listofswaps.append(puzzle[:])
            self.swapped = True


        self.move_count("Moves: %s" % str(self.m_count))

        if puzzle == [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            print("COMPARISON: %s" % (puzzle == [1, 2, 3, 4, 5, 6, 7, 8, 9]))
            print("You Win !!!")
            return True


        return False

    def move_count(self, text, x=50, y=400):
        try:
            self.hfont.render(text, True, self.blue)
            self.htextsurface = self.hfont.render(text, True, self.blue) 
            self.screen.blit(self.htextsurface, (x, y))

        except Exception as e:
            raise e
class GeneratePuzzle:
    def __init__(self, screen,start_state):
        self.screen = screen
        self.digits = start_state

    def generate_puzzle(self):
        return self.digits

    def draw_puzzle(self, digits):
        counter_x = 1
        counter_y = 1
        puzzle = []
        for digit in digits:
            puzzle.append(DigitSqr(self.screen, digit, 100 * counter_x, 100 * counter_y))
            counter_x += 1
            if counter_x % 4 == 0:
                counter_x = 1
                counter_y += 1

        return puzzle

    def is_solvable(self, digit):
        count = 0
        for i in range(0, 9):
            for j in range(i, 9):
                if digit[i] > digit[j] and digit[i] != 9:
                    count += 1

        return count
#_____________________________________________________
class DigitSqr():
    def __init__(self, screen, digit, sqr_x=100, sqr_y=100):
        self.screen = screen
        self.green = (102, 153, 153)
        self.dark_green = (0, 51, 51)
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.myfont = pygame.font.SysFont('Comic Sans MS', 30)
        self.digit = digit
        self.sqr_side = 98
        self.rect = pygame.draw.rect(self.screen, self.green, (sqr_x, sqr_y, self.sqr_side, self.sqr_side))
        if self.digit != 9:
            self.text_to_screen(self.digit, self.rect.x + 40, self.rect.y + 25) 


    def draw_rect(self, x, y):
        self.rect = self.rect.move(x, y)
        if self.digit != 9:
            self.text_to_screen(self.digit, self.rect.x + 40, self.rect.y + 25)
        pygame.display.update()

    def text_to_screen(self, text, x, y):
        try:
            text = str(text)
            self.textsurface = self.myfont.render(text, True, self.dark_green)
            self.screen.blit(self.textsurface, (x, y))

        except Exception as e:
            raise e

#____________________________________________________
class Puzzle:
    def __init__(self,start,startarray,goalarray):
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.dist = 200
        pygame.init()
        self.startarray = startarray
        self.goalarray = goalarray
        self.start = start
        self.clock = pygame.time.Clock() 
        self.screen = pygame.display.set_mode((600, 600))
        pygame.display.set_caption('### 8 numbers sorting Puzzle ###')
        self.screen.fill(self.black)

        self.generate_puzzle = GeneratePuzzle(self.screen,self.start)
        self.highlight = HighlightDigit(self.screen,False)

    def initialization(self):

        self.puzzle_numbers = self.generate_puzzle.generate_puzzle() 
        self.generate_puzzle.draw_puzzle(self.puzzle_numbers) 
        solve_button = Button(self.screen,(153, 153, 153), 450, 100, 100, 50, "Solve") #grey button x,y,width,heigh,text
        replay_button = Button(self.screen,(153, 153, 153), 420, 200, 160, 50, "Replay Steps") 
        solve_button.draw((109, 146, 155)) 
        replay_button.draw((109, 146, 155))
        
        self.finish = True
        self.you_win = False
        while self.finish:
            self.highlight.move_count("8 Puzzle Puzzle", 130, 10) 
            solve_button.draw((109, 146, 155)) 
            replay_button.draw((109, 146, 155))
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.finish = False

                elif self.you_win == False:
                    if (event.type == KEYDOWN):
                        if (event.key == K_RIGHT):
                            # print ("*** RIGHT ***")
                            self.you_win = self.highlight.highlight_digit_to_be_swapped(100, 0, "RIGHT",
                                                                                        self.puzzle_numbers) #prints bordered box in new position
                            self.generate_puzzle.draw_puzzle(self.puzzle_numbers)
                        elif (event.key == K_LEFT):
                            # print ("*** LEFT ***")
                            self.you_win = self.highlight.highlight_digit_to_be_swapped(-100, 0, "LEFT",
                                                                                        self.puzzle_numbers)
                            self.generate_puzzle.draw_puzzle(self.puzzle_numbers)

                        elif (event.key == K_DOWN):
                            # print ("*** DOWN ***")
                            self.you_win = self.highlight.highlight_digit_to_be_swapped(0, 100, "DOWN",self.puzzle_numbers)
                            self.generate_puzzle.draw_puzzle(self.puzzle_numbers)

                        elif (event.key == K_UP):
                            # print( "*** UP ***")
                            self.you_win = self.highlight.highlight_digit_to_be_swapped(0, -100, "UP",self.puzzle_numbers)
                            self.generate_puzzle.draw_puzzle(self.puzzle_numbers)
                    pos = pygame.mouse.get_pos() 

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        
                        if solve_button.isOver(pos):
                            initialstat = []
                            var = self.startarray
                            for subl in var:
                                for elee in subl:
                                    initialstat.append(elee)
                            print ("You Clicked Solve button")
                            time.sleep(1)
                            path = solve(self.startarray,self.goalarray)
                            path.insert(0,initialstat)
                            for i, puzzle in enumerate(path):
                                self.screen.fill(self.black)
                                self.highlight.move_count("8 Puzzle Puzzle", 130, 10)
                                solve_button.draw((255, 255, 0))
                                time.sleep(1)
                                self.generate_puzzle.draw_puzzle(puzzle)
                                self.highlight.move_count("Moves: %s" % str(i))
                                pygame.display.update()
                                time.sleep(1)
                            self.highlight.move_count("Solved !!!", 130, 450)

                        elif replay_button.isOver(pos):
                            
                            if self.highlight.swapped == True:
                                initialstat = []
                                var = self.startarray
                                for subl in var:
                                    for elee in subl:
                                        initialstat.append(elee)
                                print ("You Clicked Replay button")
                                time.sleep(1)
                                swaps = self.highlight.listofswaps
                                swaps.insert(0,initialstat)
                            
                                for i, puzzle in enumerate(swaps):
                                    self.screen.fill(self.black)
                                    self.highlight.move_count("8 Puzzle Puzzle", 130, 10)
                                    replay_button.draw((255, 255, 0))
                                    time.sleep(1)
                                    self.generate_puzzle.draw_puzzle(puzzle)
                                    self.highlight.move_count("Moves: %s" % str(i))
                                    pygame.display.update()
                                    time.sleep(1)
                                self.highlight.move_count("Replayed !!!", 130, 450)


                            else:
                                continue
                            

                    if self.you_win:
                        self.highlight.move_count("8 Puzzle Puzzle", 130, 10)
                        solve_button.draw((109, 146, 155)) 
                        replay_button.draw((109, 146, 155))
                        self.highlight.move_count("You Win !!!", 130, 450)
                        path = solve(self.startarray,self.goalarray)
                        if self.highlight.m_count == len(path):
                            self.highlight.move_count(" using least number of moves", 130, 500)
                        else:
                            self.highlight.move_count(" But not with least number of moves !!!", 30, 500)
                        pygame.display.update()
                        self.clock.tick(30)
                        time.sleep(2)
                        self.screen.fill(self.black)
                        self.puzzle_numbers = self.generate_puzzle.generate_puzzle()
                        self.highlight.m_count = 0
                        self.generate_puzzle.draw_puzzle(self.puzzle_numbers)
                        
                elif self.you_win == True:
                   
                    pos = pygame.mouse.get_pos() 

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        
                        if solve_button.isOver(pos):
                            initialstat = []
                            var = self.startarray
                            for subl in var:
                                for elee in subl:
                                    initialstat.append(elee)
                            print ("You Clicked Solve button")
                            time.sleep(1)
                            path = solve(self.startarray,self.goalarray)
                            path.insert(0,initialstat)
                            for i, puzzle in enumerate(path):
                                self.screen.fill(self.black)
                                self.highlight.move_count("8 Puzzle Puzzle", 130, 10)
                                solve_button.draw((255, 255, 0))
                                time.sleep(1)
                                self.generate_puzzle.draw_puzzle(puzzle)
                                self.highlight.move_count("Moves: %s" % str(i))
                                pygame.display.update()
                                time.sleep(1)
                                # self.clock.tick(30)
                            self.highlight.move_count("Solved !!!", 130, 450)

                        elif replay_button.isOver(pos):
                            
                            if self.highlight.swapped == True:
                                initialstat = []
                                var = self.startarray
                                for subl in var:
                                    for elee in subl:
                                        initialstat.append(elee)
                                print ("You Clicked Replay button")
                                time.sleep(1)
                                swaps = self.highlight.listofswaps
                                swaps.insert(0,initialstat)
                                
                                for k, puzzle in enumerate(swaps):
                                    self.screen.fill(self.black)
                                    self.highlight.move_count("8 Puzzle Puzzle", 130, 10)
                                    replay_button.draw((255, 255, 0))
                                    time.sleep(1)
                                    self.generate_puzzle.draw_puzzle(puzzle)
                                    self.highlight.move_count("Moves: %s" % str(k))
                                    pygame.display.update()
                                    time.sleep(2)
                                self.highlight.move_count("Replayed !!!", 130, 450)

                            else:
                                continue

            pygame.display.update()
            self.clock.tick(30)

        pygame.quit()
        quit()

print('Randomly generated puzzle is:')
start = randomly_generate("Puzzles.csv")
startarray = convert_to_array(start)
print(np.reshape(start, (3, 3)))
time.sleep(.8)
goal = [1,2,3,4,5,6,7,8,9]
goalarray = convert_to_array(goal)
print('To get to the goal of :' )
print(np.reshape(goal, (3, 3)))
time.sleep(.8)
if is_solvable(start):
    puzzle = Puzzle(start,startarray,goalarray)
    puzzle.initialization()


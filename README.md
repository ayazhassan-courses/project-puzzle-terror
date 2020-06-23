# 8 puzzle game
## Description:
An 8 puzzle is a simple game consisting of a 3 x 3 grid (containing 9 squares). 
One of the squares is empty. The objective is to move to squares around into different positions and having the numbers displayed in the "goal state"(final state) in smallest number of moves. 
This can be done by moving the blank space in 4 directions (up, down, left, right).
There is a Solve button, which allows us to visualize the solution of the game with smallest number of moves, by the help of A* algorithm. 
Moreover, one can also visualize their moves in an already finished game by clicking the 'Replay your Steps' button.

## Implemented Algorithm:
A* Algorithm will help provide us the solution of the puzzle with shortest number of moves by using the combination of heuristic value which is defined as the number of misplaced tiles by comparing the goal state and 
the current state and the g score which is defined as the number of nodes tranversed from start node to current node.

## Modules:
numpy


pygame


time


math


## How to play:
Open the .csv file along with the .py file in Visual Studio Code 2015 or later. Run the .py file and enjoy the game!

# Python Othello with Smart AI

<img align="center" src="https://i.imgur.com/1mrEcB0.png" alt="Othello Board" width=30% height=30%>

This repository contains a single player  version of the board game Othello, which was created using Python with the turtle graphics library. The player plays against the computer, which has been programmed to pick the "optimal" move at each of its turns. 

# The Rules
Similar to checkers, Othello is a game that involves using two different colored tiles (one for each player). When a tile of one color is sandwiched between two tiles of the opposite color, its color flips to the opposite color.

<img align="center" src="https://i.imgur.com/paxUkeb.png" alt="Player Move">

<img align="center" src="https://i.imgur.com/HYDg1Fo.png" alt="Computer Move">

 The objective of the game is to flip the color of as many of the opposing player's tiles as possible. The game ends when there are no legal moves left on the board for either player. The player with the most tiles of his/her color on the board wins.

<img align="center" src="https://i.imgur.com/jeeeUCR.png" alt="Game Over">

# How the AI Works
The computer has been programmed to always pick the move that will result in the most tile flips. At each turn, the computer will scan the board for every possible legal move it can make. It will then count the number of tiles that would be flipped as a result of each legal move and pick the move that flips the most tiles.

# File Descriptions
1. othello_driver.py - The driver of the game. Run this file to start the game.
2. game_classes_final.py - Contains all of the classes and methods that make up the game.
3. othello_test.py - The test suite for the game, which verifies that all classes and methods work properly.
4. ai.txt - A more detailed description of how the AI works and its limitations.

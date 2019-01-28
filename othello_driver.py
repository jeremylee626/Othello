'''
HW7 - Othello Driver
Fall 2018
Jeremy Lee
12/2/18

This program is the driver for the Othello game
'''

import turtle
from game_classes_final import *
import sys

def main():
    
    # Set board size and square size
    n = 8
    square_size = 50

    # Create a new game
    new_game = Game(n, square_size)

    # Draw board
    new_game.draw_board()

    # Setup game
    new_game.setup_game()

    # Start game
    new_game.determine_turn()

    # Start event loop
    turtle.mainloop()

    # Print score
    print(new_game.get_score())
    
    # Prompt player for name
    name = input("Enter your name:\n")

    # Append player name and score to text file
    new_game.save_new_player(name)
    

main()

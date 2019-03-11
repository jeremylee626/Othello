'''
CS5001 - HW7 Classes
Fall 2018
Jeremy Lee
12/2/18

This program contains the classes necessary to play Othello. The classes used
for the game inlcude Player, Tile, LegalMove, and Game. The Game class
controls the flow of the game and contains the governing rules.
'''

import turtle
import time

class Player:
    # Player constructor ------------------------------------------------------
    def __init__(self, name, score):
        self.name = name
        self.score = score
    # Player Methods-----------------------------------------------------------
    def __eq__(self, other):
        '''
        name: __eq__
        inputs: self and other (Both Player objects)
        returns: Boolean
        does: Compares two player objects and returns True if both objects have
        the same name and score or False if not
        '''
        if self.name == other.name and self.score == other.score:
            return True
        else:
            return False
   

class Tile:
    # Tile constructor --------------------------------------------------------
    def __init__(self, color, row, col):
        # Tile properties
        self.color = color
        self.row = int(row)
        self.col = int(col)
    # Tile methods ------------------------------------------------------------
    def __eq__(self, other):
        '''
        name: __eq__
        inputs: self (Tile object) and other (A different Tile object)
        returns: a boolean (True or False)
        does: Checks if two tiles have the same row and column and returns True
        if they do or False otherwise
        '''
        if self.row == other.row and self.col == other.col:
            return True
        else:
            return False
    

class LegalMove:
    # LegalMove constructor----------------------------------------------------
    def __init__(self, tile):
        self.tile = tile
        self.flip_indices = []
    # LegalMove methods--------------------------------------------------------
    def __eq__(self, other):
        '''
        name: __eq__
        inputs: self, other (both legal move objects)
        returns: boolean (True or false)
        does: Checks if two moves have the same tile and returns True if they do
        or False if they don't
        '''
        if self.tile == other.tile:
            return True
        else:
            return False
        
class Game:
    # Game constructor--------------------------------------------------------
    def __init__(self, n, square_size):
        # Game properties
        self.n = n
        self.square_size = square_size
        self.is_player_turn = True
        self.is_game_over = False
        self.tiles = []
        self.directions = {"up": [1, 0],
                           "right": [0, 1],
                           "down": [-1, 0],
                           "left": [0, -1],
                           "up_right": [1, 1],
                           "up_left" : [1, -1],
                           "down_right": [-1, 1],
                           "down_left": [-1, -1]}
        self.final_player_score = 0
        self.player_score_turtle = turtle.Turtle()
        self.comp_score_turtle = turtle.Turtle()
        self.turn_turtle = turtle.Turtle()

    # Game methods -----------------------------------------------------------
    def draw_board(self):
        ''' Function: draw_board
            Parameters: self (Game object), n, an int for # of squares
            Returns: nothing
            Does: Draws an nxn board with a green background
        '''
        self.player_score_turtle.hideturtle()
        self.comp_score_turtle.hideturtle()
        self.turn_turtle.hideturtle()
        
        turtle.setup(self.n * self.square_size + self.square_size, \
                     self.n * self.square_size + self.square_size + 40)
        turtle.screensize(self.n * self.square_size, self.n * self.square_size)
        turtle.bgcolor('white')

        # Create the turtle to draw the board
        othello = turtle.Turtle()
        othello.penup()
        othello.speed(0)
        othello.hideturtle()

        # Line color is black, fill color is green
        othello.color("black", "forest green")
        
        # Move the turtle to the upper left corner
        corner = -self.n * self.square_size / 2
        othello.setposition(corner, corner)
        # Draw the green background
        othello.begin_fill()
        for i in range(4):
            othello.pendown()
            othello.forward(self.square_size * self.n)
            othello.left(90)
        othello.end_fill()

        # Draw the horizontal lines
        for i in range(self.n + 1):
            othello.setposition(corner, self.square_size * i + corner)
            self.draw_lines(othello)

        # Draw the vertical lines
        othello.left(90)
        for i in range(self.n + 1):
            othello.setposition(self.square_size * i + corner, corner)
            self.draw_lines(othello)

    def update_scores(self):
        '''
        name: update_scores
        inputs: self (Game object)
        returns: nothing
        does: Writes the current scores for the computer and player above the board
        '''
        # Erase previous scores
        self.comp_score_turtle.undo()
        self.player_score_turtle.undo()

        # Move turtle to top left corner
        self.comp_score_turtle.penup()
        self.comp_score_turtle.hideturtle()
        corner = self.n * self.square_size / 2
        self.comp_score_turtle.goto(-corner, corner + 5)

        # Write computer's score on screen
        comp_score_string = "Computer score: {}".format(self.count_tiles("white"))
        self.comp_score_turtle.write(comp_score_string, font = ("Arial", 14, "bold"))

        # Move turtle to top right corner
        self.player_score_turtle.penup()
        self.player_score_turtle.hideturtle()
        self.player_score_turtle.goto(corner, corner + 5)

        # Write player's score on screen
        player_score_string = "Player score: {}".format(self.count_tiles("black"))
        self.player_score_turtle.write(player_score_string, align = "right", font = ("Arial", 14, "bold"))

    def update_turn_display(self):
        '''
        name: update_turn_display
        inputs: self (Game object)
        returns: nothing
        does: Writes who's turn it is (player or computer) at the top of turtle window
        '''
        # Erase previous turn message
        self.turn_turtle.undo()
        self.turn_turtle.hideturtle()

        # Move turtle to center of screen, above board
        self.turn_turtle.penup()
        self.turn_turtle.goto(0, self.n * self.square_size / 2 + 20)

        # Set message to display based on who's turn it is
        message = ""
        if self.is_player_turn and  not self.is_game_over:
            message = "Your Turn"
        elif not self.is_player_turn and not self.is_game_over:
            message = "Computer's Turn"
        else:
            message = "Game Over"

        # Write the message at the current turtle location
        self.turn_turtle.write(message, align = "center", font = ("Arial", 18, "bold"))
        
    
    def count_tiles(self, color):
        '''
        name: count_tiles
        inputs: self (Game) and color (String representing color of desired tiles)
        returns: number of tiles of the input color as an int
        does: counts the number of tiles of an input color currently in the game
        '''
        total = 0
        for tile in self.tiles:
            if tile.color == color:
                total += 1
        return total
    
    def draw_lines(self, turt):
        '''
        name: draw_lines
        inputs: self (Game) and turt (Turtle object)
        returns: nothing
        does: draws the game board lines
        '''
        turt.hideturtle()
        turt.pendown()
        turt.forward(self.square_size * self.n)
        turt.penup()

    def draw_tile(self, tile):
        '''
        name: draw_tile
        inputs: self (Game object) and a tile object
        returns: nothing
        does: draws a tile at the row and column number of the input tile in
              the color of the input tile
        '''
        
        # Set turtle settings
        turt = turtle.Turtle()
        turt.speed(0)
        turt.hideturtle()

        # Determine start point of tile such that tile is centered w/in square
        xy_max = self.n/2 * self.square_size
        x = -xy_max + self.square_size / 2 + self.square_size * tile.col
        radius = 0.4 * self.square_size
        y = xy_max - self.square_size / 2 - radius - self.square_size * tile.row

        # Draw tile
        turt.penup()
        turt.goto(x, y)
        turt.color(tile.color, tile.color)
        turt.begin_fill()
        turt.circle(radius)
        turt.end_fill()
        
    
    def setup_game(self):
        '''
        name: setup_game
        inputs: self (Game object)
        returns: nothing
        does: Draws first four tiles in the middle of the game board
        '''
        # Dictionary containing row, col, and color of first four tiles
        first_four = {0 : [self.n/2 - 1, self.n/2 -1, 'white'],
                      1 : [self.n/2, self.n/2, 'white'],
                      2 : [self.n/2 - 1, self.n/2, 'black'],
                      3 : [self.n/2, self.n/2 - 1, 'black']}

        # Loop through dictionary keys
        for key in first_four:
            # Create tile
            row = first_four[key][0]
            col = first_four[key][1]
            new_tile = Tile(first_four[key][2], row, col)

            # Add tile to game tiles
            self.tiles.append(new_tile)

            # Draw tile on board
            self.draw_tile(new_tile)
            
        # Write scores above board
        self.update_turn_display()
        self.update_scores()




    def determine_turn(self):
        '''
        name: determine_turn
        inputs: self
        returns: string 
        does: Determines who's turn it is (player or computer) and initiates
        turn. If neither player nor computer have any legal moves, ends game
        '''
        # Find player's legal moves
        legal_player_moves = self.find_legal_moves('black')

        # Check if player has legal moves and is player turn is true
        if len(legal_player_moves) > 0 \
           and self.is_player_turn:
            # Initiate player turn
            print("Player's Turn")
            self.update_turn_display()
            turtle.onscreenclick(self.player_move)
            return "Player Turn Over"

        # Find computer's legal moves
        legal_comp_moves = self.find_legal_moves('white')
        
        # Check if computer has legal moves
        if len(legal_comp_moves) > 0:
            print("Computer's Turn")
            # Disable player turn
            turtle.onscreenclick(None)
            self.is_player_turn = False
            # Initiate computer turn
            self.computer_move(legal_comp_moves)
            return "Computer Turn Over"
        
        # If computer didn't have legal moves, check if player has legal moves
        if len(legal_player_moves) > 0:
            # Initiate player turn
            print("Player's Turn")
            self.is_player_turn = True
            self.update_turn_display()
            turtle.onscreenclick(self.player_move)
            return "Player Turn Over"  
        # Otherwise end game
        else:
            # Change game's is_game_over property to True
            self.is_game_over = True
            self.update_turn_display()
            # Close turtle window
            turtle.bye()
            return "Game Over"
            
    def player_move(self, x, y):
        '''
        name: player_move
        inputs: self (Game object), x (float), y (float)
        returns: nothing
        does: Draws a tile of the appropriate color in a square that the user
        clicks on if the move is valid and on the board
        '''
        
        # Find legal moves
        legal_moves = self.find_legal_moves('black')

        # Determine row and column of click location
        row = self.get_row(y)
        col = self.get_col(x)

        # Check that row and col are on the board
        if row != -1 and col != -1:
            # Create new tile
            new_tile = Tile('black', row, col)
            # Create new move
            move = LegalMove(new_tile)
            # Check that chosen square is empty and move is legal
            if new_tile not in self.tiles and move in legal_moves:
                    # Draw  new tile
                    self.draw_tile(new_tile)

                    # Add new tile to Game tiles
                    self.tiles.append(new_tile)

                    # Flip necessary tiles
                    move_index = legal_moves.index(move)
                    self.flip_tiles(legal_moves[move_index])
            
                    # Update scores
                    self.update_scores()

                    # End player turn
                    self.is_player_turn = False

                    # Determine who moves next
                    self.determine_turn()

    def get_col(self, x):
        '''
        name: get_col
        inputs: self (Game object) and x
        returns: column number (integer)
        does: Given an x from a user click, this function returns the column
              number of that x
        '''
        # Maximum possible x based on board size and square size
        x_max = self.n/2 * self.square_size
        # Initialize column number
        col = -1
        # Loop from 0 to the number of squares per column
        for i in range(self.n):
            # Upper bound of x
            upper = -x_max + self.square_size * (i + 1)
            # Lower bound of x
            lower = -x_max + self.square_size * i
            # Check if input falls within upper and lower bounds
            if x < upper and x > lower:
                # Return ith column number
                return i
        # Return -1 if x is not within the board
        return -1

    def get_row(self, y):
        '''
        name: get_row
        inputs: self (Game object) and y
        returns: row number (integer)
        does: Given a y from a user click, this function returns the row
              number of that y
        '''
        # Maximum possible y based on board size and square size
        y_max = self.n/2 * self.square_size

        # Loop from 0 to number of squares per row
        for i in range(self.n):
            # Upper bound of y
            upper = y_max - self.square_size * i
            # Lower bound of y
            lower = y_max - self.square_size * (i + 1)
            # Check if y falls within upper and lower bounds
            if y < upper and y > lower:
                # Return ith row number
                return i
        # Return -1 if y is not within the board
        return -1


    def find_legal_moves(self, color):
        '''
        name: find_legal_moves
        inputs: self and color (string)
        returns: list of legal move objects
        does: Loops through every existing tile of specified color and returns
        list of every possible legal move
        '''
        # Initialize list for storing legal moves
        legal_moves = []

        # Loop through game tiles
        for tile in self.tiles:
            # If tile color matches input color
            if tile.color == color:
                # Loop through directions (up, down, right, left, diagonals)
                for direction in self.directions:

                    # Set row and col adders for traversing directions
                    row_add = self.directions[direction][0]
                    col_add = self.directions[direction][1]

                    # Create tile object for tracing current tile
                    current = Tile(tile.color, tile.row + row_add, \
                                   tile.col + col_add)

                    # Initialize list for storing indices of tiles to flip
                    current_flip_indices = []

                    # Loop through game tiles
                    while current in self.tiles:

                        # Find index of current tile
                        current_index = self.tiles.index(current)

                        # If tile of same color exists on path, break loop
                        if self.tiles[current_index].color == tile.color:
                            current_flip_indices = []
                            break
                        # Otherwise, append current tile index to flip indices
                        else:
                            current_flip_indices.append(current_index)

                        # Move current tile to next tile
                        current.row += row_add
                        current.col += col_add

                    # Check tiles to flip exist and current tile is on board
                    if len(current_flip_indices) > 0 \
                       and current.row < self.n and current.row >= 0 \
                       and current.col < self.n and current.col >= 0:

                        # Create legal move object
                        new_move = LegalMove(current)

                        # If move doesn't already exist in legal moves
                        if new_move not in legal_moves:
                            # Set moves flip indices
                            new_move.flip_indices = current_flip_indices
                            # Append to legal moves
                            legal_moves.append(new_move)
                        # Otherwise, update existing move's flip indices
                        else:
                            move_index = legal_moves.index(new_move)
                            move_to_update = legal_moves[move_index]
                            for flip_ind in current_flip_indices:
                                if flip_ind not in move_to_update.flip_indices:
                                    move_to_update.flip_indices.append(flip_ind)
        # Return list of legal moves
        return legal_moves

    def flip_tiles(self, move):
        '''
        name: flip_tiles
        inputs: self (game object) and move (legal move object)
        returns: nothing
        does: Changes color of tiles with indices in move's flip indices list
        '''
        
        # List of indices for tiles that must change color for chosen move
        flip_indices = move.flip_indices

        # Loop through each index
        for index in flip_indices:
            # Get color of tile at current index
            color = self.tiles[index].color

            # Determine opposite color
            if color  == 'black':
                opp_color = 'white'
            else:
                opp_color = 'black'
            
            # Flip tile's color
            self.tiles[index].color = opp_color
            
            # Redraw tile
            self.draw_tile(self.tiles[index])

    def determine_best_move(self, legal_moves):
        '''
        name: computer_move
        inputs: self
        returns: best move for computer (LegalMove object)
        does: Finds "best" move for computer by finding legal move that results
        in most tile flips
        '''
         # Create a dummy tile 
        dummy_tile = Tile('red', -1, -1)

        # Create new legal move object with dummy tile
        move = LegalMove(dummy_tile)

        # Loop through legal moves
        for potential_move in legal_moves:
            # If potential move in loop has same or more tile flips than move
            if len(potential_move.flip_indices) >= len(move.flip_indices):
                # Set move to potential move 
                move = potential_move

        return move
    
    def computer_move(self, legal_moves):
        '''
        name: computer_move
        inputs: self
        returns: nothing
        does: Makes "best" move for computer
        '''
        # Update turn display
        self.update_turn_display()
        
        # Find best move for computer
        move = self.determine_best_move(legal_moves)

        # Append move's tile to list of game tiles
        self.tiles.append(move.tile)

        # Add time delay
        time.sleep(30)
        
        # Draw new move's tile on board
        self.draw_tile(move.tile)
        
        # Flip appropriate tiles
        self.flip_tiles(move)

        # Update the scores
        self.update_scores()
        
        # Set is player turn property to True
        self.is_player_turn = True

        # Determine who moves next
        self.determine_turn()



    def get_score(self):
        '''
        name: get_score
        inputs: self (Game object)
        returns: nothing
        does: Prints the score of the game and the winner of the game 
        '''

        # Count the number of black and white tiles
        black_count = self.count_tiles("black")
        white_count = self.count_tiles("white")
        score_string = "Final Score: Black {} to White {}".format(black_count,\
                                                                  white_count)

        # Determine winner
        if black_count > white_count:
            message = "Black wins!"
        elif black_count < white_count:
            message = "White wins!"
        else:
            message = "It's a tie"

        self.final_player_score = black_count

        # Return summary message
        game_over_message = "GAME OVER!\n" + score_string + "\n" + message

        return game_over_message

    def sort_players(self, players):
        '''
        name: sort_players
        inputs: self and list of player objects
        returns: none
        does: Sorts input list of player objects by score (highest to lowest)
        using bubble sort
        '''
        # Check that games list of players is greater than 1
        if len(players) > 1:

            # Initialize indices for players to compare
            start_index = 0
            next_index = 1

            # Initialize counter for number of comparisons w/out a swap
            no_swaps_count = 0

            # Loop as long as no swaps count is less than number of players
            while no_swaps_count < len(players) - 1:
                current_player = players[start_index]
                next_player = players[next_index]
                # Compare current player and next player's scores
                if current_player.score < next_player.score:
                    # Swap if next player has higher score than current player
                    players.insert(next_index, players.pop(start_index))
                    # Reset no swaps count
                    no_swaps_count = 0
                # Otherwise increment no swaps count
                else:
                    no_swaps_count += 1

                # Increment start_ index
                start_index += 1
                # If not at the end of players list
                if next_index + 1 < len(players):
                    # Increment start and next indices
                    start_index + 1
                    next_index += 1
                # Otherwise reset start and next indices
                else:
                    start_index = 0
                    next_index = 1  

    
    def read_player_history(self):
        '''
        name: read_player_history
        inputs: self
        returns: list of player objects
        does: Creates sorted list of player objects by reading from scores.txt
        '''
        # Create scores file if it does not already exist
        scores_file = open("scores.txt", 'a')
        scores_file.close()

        # Try to read from file
        try:
            scores_file = open("scores.txt", 'r')
            data_string = scores_file.read()
            scores_file.close()

            # Initiate players list 
            players = []

            # Split data string by lines
            data_lines = data_string.splitlines()
            # Loop through each line
            for line in data_lines:
                # Create list of each space seperated string in line
                line_strings = line.split(" ")
                # Initiate string for storing player name
                name = ""
                # Append every string to name except last
                for i in range(len(line_strings) - 1):
                    if i != len(line_strings) - 2:
                        name += line_strings[i] + " "
                    else:
                        name += line_strings[i]
                # Last string in line is score
                score = int(line_strings[len(line_strings) - 1])

                # Create new player object with name and score
                player = Player(name, score)

                # Append player object to players list
                players.append(player)

        # Otherwise print error message
        except OSError:
            print("Could not open 'scores.txt'")

        # Return players list
        return players
                    
    def save_new_player(self, player_name):
        '''
        name: save_new_player
        input: self and player name (string)
        returns: none
        does: Appends player's name and score to text file of previous players
        and scores in appropriate order(highest score first)
        '''
        # Read players from scores.txt into self.players
        players = self.read_player_history()
        
        # Create new player object
        new_player = Player(player_name, self.final_player_score)
        players.append(new_player)

        # Sort players by score (highest score first)
        self.sort_players(players)

        # Initialize string for storing player data
        data_string = ""
        
        # Create data string from players_lst
        for player in players:
            data_string += player.name + " " + str(player.score) + "\n"
        
        # Try to append scores.txt file
        try:
            # Clear scores.txt
            clear_file = open("scores.txt", 'w')
            clear_file.close()
            # Append to scores.txt
            scores_file = open("scores.txt", 'a')
            scores_file.write(data_string)
            scores_file.close()

        # Otherwise print error message
        except OSError:
            print("Error appending player to 'scores.txt'")
        

'''
HW7 - Othello Test Suite
Fall 2018
Jeremy Lee
12/2/18

This program tests all non-graphics related methods of the Player, Tile,
LegalMove, and Game classes for Othello. For test case details, read the
comments under each test methods name. 
'''


from game_classes_final import *
import unittest
import turtle

class TestOthello(unittest.TestCase):
    # Testing Player Methods-----------------------------------------------------
    def test_Player_eq(self):
        '''
        Test cases
        - Input is two equal player objects
        - Input is two unequal player objects (name is different)
        - Input is two unequal player objects (scores are different)
        '''
        # Test player objects
        player1 = Player('player1', 1)
        player2 = Player('player1', 1)
        player3 = Player('player2', 0)
        player4 = Player('player1', 0)

        # Tests
        self.assertTrue(player1.__eq__(player2), True)
        self.assertFalse(player1.__eq__(player3), False)
        self.assertFalse(player1.__eq__(player4), False)

    # Testing Tile Methods-----------------------------------------------------
    def test_Tile_eq(self):
        '''
        Test Cases:
        - Input is two equal tile objects
        - Input is two unequal tile objects (different rows and cols)
        - Input is two unequal tile objects (different cols)
        - Input is two unequal tile objects (different rows)
        '''
        # Test tile objects
        tile1 = Tile('black', 1, 1)
        tile2 = Tile('white', 1, 1)
        tile3 = Tile('black', 0, 0)
        tile4 = Tile('black', 1, 0)
        tile5 = Tile('black', 0, 1)

        # Tests
        self.assertEqual(tile1.__eq__(tile2), True)
        self.assertEqual(tile1.__eq__(tile3), False)
        self.assertEqual(tile1.__eq__(tile4), False)
        self.assertEqual(tile1.__eq__(tile5), False)
        
    # Testing LegalMove Methods------------------------------------------------
    def test_LegalMove_eq(self):
        '''
        Test Cases
        - Inputs have the same tile (same row and col)
        - Inputs have tiles with same row and col, but different flip indices
        - Inputs have different tiles
        '''
        # Test move objects
        move1 = LegalMove(Tile('black', 1, 1))
        move2 = LegalMove(Tile('white', 1, 1))
        move3 = LegalMove(Tile('black', 1, 1))
        move3.flip_indices = [1, 2, 3]
        move4 = LegalMove(Tile('black', 0, 1))

        # Tests
        self.assertEqual(move1.__eq__(move2), True)
        self.assertEqual(move1.__eq__(move3), True)
        self.assertEqual(move1.__eq__(move4), False)
        
    # Testing Game Methods------------------------------------------------------
    def test1_Game_setup_game(self):
        '''
        Tests Game's setup_game method on three different board sizes by
        checking that appropriate tiles created and appended to Game object's
        tiles list
        - 4x4
        - 6x6
        - 8x8
        '''
        turtle.clear()
        
        # List of game objects to test
        games = [Game(4, 50), Game(6, 50), Game(8, 50)]

        # Expected game tiles lists after running setup_game
        four_expected = [Tile('white', 1, 1), Tile('white', 2,2),\
                          Tile('black', 1, 2), Tile('black', 2, 1)]
        six_expected = [Tile('white', 2, 2), Tile('white', 3, 3),\
                          Tile('black', 2, 3), Tile('black', 3, 2)]
        eight_expected = [Tile('white', 3, 3), Tile('white', 4, 4),\
                          Tile('black', 3, 4), Tile('black', 4, 3)]
        expected_results = [four_expected, six_expected, eight_expected]

        # Loop through each game object
        for i in range(len(games) - 1):
            # Clear screen
            games[i].draw_board()
            # Setup the game
            games[i].setup_game()
            # Check that correct tiles were created
            self.assertEqual(games[i].tiles, expected_results[i])
            turtle.clear()
        
    def test_Game_player_move_invalid(self):
        '''
        Tests Game's player_move method for invalid move cases on 4x4 board
        - Player clicks off the board
        - Player clicks a square that already has a tile
        - Player clicks a square that is not a legal move
        '''
        
        # Initialize game
        game = Game(4, 50)
        game.tiles.append(Tile('white', 1, 1))
        game.tiles.append(Tile('white', 2, 2))
        game.tiles.append(Tile('black', 3, 3))
        
        # Off the board
        game.player_move(-1000, -1000)
        # In a square that is already filled
        game.player_move(-25, 25)
        game.player_move(25, -25) 
        game.player_move(75, -75)
        # Empty square but illegal move
        game.player_move(-25, 75) 
        game.player_move(25, 75)
        game.player_move(75, 75)
        game.player_move(25, 25)
        game.player_move(75, 25)
        game.player_move(75, -25)
        game.player_move(25, -75)
        game.player_move(-25, -75)
        game.player_move(-75, -75)
        game.player_move(-25, -25)
        game.player_move(-75, -25)

        # Check that no tiles added
        self.assertEqual(len(game.tiles), 3)

        # Check that tile colors did not change
        self.assertEqual(game.tiles[0].color, 'white')
        self.assertEqual(game.tiles[1].color, 'white')
        
    def test_Game_valid_player_move_and_determine_turn(self):
        '''
        Testing Game's player_move method for case that user clicks on a
        valid board square and has chosen a legal move

        Also tests that determine_turn method properly prompts computer to
        move after player and ends game when no legal moves left for both
        computer and player
        '''
        # Clear turtle graphics window
        turtle.clear()

        # Initialize game
        game = Game(4, 50)

        # Redraw board
        game.draw_board()
        
        # Initialize board so player and computer have only one legal move each
        game.tiles = [Tile('white', 1, 1), Tile('white', 2, 2), \
                      Tile('black', 3, 3), Tile('white', 1,3)]
        for tile in game.tiles:
            game.draw_tile(tile)

        # Make valid player move (placing tile at row 1, col 1)
        # This also initiates determine_turn method
        game.player_move(-75, 75)
        
        # Known tile for only legal player move on board
        player_tile = Tile('black', 1, 1)

        # Known tile for only legal computer move after player moves
        comp_tile = Tile('white', 3, 1)

        # Check that player tile exists in game
        self.assertTrue(player_tile in game.tiles)
        # Check that computer tile exists in game
        self.assertTrue(comp_tile in game.tiles)
        # Check that game over property set to True
        self.assertTrue(game.is_game_over)
        
        
    def test_Game_get_col(self):
        '''
        Tests Game's get_col method for every valid col of a 4x4 board and 2
        invalid cols (off the board)
        '''
        # 4x4 Game object with square size of 50
        game = Game(4, 50)

        # Test cases 
        self.assertEqual(game.get_col(-51), 0)
        self.assertEqual(game.get_col(-49), 1)
        self.assertEqual(game.get_col(1), 2)
        self.assertEqual(game.get_col(51), 3)
        self.assertEqual(game.get_col(-101), -1)
        self.assertEqual(game.get_col(101), -1)

    def test_Game_get_row(self):
        '''
        Tests Game's get_row method for every valid row of a 4x4 board and
        2 invalid rows (off the board)
        '''
        # 4x4 Game object with square size of 50
        game = Game(4, 50)

        # Test cases
        self.assertEqual(game.get_row(99), 0)
        self.assertEqual(game.get_row(49), 1)
        self.assertEqual(game.get_row(-1), 2)
        self.assertEqual(game.get_row(-51), 3)
        self.assertEqual(game.get_row(-101), -1)
        self.assertEqual(game.get_row(101), -1)

    def test_Game_find_legal_moves(self):         
        '''
        Tests Game's find_legal_move methods for the following cases:
        - Legal moves exist for both black and white
        - Legal moves do NOT exist for black
        - Legal moves do Not exist for white
        '''
        game = Game(8, 50)
        # Case 1: Legal moves available for both black and white --------------
        white1 = Tile('white', 3, 3)
        white2 = Tile('white', 4, 4)
        black1 = Tile('black', 3, 4)
        black2 = Tile('black', 4, 3)
        game.tiles = [white1, white2, black1, black2]

        # Known legal moves for white for game setup
        white1_move1 = LegalMove(Tile('white', 5, 3))
        white1_move1.flip_indices = [2]
        white1_move2 = LegalMove(Tile('white', 3, 5))
        white1_move2.flip_indices = [2]
        white2_move1 = LegalMove(Tile('white', 2, 4))
        white2_move1.flip_indices = [3]
        white2_move2 = LegalMove(Tile('white', 4, 2))
        white2_move2.flip_indices = [3]
        # List of known legal moves for white
        white_moves = [white1_move1, white1_move2, white2_move1, white2_move2]
        
        # Known legal moves for black for game setup
        black1_move1 = LegalMove(Tile('black', 5, 4))
        black1_move1.flip_indices = [1]
        black1_move2 = LegalMove(Tile('black', 3, 2))
        black1_move2.flip_indices = [0]
        black2_move1 = LegalMove(Tile('black', 4, 5))
        black2_move1.flip_indices = [1]
        black2_move2 = LegalMove(Tile('black', 2, 3))
        black2_move2.flip_indices = [0]
        # List of known legal moves for black
        black_moves = [black1_move1, black1_move2, black2_move1, black2_move2]

        # Check that find_legal_moves method returns expected results
        self.assertEqual(game.find_legal_moves('white'), white_moves)
        self.assertEqual(game.find_legal_moves('black'), black_moves)

        # Case 2: No legal moves available for black ---------------------------
        game.tiles[0].color = 'black'
        game.tiles[1].color = 'black'
        self.assertEqual(game.find_legal_moves('black'), [])

        # Case 3: No legal moves available for white --------------------------
        for tile in game.tiles:
            tile.color = 'white'
        self.assertEqual(game.find_legal_moves('white'), [])
        
    def test_Game_sort_players(self):
        '''
        Testing Game's sort_players method for the following cases
        - Empty list of players
        - List of 1 player
        - List of 3 players (unsorted) with three different scores
        - List of 3 players already sorted
        '''
        # Create game object
        game = Game(8, 50)

        # Create player objects
        player1A = Player("player1", 10)
        player2 = Player("player2", 100)
        player1B = Player("player1", 50)

        # Test cases
        empty = []
        one_player = [player1A]
        three_players_unsorted = [player1A, player2, player1B]
        three_players_sorted = [player2, player1B, player1A] 

        # Expected results
        empty_result = []
        one_player_result = [player1A]
        three_players_unsorted_result = [player2, player1B, player1A]
        three_players_sorted_result = [player2, player1B, player1A]

        # Call sort function on test cases
        game.sort_players(empty)
        game.sort_players(one_player)
        game.sort_players(three_players_unsorted)
        game.sort_players(three_players_sorted)

        # Check results
        self.assertEqual(empty, empty_result)
        self.assertEqual(one_player, one_player_result)
        self.assertEqual(three_players_unsorted, three_players_unsorted_result)
        self.assertEqual(three_players_sorted, three_players_sorted_result)

    def test_Game_flip_tiles_white(self):
        '''
        Test Cases
        - Flipping 4 tiles from black to white, one by one
        '''
        turtle.clear()
        
        # Create game object
        game = Game(8, 50)
        game.draw_board()
        
        # Create test tiles
        game.tiles = [Tile('black', 3, 3), Tile('black', 3, 4), \
                      Tile('black', 4, 3), Tile('black', 4, 4)]
        for tile in game.tiles:
            game.draw_tile(tile)
            
        # Create test legal move for white tiles
        move = LegalMove(Tile('white', 3, 3))

        # Loop from 0 to 3
        for i in range(len(game.tiles)):
            # Append new index to flip indices
            move.flip_indices.append(i)
            # Flip specified tile colors
            game.flip_tiles(move)
            # Check that color flip was successful
            self.assertEqual(game.tiles[i].color, 'white')
        
    def test_Game_flip_tiles_black(self):
        '''
        Test Cases
        - Flipping 4 tiles from white to black, one by one
        '''
        turtle.clear()
        
        # Create game object
        game = Game(8, 50)
        game.draw_board()

        # Create test tiles
        game.tiles = [Tile('white', 3, 3), Tile('white', 3, 4), \
                      Tile('white', 4, 3), Tile('white', 4, 4)]
        for tile in game.tiles:
            game.draw_tile(tile)

        # Create test legal move for white tiles
        move = LegalMove(Tile('black', 3, 3))

        # Loop from 0 to 3
        for i in range(len(game.tiles)):
            # Append new index to flip indices
            move.flip_indices.append(i)
            # Flip specified tile colors
            game.flip_tiles(move)
            # Check that color flip was successful
            self.assertEqual(game.tiles[i].color, 'black')

    def test_Game_determine_best_move(self):
        '''
        Tests Game's determine_best_move method for following cases
        - Three legal moves, each with different # of tile flips
        - Two legal moves with different #'s of tile flips
        - Two legal moves with the same #'s of tile flips
        - One legal move
        '''
        game = Game(8, 50)

        # LegalMove objects for testing
        move1 = LegalMove(Tile('white', 1, 1))
        move1.flip_indices = [0, 1, 2, 3, 4, 5, 6, 7]
        move2 = LegalMove(Tile('white', 0, 1))
        move2.flip_indices = [0, 1]
        move3 = LegalMove(Tile('white', 1,0))
        move3.flip_indices = [0, 1, 2]
        move4 = LegalMove(Tile('white', 2, 2))
        move4.flip_indices = [0, 5, 7]

        # Test inputs:
        # Three legal moves with different numbers of tile flips
        legal_moves = [move1, move2, move3]
        # Two legal moves with different numbers of tile flips
        legal_moves2 = [move2, move3]
        # Two legal moves with the same number of tile flips
        legal_moves3 = [move3, move4]
        # One legal move
        legal_moves4 = [move1]

        # Check that calling method returns expected 'best' move
        self.assertEqual(game.determine_best_move(legal_moves), move1)
        self.assertEqual(game.determine_best_move(legal_moves2), move3)
        self.assertEqual(game.determine_best_move(legal_moves3), move4)
        self.assertEqual(game.determine_best_move(legal_moves4), move1)
    
    def test_Game_read_player_history(self):
        '''
       Tests Game's read_player_history method for the following cases:
        - scores.txt contains three player-score pairs
        - scores.txt is empty
        - scores.txt contains one player-score pair where name has mult. spaces
        '''
        # Create game object
        game = Game(8, 50)

        # Create txt file for testing
        test_file = open("scores.txt", 'a')
        test_file.close()

        # Test cases
        test1 = "Player1 50\nPlayer2 15\nPlayer3 5"
        test2 = ""
        test3 = "Really long player name 99"

        # Expected outputs
        output1 = [Player("Player1", 50), Player("Player2", 15),\
                   Player("Player3", 5)]
        output2 = []
        output3 = [Player("Really long player name", 99)]

        # Dictionary (key = test input, value = expected output)
        test_dict = {test1 : output1, test2 : output2, test3 : output3}

        for test in test_dict:
            try:
                # Write test string to scores.txt
                test_file = open("scores.txt", 'w')
                test_file.write(test)
                test_file.close()
                # Check that method returns correct list of player objects
                self.assertEqual(game.read_player_history(), test_dict[test])
            except OSError:
                print("Could not write to 'scores.txt'")      

    
    def test_Game_save_new_player(self):
        '''
        Tests Game's save_new_player method using read_player_history method to
        check that new player objects have been created and added in the correct
        order to scores.txt
        '''
        try:
            # Clear scores.txt
            scores_clear = open('scores.txt','w')
            scores_clear.close()

            # Create new game object
            game = Game(8, 50)

            # Create test player objects
            player1 = Player("player1", 50)
            player2 = Player("player2", 61)
            player3 = Player("player3", 60)
            player4 = Player("player4", 5)
            player5 = Player("player2", 64)

            # Dictionary of player names (keys) and list of scores and expected results
            player_dict = { "player1" : [50, [player1]],
                            "player2" : [61, [player2, player1]],
                            "player3" : [60, [player2, player3, player1]],
                            "player4" : [5, [player2, player3, player1, player4]]}
            
            # Loop through each player name in player_dict
            for player in player_dict:
                # Set Game's player score
                game.final_player_score = player_dict[player][0]
                # Save new player
                game.save_new_player(player)
                # Check if new player was created correctly and added in correct order
                self.assertEqual(game.read_player_history(), player_dict[player][1])

            # Test case where multiple instances of same player name exist 
            game.final_player_score = player5.score
            game.save_new_player(player5.name)
            expected_result = [player5, player2, player3, player1, player4]
            self.assertEqual(game.read_player_history(), expected_result)
            
        except OSError:
            print("Could not open 'scores.txt'")

        
    def test_Game_get_score(self):
        '''
        Tests Game's get_score method for the following cases:
        - Player has more tiles than computer
        - Computer has more tiles than Player
        - Player and computer have equal number of tiles
        '''
        # Game object
        game = Game(8, 50)
        
        # Game tiles cases
        player_win_tiles = [Tile('black', 1, 0), Tile('black', 1, 1), \
                            Tile('white', 0, 0)]
        comp_win_tiles = [Tile('white', 1, 0), Tile('black', 1, 1), \
                          Tile('white', 0, 0)]
        tie_tiles = [Tile('white', 1, 0), Tile('black', 1, 1)]
        test_inputs = [player_win_tiles, comp_win_tiles, tie_tiles]

        # Expected game over messages
        player_win_message = "GAME OVER!\nFinal Score: Black 2 to White 1\n"\
                             "Black wins!"
        comp_win_message = "GAME OVER!\nFinal Score: Black 1 to White 2\n"\
                           "White wins!"
        tie_message = "GAME OVER!\nFinal Score: Black 1 to White 1\n"\
                      "It's a tie"
        expected_outputs = [player_win_message, comp_win_message, tie_message]       

        # Loop through each test input and test for expected output
        for i in range(len(test_inputs)):
            game.tiles = test_inputs[i]
            self.assertEqual(game.get_score(), expected_outputs[i])
    
        
def main():
    unittest.main(verbosity = 3)
    turtle.mainloop()
main()

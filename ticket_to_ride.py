"""
Args:
-m or --mode: Score or Game.
-g or --game_name: Path to the cards.
-p or --players: Number of Players 

Returns:
Nothing, prints out people's score and error messages for card.txt without a matching edge.txt
"""

import argparse
from enum import Enum
from ticket_to_ride_game import TicketToRideGame
import ticket_to_ride_input_reader


class Mode(Enum) :
    """
    Class Enum for Mode
    """

    SCORE = 'score'
    GAME = 'game'

    def __str__(self):
        return self.value


parser = argparse.ArgumentParser()
FOLDER_HELP = "The folder where all cards reside, does not include recursion into subfolders."
parser.add_argument("-m", "--mode", type=Mode,
                    choices=list(Mode), help="Mode either game or score.")
parser.add_argument("-g", "--game_name", type=str, help=FOLDER_HELP)
NUM_PLAYERS_HELP = "The Number of Players by the rules less than 6 but"
NUM_PLAYERS_HELP += " I didn't implement that logic yet."
parser.add_argument("-p", "--players",
                    type=int, help=NUM_PLAYERS_HELP, required=False, default=None)

args = parser.parse_args()
# print(args)
mode = args.mode
game_name = args.game_name

if mode == Mode.GAME:
    number_players = int(args.players)
    new_game = TicketToRideGame('./game_setup/usa_game_board.txt', game_name)
    # new_game.print_game_board()
    new_game.play_game(number_players)
    new_game.print_players()


    playersList = ticket_to_ride_input_reader.read_folder(f"./{game_name}/")
    for cardset in playersList:
        score = ticket_to_ride_input_reader.score_card_set(cardset[1], cardset[2])
        print(cardset[0], "got a score of", score)
elif mode == Mode.SCORE:
    # print("Here")
    playersList = ticket_to_ride_input_reader.read_folder(f"./{game_name}/")
    for cardset in playersList:
        score = ticket_to_ride_input_reader.score_card_set(cardset[1], cardset[2])
        print(cardset[0], "got a score of", score)

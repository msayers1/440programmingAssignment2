"""
Args:
folder (): Path to the cards.

Returns:
Nothing, prints out people's score and error messages for card.txt without a matching edge.txt

"""

import argparse
import ticket_to_ride_input_reader


parser = argparse.ArgumentParser()
FOLDER_HELP = "The folder where all cards reside, does not include recursion into subfolders."
parser.add_argument("folder", type=str, help=FOLDER_HELP)

args = parser.parse_args()
folderPath = args.folder
playersList = ticket_to_ride_input_reader.read_folder(folderPath)
for cardset in playersList:
    score = ticket_to_ride_input_reader.score_card_set(cardset[1], cardset[2])
    print(cardset[0], "got a score of", score)

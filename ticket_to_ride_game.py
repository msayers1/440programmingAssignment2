"""
Args:
?

Returns:
?
"""
import dataclasses
import random
import csv
import os
from enum import Enum
from ticket_to_ride_input_reader import CITY_A, CITY_B,TRAINS, ROUTE_POINTS, trains_to_points
from filemanager import add_to_file, create_file, count_lines, read_file
#Global Constants
ROUTE_SLOT_A = 'route_slot_a'
ROUTE_SLOT_B = 'route_slot_b'
DOUBLE = 'double'
GAME_DIRECTORY = './game/'

def create_empty_file(game, player):
    """
    Args:
    player: name of player
    
    Returns:
    Nothing 
    """
    filename = f"./{game}/card-{player}.txt"
    create_file(filename)
    # with open(filename, 'w', encoding="utf-8"):
    #     pass
    filename = f"./{game}/edge-{player}.txt"
    create_file(filename)
    # with open(filename, 'w', encoding="utf-8"):
    #     pass


def add_route_to_file(game, player, route):
    """
    Args:
    player: name of player
    route: route object being recorded to the file. 

    Returns:
    Nothing 
    """
    filename = f"./{game}/edge-{player}.txt"
    route_string = f"{route[CITY_A]}:{route[CITY_B]}:{route[TRAINS]}"
    add_to_file(filename, route_string)
    # with open(filename, 'a', encoding="utf-8") as file:
    #     file.write(route_string + '\n')




def fetch_first_name():
    """
    Args:
    none

    Returns:
    random first name.
    """
    filename = './game_setup/random_names.csv'
    max_value = count_lines(filename)
    line_number = random.randint(1, max_value)
    with open(filename, 'r', encoding="utf-8") as csv_file:

        csv_reader = csv.reader(csv_file)
        for i, row in enumerate(csv_reader, start=1):
            if i == line_number:
                return row[0]

    return None
# Enumarate for Player type
class RouteColor(Enum) :
    """
    Args:
    filename: name of file for game board.

    Returns:
    class of ticket_to_ride_game
    """
    WHITE = 'White'
    YELLOW = 'Yellow'
    BLUE = 'Blue'
    RED = 'Red'
    GREEN = 'Green'
    BLACK = 'Black'
    PINK = 'Pink'
    ORANGE = 'Orange'
    GREY = 'Grey'

    def __str__(self):
        return self.value

# function to create the route dictionary.
def create_game_route_dictionary(destination_array):
    """
    Args:
    destination_array: the array of routes in the edge text file.

    Returns:
    route dictionary: a card of city a, city b, number of trains, 
        the points based off that number of trains, route slot a, 
        route slot b (which will be the color or none). 
    """
    route_dictionary = {}
    # print(destination_array, " | ", len(destination_array), " | ", destination_array[3])
    route_dictionary.update({CITY_A: destination_array[0]})
    # end or Destination 2
    route_dictionary.update({CITY_B: destination_array[1]})
    # The number of trains is in the text file so you need to convert to points.
    route_dictionary.update({TRAINS: destination_array[2]})
    points = trains_to_points(destination_array[2])
    route_dictionary.update({ROUTE_POINTS: points})
    route_dictionary.update({ROUTE_SLOT_A: destination_array[3]})
    if len(destination_array) > 4 and destination_array[4] != '':
        route_dictionary.update({ROUTE_SLOT_B: destination_array[4]})
        route_dictionary.update({DOUBLE: True})
    else:
        route_dictionary.update({ROUTE_SLOT_B: None})
        route_dictionary.update({DOUBLE: False})
    return route_dictionary
# Function to read card file

# # Read the game_board file.
# def read_game_board_file(filename):
#     """
#     Args:
#     filename: the filename of the game board file.
#
#     Returns:
#     list of routes: list of routes from a game_board.txt
#     """
#     routes = []
#     with open(filename, 'r', encoding="utf-8") as f:
#         all_lines = f.readlines()
#         route = None
#         for line in all_lines:
#             line_without_newline = line[:-1]
#             route_array = line_without_newline.split(':')
#             route = create_game_route_dictionary(route_array)
#             routes.append(route)
#     return routes

# Function to create the Graph Adjancency List. Really a dictionary of lists.
def create_game_graph_adjacency_list(routes):
    """
    Args:
    routes: list of routes from a file.

    Returns:
    route adjaceny list: dictionary of all the cities with a list for each of all
    the connected cities to that one. 
    """
    route_adjaceny_list = {}
    for route in routes:
        city_a = route[CITY_A]
        city_b = route[CITY_B]
        add_route_to_game_graph_adjacency_list(route_adjaceny_list, city_a, city_b, route)
        add_route_to_game_graph_adjacency_list(route_adjaceny_list, city_b, city_a, route)
    return route_adjaceny_list

# Function to separate out the logic to add the route to the list, I decided to call the
# route twice instead of spelling out the two different ways to log it in one function.
def add_route_to_game_graph_adjacency_list(route_adjaceny_list, source, end, route):
    """
    Args:
    route_adjaceny_list: Adjacency list of the routes that the previous function is building.
    source: city a or the first city
    end: city b or the second city

    Returns:
    Nothing it modifies the route_adjacency_list which is passed into it. 
    """
    if source in route_adjaceny_list.keys():
        if end not in route_adjaceny_list[source]:
            route_adjaceny_list[source].update({end:route})
    else:
        route_adjaceny_list[source] = {}
        route_adjaceny_list[source].update({end:route})

# Enumarate for Player type
class PlayerType(Enum) :
    """
    Args:
    filename: name of file for game board.

    Returns:
    class of ticket_to_ride_game
    """
    USER = 'user'
    COMP_LEVEL_1 = 'comp_level_1'
    COMP_LEVEL_2 = 'comp_level_2'
    COMP_LEVEL_3 = 'comp_level_3'

    def __str__(self):
        return self.value

@dataclasses.dataclass
class Player:
    """
    Args:
    player_name: name of player
    player_type_value: type of player ( user vs comp ( including level of comp, 
                                                maybe eventually play style))

    Returns:
    class of player
    """
    name: str
    score: int
    player_type: PlayerType
    game_name: str
    train_tokens: int

    def __init__(self,name, player_type, game_name):
        self.name = name
        self.player_type = player_type
        self.train_tokens = 45
        self.score = 0
        self.game_name = game_name
        create_empty_file(game_name, name)

    def place_route(self, route_object):
        """
        Args:
        route_object: route to place. 

        Result:
        Route is added to the file, score adjusted and trains deducted. 
        """
        add_route_to_file(self.game_name, self.name, route_object)
        self.score += int(route_object[ROUTE_POINTS])
        self.train_tokens -= int(route_object[TRAINS])

class TicketToRideGame:
    """
    Args:
    filename: name of file for game board.

    Returns:
    class of ticket_to_ride_game
    """
    game_adjaceny_list: {}
    player_list: []
    remaining_route_list: []
    active_player: int
    turn_counter: int
    game_name: str

    def __init__(self, filename, game_name):
        folder_path = f"./{game_name}/"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        # self.remaining_route_list = read_game_board_file(filename)
        self.remaining_route_list = read_file(filename, ':', create_game_route_dictionary)
        # print(self.remaining_route_list)
        self.game_adjaceny_list = create_game_graph_adjacency_list(self.remaining_route_list)
        self.player_list = []
        self.active_player = 0
        self.turn_counter = 0
        self.game_name = game_name

    def add_player(self, player_name, player_type_value):
        """
        Method off TicketToRideGame class
        Args:
        player_name: name of player
        player_type_value: type of player (user vs comp(including level of comp))
        Result:
        adds player to game. 
        """
        self.player_list.append(Player(player_name, player_type_value, self.game_name))
    def check_game_status(self):
        """
        Method off TicketToRideGame class
        Args:
        None
        Result:
        Checks game. 
        """
        for player in self.player_list:
            # print(player.train_tokens, " | ", (player.train_tokens < 3))
            if player.train_tokens < 3:
                return False
        return True

    def set_active_player(self, player_index):
        """
        Method off TicketToRideGame class
        Args:
        player_index: index of player
        Result:
        sets active player 
        """
        if player_index < len(self.player_list):
            self.active_player = player_index
        else:
            self.active_player = 0

    def take_turn(self, active_player):
        """
        Method off TicketToRideGame class
        Args:
        active_player: index of active player
        Result:
        active player takes a turn
        """
        route_number = random.randint(1, len(self.remaining_route_list)-1)
        route_trains = int(self.remaining_route_list[route_number][TRAINS])
        player_train_tokens = self.player_list[active_player].train_tokens
        if route_trains < player_train_tokens:
            self.player_list[active_player].place_route(self.remaining_route_list[route_number])
            self.remaining_route_list.pop(route_number)

    def play_game(self, number_players):
        """
        Method off TicketToRideGame class
        Args:
        player_index: index of player
        Result:
        runs through a game 
        """
        for _ in range(number_players):
            # print(fetch_first_name())
            self.add_player(fetch_first_name(),'comp_level_1')
        # self.set_active_player(0)
        while self.check_game_status():
            self.take_turn(self.active_player)
            self.print_players()
            self.set_active_player(self.active_player+1)

    def print_game_board(self):
        """
        Method off TicketToRideGame class
        Args:
        none
        Result:
        prints out city list with connected cities. 
        """
        # print(self.game_adjaceny_list)
        for city, city_list in self.game_adjaceny_list.items():
            city_list_string = ''
            for destination, route in city_list.items():
                city_list_string += destination + '(' + str(route[TRAINS]) + '|'
                city_list_string += str(route[ROUTE_POINTS]) + '|'
                city_list_string += route[ROUTE_SLOT_A] + '|' + str(route[ROUTE_SLOT_B]) +'), '
            city_list_string = city_list_string[:-2]
            print(city, ":", city_list_string)

    def print_players(self):
        """
        Method off TicketToRideGame class
        Args:
        none
        Result:
        prints out city list with connected cities. 
        """
        players_string = ''
        # print(dir(self))
        for player in self.player_list:
            players_string += f"{player.name} has a score of {str(player.score)} "
            players_string += f"and {str(player.train_tokens)} trains left, "
        players_string = players_string[:-2]
        players_string += '.'
        print(players_string)

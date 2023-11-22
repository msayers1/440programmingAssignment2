"""
Ticket to Ride Scoring Script
"""
# Global OS - providing accces to the OS.
import os
from filemanager import read_file
# Global variable to switch between depth vs breadth searches
DEPTH_VS_BREADTH = True
# DEPTH_VS_BREADTH = False
SPECIFIC_CARDS = False
# SPECIFIC_CARDS = True
FOLDER_OPTIONS = True
# FOLDER_OPTIONS = False
playersList = []
#Global Constants
DESTINATION1 = 'destination1'
DESTINATION2 = 'destination2'
TRAINS = 'trains'
DESTINATION_POINTS = 'destination_points'
CITY_A = 'city_a'
CITY_B = 'city_b'
ROUTE_POINTS = 'route_points'

# Function to read a folder.


def read_folder(folder_path):
    """
    Args:
    folder_path (str): Path to the cards.

    Returns:
    list: List of tuples of ( player name(str), card filenames with path (str),
    edge filenames with path (str) )
    """
    # Get a list of all files in the folder
    files = [f for f in os.listdir(folder_path) if os.path.isfile(
        os.path.join(folder_path, f))]
    # print(files)
    # Filter files to only card files
    card_files = [f for f in files if f.startswith('card')]
    for card in card_files:
        key = card[card.find("-")+1:card.find(".")]
        # print(key)
        edge_filename = folder_path + "edge-" + key + ".txt"
        print(edge_filename)
        # check if the edge file exists.
        if os.path.exists(edge_filename):
            card_filename = folder_path + card
            playersList.append((key, card_filename, edge_filename))
        else:
            print("Error: missing edge card for: ", key)
            # print(playersList)
    return playersList

# Function to create a destination card.


def create_destination_card(destination_array):
    """
    Args:
    destination_array: Path to the cards.

    Returns:
    dictionary of destination1, destination2, destination points of 
        a destination card. 
    """
    destination_card = {}
    destination_card.update({DESTINATION1: destination_array[0]})
    destination_card.update({DESTINATION2: destination_array[1]})
    destination_card.update({DESTINATION_POINTS: destination_array[2]})
    return destination_card
# Function to take the number of trains and return the points those trains are worth.


def trains_to_points(trains):
    """
    Args:
    trains: Number of trains.

    Returns:
    int (points) based on number of trains
    """
    trains_num = int(trains)
    train_conversion = [0,1,2,4,7,10,15]
    return train_conversion[trains_num]
    # if trains_num == 1:
    #     return 1
    # if trains_num == 2:
    #     return 2
    # if trains_num == 3:
    #     return 4
    # if trains_num == 4:
    #     return 7
    # if trains_num == 5:
    #     return 10
    # if trains_num == 6:
    #     return 15
    # return None

# function to create the route dictionary.


def create_route_dictionary(destination_array):
    """
    Args:
    destination_array: the array of routes in the edge text file.

    Returns:
    route dictionary: a card of city a, city b, number of trains, 
    and the points based off that number of trains. 
    """
    route_dictionary = {}
    route_dictionary.update({CITY_A: destination_array[0]})
    # end or Destination 2
    route_dictionary.update({CITY_B: destination_array[1]})
    # The number of trains is in the text file so you need to convert to points.
    route_dictionary.update({TRAINS: destination_array[2]})
    points = trains_to_points(destination_array[2])
    route_dictionary.update({ROUTE_POINTS: points})
    return route_dictionary
# Function to read card file


def read_card_file(filename):
    """
    Args:
    filename: the filename of the card file. 

    Returns:
    a list of destination cards: the card text file has the destination cards, 
    the list has the list of cards in the file. 
    """
    destination_cards = []
    with open(filename, 'r', encoding="utf-8") as f:
        all_lines = f.readlines()
        dest = None
        for line in all_lines:
            dest_array = line.split(':')
            dest = create_destination_card(dest_array)
            destination_cards.append(dest)
    return destination_cards

# Function to read the Edge file


# def read_edge_file(filename):
#     """
#     Args:
#     filename: the filename of the edge file.

#     Returns:
#     list of routes: list of routes from an edge file.
#     (Possibly also used for a game_board.txt also)
#     """
#     routes = []
#
#     return routes

# Function to create the Graph Adjancency List. Really a dictionary of lists.
def create_graph_adjacency_list(routes):
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
        add_route_to_graph_adjacency_list(route_adjaceny_list, city_a, city_b)
        add_route_to_graph_adjacency_list(route_adjaceny_list, city_b, city_a)
    return route_adjaceny_list

# Function to separate out the logic to add the route to the list, I decided to call the
# route twice instead of spelling out the two different ways to log it in one function.
def add_route_to_graph_adjacency_list(route_adjaceny_list, source, end):
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
            route_adjaceny_list[source].append(end)
    else:
        route_adjaceny_list[source] = []
        route_adjaceny_list[source].append(end)

# Function to switch between depth first and breadth first searchs.
def check_card(route_adjaceny_list, card):
    """
    Args:
    route_adjaceny_list: is the adjacency list to be checked.  
    card: the destination card to be checked. 

    Returns:
    Destination points: either + or - of the destination points of the card provided
    depened upon whether there was a route between the cities. 
    """
    # Holds the cities checked.
    checked = []
    # tells if the destination card was met or not.
    result = False
    # Allows swapping between Breadth vs depth
    if DEPTH_VS_BREADTH:
        result = depth_first_search(
            route_adjaceny_list, checked, card[DESTINATION1], card[DESTINATION2])
    else:
        result = breadth_first_search(
            route_adjaceny_list, checked, card[DESTINATION1], card[DESTINATION2])
    # checks the result and leaves the destination points as is, or if not met,
    # then places a negative sign on it.
    if result:
        return int(card[DESTINATION_POINTS])
    return -1 * int(card[DESTINATION_POINTS])

# Breadth first search to dive in and see if they are connected.


def breadth_first_search(route_adjaceny_list, checked, source, end):
    """
    Args:
    route_adjaceny_list: Adjacency list to check whether there is a route between two cities
    checked: list of cites checked (could really be a optional argument but would need to be shifted
            to the end)
    source: city a or first city
    end: city b or second city or destination

    Returns:
    True or False whether or not there is a route between the two cities or True when the two 
    cities are the same.
    """
    # Marks the source as checked.
    checked.append(source)
    # print("Source", source)
    # If you find the city then return true.
    if source == end:
        return True
    # Make sure the source is in the route_adjaceny_list.
    if source in route_adjaceny_list.keys():
        # print("Source List", route_adjaceny_list[source])
        # chekc to see if the source is connected to the end.
        # Basically checking the breadth at once.
        if end in route_adjaceny_list[source]:
            return True
        # Now you dive into each city in the list.
        for city in route_adjaceny_list:
            # Make sure it is not checked already.
            if city not in checked:
                # print("To the next level", checked, city)
                # Call the recursive function with city as the source now.
                if breadth_first_search(route_adjaceny_list, checked, city, end):
                    return True
            # else:
            #     return False
    return False

# Depth first search to dive in and see if they are connected.


def depth_first_search(route_adjaceny_list, checked, source, end):
    """
    Args:
    route_adjaceny_list: Adjacency list to check whether there is a route between two cities
    checked: list of cites checked (could really be a optional argument but would need to be shifted
            to the end)
    source: city a or first city
    end: city b or second city or destination

    Returns:
    True or False whether or not there is a route between the two cities or True when the two 
    cities are the same.
    """
    # Marks the source as checked.
    checked.append(source)
    # Check if you found the city.
    if source == end:
        return True
    # Make sure the source is in the route list.
    if source in route_adjaceny_list.keys():
        # check each city
        for city in route_adjaceny_list[source]:
            # Check if you found it.
            if city == end:
                # print("It returned true once")
                return True
            # Before you move on, then you dive in and search down that city.
            if city not in checked and depth_first_search(route_adjaceny_list, checked, city, end):
                return True
    return False

# Function to score a card set.


def score_card_set(card_filename, edge_filename):
    """
    Args:
    card_filename: the filename of the card file. 
    edge_filename: the filename of the edge file. 

    Returns:
    local_score: score of the game. 
    """
    destinations = read_card_file(card_filename)
    # routes = read_edge_file(edge_filename)
    routes = read_file(edge_filename,':',create_route_dictionary)
    player_name = card_filename[card_filename.find("-")+1:card_filename.find(".", 1)]
    adjacency_list = create_graph_adjacency_list(routes)
    local_score = 0
    number_of_trains = 0
    # Score the routes
    for route in routes:
        local_score += int(route[ROUTE_POINTS])
        number_of_trains += int(route[TRAINS])
    # Score the destination cards.
    if number_of_trains > 45:
        error_string = "There seems to be too many routes for " + player_name + ", he"
        error_string += " seems to have used " + str(number_of_trains)
        print(error_string)
    for destination_card in destinations:
        local_score += check_card(adjacency_list, destination_card)
    return local_score


# Checks if you want to do specific cards.
# if SPECIFIC_CARDS:
#     card_filename_str = './cards/card-example.txt'
#     edge_filename_str = './cards/edge-example.txt'
#     score = scoreCardSet(card_filename_str, edge_filename_str)
#     print("Your Example Score:", score)
#     card_filename_str = './cards/card-test2.txt'

#     edge_filename_str = './cards/edge-test2.txt'
#     score = scoreCardSet(card_filename_str, edge_filename_str)
#     print("Your Test2 Score:", score)

# if FOLDER_OPTIONS:
#     folderPath = './cards/'
#     playersList = read_folder(folderPath)
#     for cardset in playersList:
#         score = scoreCardSet(cardset[1], cardset[2])
#         print(cardset[0], "got a score of", score)

# print(adjacencyList)
# for source, destinations in adjacencyList:
#     destinationString = ''
#     for destination in destinations:
#             destinationString += destination + ' '
#     print(source, " is connected to ", destinationString)

# print(destinations)
# for route in routes:
# print(route[DESTINATION1], ' to ', route[DESTINATION2], ', worth:', route.route_points,
#                                                                               ' points.' )

# for card in destinations:
#         if check_card(adjacencyList, card):
#             print(card[DESTINATION1], ' is connected to ', card[DESTINATION2],
#                                               ' worth:', card[DESTINATION_POINTS])
#         else:
#             print(card[DESTINATION1], ' is not connected to ', card[DESTINATION2],
#                                               ' deduct:', card[DESTINATION_POINTS])

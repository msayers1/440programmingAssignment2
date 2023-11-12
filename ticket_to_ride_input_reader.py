"""
Ticket to Ride Scoring Script
"""
# Global OS - providing accces to the OS.
import os
# Global variable to switch between depth vs breadth searches
DEPTH_VS_BREADTH = True
# DEPTH_VS_BREADTH = False
SPECIFIC_CARDS = False
# SPECIFIC_CARDS = True
FOLDER_OPTIONS = True
# FOLDER_OPTIONS = False
playersList = []

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
        # check if the edge file exists.
        if os.path.exists(edge_filename):
            card_filename = folder_path + card
            playersList.append((key, card_filename, edge_filename))
        else:
            print("Error: missing edge for: ", key)
            # print(playersList)
    return playersList

# Function to create a destination card.


def create_destination_card(destination_array):
    """
    Args:
    destination_array (): Path to the cards.

    Returns:
    list: List of tuples of ( player name(str), card filenames with path (str),
    edge filenames with path (str) )
    """
    destination_card = {}
    destination_card.update({"destination1", destination_array[0]})
    destination_card.update({"destination2",destination_array[1]})
    destination_card.update({"destination_points",destination_array[2]})
    return destination_card
# Function to take the number of trains and return the points those trains are worth.


def trains_to_points(trains):
    """
    Add this docstring
    """
    trains_num = int(trains)
    if trains_num == 1:
        return 1
    if trains_num == 2:
        return 2
    if trains_num == 3:
        return 4
    if trains_num == 4:
        return 7
    if trains_num == 5:
        return 10
    if trains_num == 6:
        return 15

# function to create the route dictionary.


def create_route_dictionary(destination_array):
    """
    Add this docstring
    """
    route_dictionary = {}
    route_dictionary.update({'destination1', destination_array[0]})
    # end or Destination 2
    route_dictionary.update({"destination2", destination_array[1]})
    # The number of trains is in the text file so you need to convert to points.
    route_dictionary.update({'trains', destination_array[2]})
    points = trains_to_points(destination_array[2])
    route_dictionary.update({"route_points", points})
    return route_dictionary
# Function to read card file


def read_card_file(filename):
    """
    Add this docstring
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


def read_edge_file(filename):
    """
    Add this docstring
    """
    routes = []
    with open(filename, 'r', encoding="utf-8") as f:
        all_lines = f.readlines()
        route = None
        for line in all_lines:
            route_array = line.split(':')
            route = create_route_dictionary(route_array)
            routes.append(route)
    return routes

# Function to create the Graph Adjancency List. Really a dictionary of lists.


def create_graph_adjacency_list(routes):
    """
    Add this docstring
    """
    route_list = {}
    for route in routes:
        city_a = route['destination1']
        city_b = route['destination2']
        add_route_to_graph_adjacency_list(route_list, city_a, city_b)
        add_route_to_graph_adjacency_list(route_list, city_b, city_a)
    return route_list

# Function to separate out the logic to add the route to the list, I decided to call the
# route twice instead of spelling out the two different ways to log it in one function.


def add_route_to_graph_adjacency_list(route_list, source, end):
    """
    Add this docstring
    """
    if source in route_list.keys():
        if end not in route_list[source]:
            route_list[source].append(end)
    else:
        route_list[source] = []
        route_list[source].append(end)

# Function to switch between depth first and breadth first searchs.


def check_card(route_list, card):
    """
    Add this docstring
    """
    # Holds the cities checked.
    checked = []
    # tells if the destination card was met or not.
    result = False
    # Allows swapping between Breadth vs depth
    if DEPTH_VS_BREADTH:
        result = depth_first_search(
            route_list, checked, card["destination1"], card["destination2"])
    else:
        result = breadth_first_search(
            route_list, checked, card["destination1"], card["destination2"])
    # checks the result and leaves the destination points as is, or if not met,
    # then places a negative sign on it.
    if result:
        return int(card.destination_points)
    else:
        return -1 * int(card.destination_points)

# Breadth first search to dive in and see if they are connected.


def breadth_first_search(route_list, checked, source, end):
    """
    Add this docstring
    """
    # Marks the source as checked.
    checked.append(source)
    # print("Source", source)
    # If you find the city then return true.
    if source == end:
        return True
    # Make sure the source is in the route_list.
    if source in route_list.keys():
        # print("Source List", route_list[source])
        # chekc to see if the source is connected to the end.
        # Basically checking the breadth at once.
        if end in route_list[source]:
            return True
        else:
            # Now you dive into each city in the list.
            for city in route_list:
                # Make sure it is not checked already.
                if city not in checked:
                    # print("To the next level", checked, city)
                    # Call the recursive function with city as the source now.
                    if breadth_first_search(route_list, checked, city, end):
                        return True
                # else:
                #     return False
    else:
        return False

# Depth first search to dive in and see if they are connected.


def depth_first_search(route_list, checked, source, end):
    """
    Add this docstring
    """
    # Marks the source as checked.
    checked.append(source)
    # Check if you found the city.
    if source == end:
        return True
    # Make sure the source is in the route list.
    if source in route_list.keys():
        # check each city
        for city in route_list[source]:
            # Check if you found it.
            if city == end:
                # print("It returned true once")
                return True
            else:
                # Before you move on, then you dive in and search down that city.
                if city not in checked and depth_first_search(route_list, checked, city, end):
                    return True
    else:
        return False
    return False

# Function to score a card set.


def score_card_set(card_filename, edge_filename):
    """
    Add this docstring
    """
    destinations = read_card_file(card_filename)
    routes = read_edge_file(edge_filename)
    adjacency_list = create_graph_adjacency_list(routes)
    local_score = 0
    # Score the routes
    for route in routes:
        local_score += int(route.route_points)
        number_of_trains += int(route.trains)
    # Score the destination cards.
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
# print(route["destination1"], ' to ', route["destination2"], ', worth:', route.route_points,
#                                                                               ' points.' )

# for card in destinations:
#         if check_card(adjacencyList, card):
#             print(card["destination1"], " is connected to ", card["destination2"],
#                                               " worth:", card["destination_points"])
#         else:
#             print(card["destination1"], " is not connected to ", card["destination2"],
#                                               " deduct:", card["destination_points"])

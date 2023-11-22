# library for argument parsing in python

import argparse

# Global variable to switch between depth vs breadth searches
DEPTH_VS_BREADTH = True # Depth Search
# DEPTH_VS_BREADTH = False # Breadth Search
#Global Constants
DESTINATION1 = 'destination1'
DESTINATION2 = 'destination2'
TRAINS = 'trains'
DESTINATION_POINTS = 'destination_points'
CITY_A = 'city_a'
CITY_B = 'city_b'
ROUTE_POINTS = 'route_points'



# Function to create a destination card.


def create_destination_card(destination_array):
    """
    Args:
    destination_array: Path to the cards.

    Returns:
    dictionary of destination1, destination2, destination points of 
        a destination card. 
    """
    # Initiate a dictionary
    destination_card = {}
    #set the Destionation 1. 
    destination_card.update({DESTINATION1: destination_array[0]})
    #set the Destionation 2. 
    destination_card.update({DESTINATION2: destination_array[1]})
    #set the Destionation points. 
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
    # Ensure the input is an int. 
    trains_num = int(trains)
    # Build a list of the points related to the # of trains. 
    train_conversion = [0,1,2,4,7,10,15]
    # Return the points based on the number of trains. 
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
    # initiaite a dictionary. 
    route_dictionary = {}
    route_dictionary.update({CITY_A: destination_array[0]})
    # end or Destination 2
    route_dictionary.update({CITY_B: destination_array[1]})
    # The number of trains is in the text file so you need to convert to points.
    route_dictionary.update({TRAINS: destination_array[2]})
    # call trainss to points to convert to points. 
    points = trains_to_points(destination_array[2])
    # set points. 
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
    # Initiate dictionary
    destination_cards = []
    #runs through the file. 
    with open(filename, 'r', encoding="utf-8") as f:
        # read all lines. 
        all_lines = f.readlines()
        # set a variable to hold
        dest = None
        # then work through each line. 
        for line in all_lines:
            # Split the line by the delimeter. 
            dest_array = line.split(':')
            # add the array into a desitnation card. 
            dest = create_destination_card(dest_array)
            # append it to the dictionary
            destination_cards.append(dest)
    # return dictionary
    return destination_cards

# Function to read the Edge file


def read_edge_file(filename):
    """
    Args:
    filename: the filename of the edge file. 

    Returns:
    list of routes: list of routes from an edge file. (Possibly also used for a game_board.txt also)
    """
    # Create Dictionary for routes
    routes = []
    # read file
    with open(filename, 'r', encoding="utf-8") as f:
        # read all lines from file. 
        all_lines = f.readlines()
        # initiate a holder for individual 
        route = None
        # go line by line. 
        for line in all_lines:
            # split line by delimeter and stick in array. 
            route_array = line.split(':')
            # takes route array and builds a route
            route = create_route_dictionary(route_array)
            # append route to dictionary
            routes.append(route)
    # Return route dictionary. 
    return routes

# Function to create the Graph Adjancency List. Really a dictionary of lists.
def create_graph_adjacency_list(routes):
    """
    Args:
    routes: list of routes from a file.

    Returns:
    route adjacency list: dictionary of all the cities with a list for each of all
    the connected cities to that one. 
    """
    # Create a route adjacency
    route_adjacency_list = {}
    # iterate over routes
    for route in routes:
        # grab city a
        city_a = route[CITY_A]
        # grab city b
        city_b = route[CITY_B]
        # add city a to city b route then add city b to city a. 
        add_route_to_graph_adjacency_list(route_adjacency_list, city_a, city_b)
        add_route_to_graph_adjacency_list(route_adjacency_list, city_b, city_a)
    # Return Adjacency List. 
    return route_adjacency_list

# Function to separate out the logic to add the route to the list, I decided to call the
# route twice instead of spelling out the two different ways to log it in one function.
def add_route_to_graph_adjacency_list(route_adjacency_list, source, end):
    """
    Args:
    route_adjacency_list: Adjacency list of the routes that the previous function is building.
    source: city a or the first city
    end: city b or the second city

    Returns:
    Nothing it modifies the route_adjacency_list which is passed into it. 
    """
    # checks if source is in the dictionary. 
    if source in route_adjacency_list.keys():
        # checks if the end is not in the list for the source. 
        if end not in route_adjacency_list[source]:
            # add end to the list for source. 
            route_adjacency_list[source].append(end)
    else:
        # add the source to the dictionary
        route_adjacency_list[source] = []
        # add the end to the list for source in the dictionary. 
        route_adjacency_list[source].append(end)

# Function to switch between depth first and breadth first searchs.
def check_card(route_adjacency_list, card):
    """
    Args:
    route_adjacency_list: is the adjacency list to be checked.  
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
            route_adjacency_list, checked, card[DESTINATION1], card[DESTINATION2])
    else:
        result = breadth_first_search(
            route_adjacency_list, checked, card[DESTINATION1], card[DESTINATION2])
    # checks the result and leaves the destination points as is, or if not met,
    # then places a negative sign on it.
    if result:
        return int(card[DESTINATION_POINTS])
    return -1 * int(card[DESTINATION_POINTS])

# Breadth first search to dive in and see if they are connected.
def breadth_first_search(route_adjacency_list, checked, source, end):
    """
    Args:
    route_adjacency_list: Adjacency list to check whether there is a route between two cities
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
    # Make sure the source is in the route_adjacency_list.
    if source in route_adjacency_list.keys():
        # print("Source List", route_adjacency_list[source])
        # chekc to see if the source is connected to the end.
        # Basically checking the breadth at once.
        if end in route_adjacency_list[source]:
            return True
        # Now you dive into each city in the list.
        for city in route_adjacency_list:
            # Make sure it is not checked already.
            if city not in checked:
                # print("To the next level", checked, city)
                # Call the recursive function with city as the source now.
                if breadth_first_search(route_adjacency_list, checked, city, end):
                    return True
            # else:
            #     return False
    return False

# Depth first search to dive in and see if they are connected.


def depth_first_search(route_adjacency_list, checked, source, end):
    """
    Args:
    route_adjacency_list: Adjacency list to check whether there is a route between two cities
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
    if source in route_adjacency_list.keys():
        # check each city
        for city in route_adjacency_list[source]:
            # Check if you found it.
            if city == end:
                # print("It returned true once")
                return True
            # Before you move on, then you dive in and search down that city.
            if city not in checked and depth_first_search(route_adjacency_list, checked, city, end):
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
    routes = read_edge_file(edge_filename)
    # player_name = card_filename[card_filename.find("-")+1:card_filename.find(".", 1)]
    adjacency_list = create_graph_adjacency_list(routes)
    local_score = 0
    # Used if using the 45 train logic. 
    # number_of_trains = 0
    # Score the routes
    for route in routes:
        local_score += int(route[ROUTE_POINTS])
        # Used if using the 45 train logic. 
        # number_of_trains += int(route[TRAINS])
    # Logic to verify that the edge.txt doesn't use more than 45 trains. 
    # if number_of_trains > 45:
        # error_string = "There seems to be too many routes for " + player_name + ", he"
        # error_string += " seems to have used " + str(number_of_trains)
        # print(error_string)
    # Score the destination cards.
    for destination_card in destinations:
        local_score += check_card(adjacency_list, destination_card)
    # return local score
    return local_score

# main function, code is executed here if the script is run

if __name__ == '__main__':

    # load argument parser

    parser = argparse.ArgumentParser()

    # arguments for data sources

    parser.add_argument('-e', '--edges', type=str, default='edge.txt', help='Name of file that contains edges')

    parser.add_argument('-c', '--cards', type=str, default='card.txt', help='Name of file that contains cards')

    # parse arguments from command line

    args = parser.parse_args()

    

    # load edges filename into variable

    edges_filename = args.edges



    # load card filename into variable

    cards_filename = args.cards

    #call score function to get score
    score = score_card_set(cards_filename, edges_filename)

    #print the score
    print(score)
    
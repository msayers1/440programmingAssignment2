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

# Class to hol the destination cards.


class DestinationCard():
    """
    Args:
    destination_array (): Path to the cards.

    Returns:
    list: List of tuples of ( player name(str), card filenames with path (str),
    edge filenames with path (str) )
    """
    destination1: str
    destination2: str
    destinationPoints: int

    def __init__(self, destination_array):
        """
        Add this docstring
        """
        self.destination1 = destination_array[0]
        self.destination2 = destination_array[1]
        self.destinationPoints = destination_array[2]

# Function to take the number of trains and return the points those trains are worth.


def trains_to_points(trains):
    """
    Add this docstring
    """
    trainsNum = int(trains)
    if trainsNum == 1:
        return 1
    if trainsNum == 2:
        return 2
    if trainsNum == 3:
        return 4
    if trainsNum == 4:
        return 7
    if trainsNum == 5:
        return 10
    if trainsNum == 6:
        return 15

# Class to hold the route objects.


class RouteObject():
    """
    Add this docstring
    """
    destination1: str
    destination2: str
    routePoints: int

    def __init__(self, destination_array):
        # Source or Destination 1
        self.destination1 = destination_array[0]
        # end or Destination 2
        self.destination2 = destination_array[1]
        # The number of trains is in the text file so you need to convert to points.
        points = trains_to_points(destination_array[2])
        self.routePoints = points

# Function to read card file


def readCardFile(filename):
    """
    Add this docstring
    """
    DestinationCards = []
    with open(filename, 'r', encoding="utf-8") as f:
        all_lines = f.readlines()
        dest = None
        for line in all_lines:
            destArray = line.split(':')
            dest = DestinationCard(destArray)
            DestinationCards.append(dest)
    return DestinationCards

# Function to read the Edge file


def readEdgeFile(filename):
    """
    Add this docstring
    """
    routes = []
    with open(filename, 'r', encoding="utf-8") as f:
        all_lines = f.readlines()
        route = None
        for line in all_lines:
            routeArray = line.split(':')
            route = RouteObject(routeArray)
            routes.append(route)
    return routes

# Function to create the Graph Adjancency List. Really a dictionary of lists.


def createGraphAdjacencyList(routes):
    """
    Add this docstring
    """
    routeList = {}
    for route in routes:
        cityA = route.destination1
        cityB = route.destination2
        addRouteToGraphAdjacencyList(routeList, cityA, cityB)
        addRouteToGraphAdjacencyList(routeList, cityB, cityA)
    return routeList

# Function to separate out the logic to add the route to the list, I decided to call the route twice instead of spelling out the two different ways to log it in one function.


def addRouteToGraphAdjacencyList(routeList, source, end):
    """
    Add this docstring
    """
    if source in routeList.keys():
        if end not in routeList[source]:
            routeList[source].append(end)
    else:
        routeList[source] = []
        routeList[source].append(end)

# Function to switch between depth first and breadth first searchs.


def checkCard(routeList, card):
    """
    Add this docstring
    """
    # Holds the cities checked.
    checked = []
    # tells if the destination card was met or not.
    result = False
    # Allows swapping between Breadth vs depth
    if DEPTH_VS_BREADTH:
        result = depthFirstSearch(
            routeList, checked, card.destination1, card.destination2)
    else:
        result = breadthFirstSearch(
            routeList, checked, card.destination1, card.destination2)
    # checks the result and leaves the destination points as is, or if not met,
    # then places a negative sign on it.
    if result:
        return int(card.destinationPoints)
    else:
        return -1 * int(card.destinationPoints)

# Breadth first search to dive in and see if they are connected.


def breadthFirstSearch(routeList, checked, source, end):
    """
    Add this docstring
    """
    # Marks the source as checked.
    checked.append(source)
    # print("Source", source)
    # If you find the city then return true.
    if source == end:
        return True
    # Make sure the source is in the routeList.
    if source in routeList.keys():
        # print("Source List", routeList[source])
        # chekc to see if the source is connected to the end.
        # Basically checking the breadth at once.
        if end in routeList[source]:
            return True
        else:
            # Now you dive into each city in the list.
            for city in routeList:
                # Make sure it is not checked already.
                if city not in checked:
                    # print("To the next level", checked, city)
                    # Call the recursive function with city as the source now.
                    if breadthFirstSearch(routeList, checked, city, end):
                        return True
                # else:
                #     return False
    else:
        return False

# Depth first search to dive in and see if they are connected.


def depthFirstSearch(routeList, checked, source, end):
    """
    Add this docstring
    """
    # Marks the source as checked.
    checked.append(source)
    # Check if you found the city.
    if source == end:
        return True
    # Make sure the source is in the route list.
    if source in routeList.keys():
        # check each city
        for city in routeList[source]:
            # Check if you found it.
            if city == end:
                # print("It returned true once")
                return True
            else:
                # Before you move on, then you dive in and search down that city.
                if city not in checked and depthFirstSearch(routeList, checked, city, end):
                    return True
    else:
        return False
    return False

# Function to score a card set.


def scoreCardSet(card_filename, edge_filename):
    """
    Add this docstring
    """
    destinations = readCardFile(card_filename)
    routes = readEdgeFile(edge_filename)
    adjacencyList = createGraphAdjacencyList(routes)
    local_score = 0
    # Score the routes
    for route in routes:
        local_score += int(route.routePoints)
    # Score the destination cards.
    for destination_card in destinations:
        local_score += checkCard(adjacencyList, destination_card)
    return local_score


# Checks if you want to do specific cards.
if SPECIFIC_CARDS:
    card_filename_str = './cards/card-example.txt'
    edge_filename_str = './cards/edge-example.txt'
    score = scoreCardSet(card_filename_str, edge_filename_str)
    print("Your Example Score:", score)
    card_filename_str = './cards/card-test2.txt'

    edge_filename_str = './cards/edge-test2.txt'
    score = scoreCardSet(card_filename_str, edge_filename_str)
    print("Your Test2 Score:", score)

if FOLDER_OPTIONS:
    folderPath = './cards/'
    playersList = read_folder(folderPath)
    for cardset in playersList:
        score = scoreCardSet(cardset[1], cardset[2])
        print(cardset[0], "got a score of", score)

# print(adjacencyList)
# for source, destinations in adjacencyList:
#     destinationString = ''
#     for destination in destinations:
#             destinationString += destination + ' '
#     print(source, " is connected to ", destinationString)

# print(destinations)
# for route in routes:
# print(route.destination1, ' to ', route.destination2, ', worth:', route.routePoints, ' points.' )

# for card in destinations:
#         if checkCard(adjacencyList, card):
#             print(card.destination1, " is connected to ", card.destination2,
#                                               " worth:", card.destinationPoints)
#         else:
#             print(card.destination1, " is not connected to ", card.destination2,
#                                               " deduct:", card.destinationPoints)

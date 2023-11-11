import os
#Global variable to switch between depth vs breadth searches
depthVsBreadth = True
# depthVsBreadth = False
specificCards = False
# specificCards = True
folderOption = True
# folderOption = False

#Function to read a folder. 
def readFolder(folder_path):
    # Get a list of all files in the folder
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    # print(files)
    playersList = []
    # Filter files to only card files
    card_files = [f for f in files if f.startswith('card')]
    for card in card_files:
        key = card[card.find("-")+1:card.find(".")]
        # print(key)
        edgeFilename = folder_path + "edge-" + key + ".txt"
        #check if the edge file exists. 
        if os.path.exists(edgeFilename):
            cardFilename = folder_path + card
            playersList.append((key, cardFilename, edgeFilename))
        else:
            print("Error: missing edge for: ", key)
    # print(playersList)
    return playersList



#Class to hol the destination cards.
class destinationCard():
    destination1: str
    destination2: str
    destinationPoints: int

    def __init__(self, destinationArray):
            self.destination1 = destinationArray[0]
            self.destination2 = destinationArray[1]
            self.destinationPoints = destinationArray[2]

#Function to take the number of trains and return the points those trains are worth. 
def trains2points(trains):
    trainsNum = int(trains)
    if (trainsNum == 1):
        return 1
    if (trainsNum == 2):
        return 2
    if (trainsNum == 3):
        return 4
    if (trainsNum == 4):
        return 7
    if (trainsNum == 5):
        return 10
    if (trainsNum == 6):
        return 15

#Class to hold the route objects. 
class routeObject():
    destination1: str
    destination2: str
    routePoints: int

    def __init__(self, destinationArray):
            #Source or Destination 1
            self.destination1 = destinationArray[0]
            #end or Destination 2
            self.destination2 = destinationArray[1]
            #The number of trains is in the text file so you need to convert to points. 
            points = trains2points(destinationArray[2])
            self.routePoints = points

# Function to read card file
def readCardFile(filename) : 
    destinationCards = []
    with open(filename, 'r') as f:
            all_lines = f.readlines()
            dest = None
            for i, line in enumerate(all_lines):
                destArray = line.split(':')
                dest = destinationCard(destArray)
                destinationCards.append(dest)
    return destinationCards

# Function to read the Edge file
def readEdgeFile(filename) : 
    routes = []
    with open(filename, 'r') as f:
            all_lines = f.readlines()
            route = None
            for i, line in enumerate(all_lines):
                routeArray = line.split(':')
                route = routeObject(routeArray)
                routes.append(route)
    return routes

# Function to create the Graph Adjancency List. Really a dictionary of lists. 
def createGraphAdjacencyList(routes):
    routeList = {}   
    for route in routes:
        source = route.destination1
        end = route.destination2
        addRouteToGraphAdjacencyList(routeList, source, end)
        addRouteToGraphAdjacencyList(routeList, end, source)
    return routeList
    
# Function to separate out the logic to add the route to the list, I decided to call the route twice instead of spelling out the two different ways to log it in one function.
def addRouteToGraphAdjacencyList(routeList, source, end):

    if source in routeList.keys():
        if end not in routeList[source]:
                routeList[source].append(end)
    else:
        routeList[source] = []
        routeList[source].append(end)

#Function to switch between depth first and breadth first searchs.
def checkCard(routeList, card):
    #Holds the cities checked. 
    checked = []
    #tells if the destination card was met or not. 
    result = False
    #Allows swapping between Breadth vs depth
    if depthVsBreadth:
        result = depthFirstSearch(routeList, checked, card.destination1, card.destination2)
    else:
        result =  breadthFirstSearch(routeList, checked, card.destination1, card.destination2)
    #checks the result and leaves the destination points as is, or if not met, then places a negative sign on it. 
    if result:
        return int(card.destinationPoints)
    else:
        return -1 * int(card.destinationPoints)
    
# Breadth first search to dive in and see if they are connected. 
def breadthFirstSearch(routeList, checked, source, end):
    #Marks the source as checked. 
    checked.append(source)
    # print("Source", source)
    #If you find the city then return true. 
    if source == end:
        return True
    #Make sure the source is in the routeList. 
    if source in routeList.keys(): 
        # print("Source List", routeList[source])
        #chekc to see if the source is connected to the end. Basically checking the breadth at once. 
        if end in routeList[source]:
            return True
        else:
            #Now you dive into each city in the list. 
            for city in routeList:
                #Make sure it is not checked already. 
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
    #Marks the source as checked. 
    checked.append(source)
    #Check if you found the city.
    if source == end:
        return True
    #Make sure the source is in the route list. 
    if source in routeList.keys(): 
        #check each city
        for city in routeList[source]:
            #Check if you found it. 
            if city == end:
                # print("It returned true once")
                return True
            else:
                #Before you move on, then you dive in and search down that city. 
                if city not in checked and depthFirstSearch(routeList, checked, city, end):
                        return True
    else:
        return False
#Function to score a card set.
def scoreCardSet(cardFilename, edgeFilename):
    destinations = readCardFile(cardFilename)
    routes = readEdgeFile(edgeFilename)
    adjacencyList = createGraphAdjacencyList(routes)
    score = 0
    #Score the routes
    for route in routes:
        score += int(route.routePoints)
    #Score the destination cards. 
    for destinationCard in destinations:
        score += checkCard(adjacencyList, destinationCard)
    return score

if specificCards:
    cardFilename ='./cards/card-example.txt'
    # destinations = readCardFile(filename)

    edgeFilename ='./cards/edge-example.txt'
    # routes = readEdgeFile(filename)
    score = scoreCardSet(cardFilename, edgeFilename)
    print("Your Example Score:", score)
    cardFilename ='./cards/card-test2.txt'
    # destinations = readCardFile(filename)

    edgeFilename ='./cards/edge-test2.txt'
    # routes = readEdgeFile(filename)
    score = scoreCardSet(cardFilename, edgeFilename)
    print("Your Test2 Score:", score)
# adjacencyList = createGraphAdjacencyList(routes)
if folderOption:
    folderPath = './cards/'
    playersList = readFolder(folderPath)
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
#             print(card.destination1, " is connected to ", card.destination2, " worth:", card.destinationPoints)
#         else:
#             print(card.destination1, " is not connected to ", card.destination2, " deduct:", card.destinationPoints)
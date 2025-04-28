# Author: Michael LaGumina
# Date: 4/2/2025
# Description:  The functions contained within this file are for course project data processing

import pandas as pd
import random
import sys
import math
import time
import cityCoords as cc

def createDCMatrix(citiesList):
    """
    This function converts a list of cities into a square dataframe that can later be filled with travel costs between cities on the index and column axes.
    :param p1: citiesList.
    :type p1: List.
    :return: dataframe.
    """
    # Creating square dataframe by using the cities in the list for indices and columns.
    df = pd.DataFrame(index=[i for i in citiesList], columns=[j for j in citiesList])
    return df


def originDestination(dcDict):
    """
    This function takes in a nested dictionary of cities and the distances pertaining to their respective direct connections.  It then prompts the user to select an origin and destination city.  Only cities contained within the nested dictionary can be selected and the origin cannot be the same as the destination.
    :param p1: dcDict.
    :type p1: dictionary.
    :return: tuple of origin and destination strings.
    """
    # Extracting the cities from the dictionary into a list
    cities = [key for key in dcDict.keys()]
    # Storing the cities as a set
    citiesSet = set(cities)

    # Prompting user to provide starting city
    origin = input('Select your starting location: ')

    # While loop to prevent user from selecting city that isn't in dictionary
    while origin not in citiesSet:
        print('Your selection was not one of the supported cities.  Please choose again.')
        origin = input('Select your starting location: ')

    # Removing origin city from set to ensure that it can't be picked as the destination
    citiesSet.remove(origin)

    # Prompting user to provide destination city
    destination = input('Select your destination: ')

    # While loop to prevent user from selecting city that isn't in dictionary
    while destination not in citiesSet:
        print('Your selection was not one of the supported cities.  Please choose again.')
        destination = input('Select your destination: ')

    return origin, destination


def fillDCMatrix(dcDict):
    """
    This function takes in a nested dictionary of cities and the travel costs of the direct connections available to each city.  It outputs a dataframe of the travel cost between each city with 'Nan' values for unconnected cities.
    :param p1: dcDict.
    :type p1: dictionary.
    :return: dataframe.
    """
    # Extracting cities from nested dictionary to be stored in list
    cities = [key for key in dcDict.keys()]
    # Using list of cities to create dataframe with cities as indices and headers
    df = pd.DataFrame(index=[i for i in cities], columns=[j for j in cities])

    # Nested for loops to fill the dataframe with distances between directly connected cities.
    for outerkey in dcDict.keys():
        innerDict = dcDict[outerkey]

        for innerKey in innerDict.keys():
            distance = innerDict[innerKey]
            df.at[outerkey, innerKey] = distance

    return df


def bearingAngle(cityCoordsA, cityCoordsB):
    """
    This function takes in 2 cityCoords class objects, uses the class functions to obtain their latitudes and longitudes in radians, then calculates the bearing angle from A to B.
    :param p1: cityCoordsA
    :type p1: cityCoords class object
    :param p2: cityCoordsB
    :type p2: cityCoords class object
    :return: bearing angle in degrees.
    """    
    #converting coordinates from degrees to radians using cityCoords class functions
    longA = cityCoordsA.longRad()
    latA = cityCoordsA.latRad()
    longB = cityCoordsB.longRad()
    latB = cityCoordsB.latRad()
    
    # Calculating difference of longitudes
    deltaL = longB - longA   
    
    # Calculating bearing angle from point A to point B
    x = math.cos(latB) * math.sin(deltaL)    
    y = (math.cos(latA) * math.sin(latB)) - (math.sin(latA) * math.cos(latB) * math.cos(deltaL))    
    bearing = (math.degrees(math.atan2(x, y)) + 360) % 360
    
    return bearing


def bearingPenalty(bearingToStop, bearingToDest):
    """
    This function takes in the bearing required to get from the current location to the final stop and compares it to the bearing required to get from the current stop to a direct connection city.  Using the differences in the bearing angles, a penalty is generated depending on whether the bearing to the direct connection city is bringing you closer to the target city.
    :param p1: bearingToStop
    :type p1: float (in degrees)
    :param p2: bearingToDest
    :type p2: float (in degrees)
    :return: penalty factor as float.
    """
    # Calculating difference in bearing angle between the ideal bearing (directly toward destination) and the bearing that takes you to the city being evaluated.
    diff = abs(bearingToDest - bearingToStop)
    
    # if the difference is greater than 180 deg, it needs to be calculated from the other direction (CCW rather than CW) since we care only about difference w.r.t. the ideal bearing, not whether we are deviating from it in the CW direction or CCW direction.
    if diff > 180:
        diff = 360 - diff
    
    # Applying a penalty for bearing differences that are generally sending the user closer to the destination.        
    if diff <= 90:
        penaltyMultiplier = (diff / 180) + 1
    
    # Applying a harsher penalty for bearing differences that are generally sending the user away from the destination in the first 45 degrees of the backwards direction.    
    elif diff <= 135:
        print('Moving Backwards in 90-135 deg range')
        penaltyMultiplier = (diff / 180) + 1.5
    
    # Applying the harshest penalty for bearing differences that are generally sending the user backwards w.r.t. the destination in the remaining 45 degrees.    
    else:
        print('Moving Backwards in 135-180 deg range')
        penaltyMultiplier = (diff / 180) + 2
        
    return penaltyMultiplier


def minPath(coordsDF, dcMatrix, current, destination):
    """
    This function takes in a dataframe of cities and their coordinates, a dataframe filled with direct connections travel costs, an origin city, and a destination city.  Using Dijkstra's Algorithm, it returns a list showing the optimal route in the sequence that the cities are traveled to and the total cost of the trip.  It also detects when the destination city is available to be traveled to and records the cost of traveling directly there even if there is a lower cost option available.  This allows the function to compare the Djikstra's Algorithm result to offshoot routes and chooses the lowest cost possibility.
    :param p1: coordsDF.
    :type p1: dataframe.
    :param p2: dcMatrix.
    :type p2: dataframe.
    :param p3: current.
    :type p3: string.
    :param p4: destination.
    :type p4: string.
    :return: tuple of total cost and route as a list.
    """  
    # Obtain coordinates of destination city and create cityCoords class object
    destLat = coordsDF.loc[destination, 'lat']
    destLong = coordsDF.loc[destination, 'lng']
    destination = cc.cityCoords(destination, destLat, destLong)
    
    # Initialize total route cost 
    total = 0    
    
    # Initialize empty set of stops along the route
    stops = set()   
    
    # Initialize route list with current city at the first index position since you must start in the origin city.
    route = [current]    
    
    # Initialize empty skip to end routes list and cost of those routes to track offshoot routes that may be better than strictly following Djikstra's Algorithm.
    skipToEndRoutesList = []
    skipToEndRoutesCost = []
    
    # Entering while loop that will not end until the route brings you to the destination city.    
    while current != destination.getName():
        
        # Initializing shortest leg cost to infinity
        shortestLeg = math.inf 
        
        # Obtaining the coordinates of the current city and using them to create a cityCoords class object
        currentLat = coordsDF.loc[current, 'lat']
        currentLong = coordsDF.loc[current, 'lng']
        
        # setting the starting point variable as a cityCoords class object.
        startingPoint = cc.cityCoords(current, currentLat, currentLong)
        
        # Adding the starting point city to the set of stops
        stops.add(startingPoint.getName())
        
        # for loop to iterate through cities in the direct connection dataframe.
        for i in dcMatrix.columns:            
            # print(f'checking node {startingPoint} to node {i}')  
            
            # checking to see if the cities have a direct connection.
            unconnected = pd.isna(dcMatrix.loc[startingPoint.getName(), i])
            
            # Checking to see if the city being evaluated is directly connected or has already been traveled to along the route.
            if i in stops or unconnected:
                # print(f'node {i} disqualified, been there already')
                continue
            
            # creating cityCoords class object of the candidate city being evaluated.            
            candidateLat = coordsDF.loc[i, 'lat']
            candidateLong = coordsDF.loc[i, 'lng']
            candidate = cc.cityCoords(i, candidateLat, candidateLong)            
            
            # Obtaining the cost of traveling on this direct connection link.
            dcDistance = dcMatrix.loc[startingPoint.getName(), i]
            
            # Using the cityCoords class objects to calculated the bearing angles between them and assign a penalty based on the difference in bearings being evaluated w.r.t. the ideal bearing.
            bearingToStop = bearingAngle(startingPoint, candidate)
            bearingToDest = bearingAngle(startingPoint, destination)            
            directionPenalty = bearingPenalty(bearingToStop, bearingToDest)
            
            # Updating the direct connection cost to account for the direction penalty
            dcDistance = dcDistance * directionPenalty
            # print(f'Currently in {startingPoint.getName()}, evaluating connection to {candidate.getName()}')
            # print(f'Bearing Penalty --> {directionPenalty}')
            
            # Checking whether the city being evaluated is the destination city.  This allows the function to track the total cost of the route if the user were to go directly to the end instead of potentially following Djikstra's Algorithm to a different lower cost connection.
            if i == destination.getName():
                print('\nit is possible to jump directly to the destination')
                # Calculating the total cost of going directly to the end.
                skipToEndCost = round(total + dcDistance, 0)
                # Appending the total cost of this offshoot route to the skipToEndRoutesCost list
                skipToEndRoutesCost.append(skipToEndCost)
                # Creating the offshoot route list if the user were to go directly to the end.
                skipToEndRoute = route + [i]
                # Appending the offshoot route to the list of offshoot skip to end routes
                skipToEndRoutesList.append(skipToEndRoute)                
            
            # If the connection being evaluated is cheaper than the current cheapest connection, it surpasses it and becomes the new best option to beat.                
            if dcDistance < shortestLeg:  
                current = i            
                shortestLeg = dcDistance
                
                # print(f'Node {startingPoint} to node {current} seems to be best path forward')                
        
        # If statement to detect when the algorithm recommends that the user leave the current city and go to another stop.
        if startingPoint.getName() != current:
            # Appending the next stop in the route to the route list.
            route.append(current)
            # Incrementing the total cost by the cost of this individual connection.
            total += shortestLeg
            print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
            print(f'{startingPoint} -----> {current}........Leg Distance: {shortestLeg}.....Cumulative route cost: {total}')
            print(f'Route thus far is: {route}')
            print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n')
            # time.sleep(2)
        
        # Else statement to back track in the event that the algorithm gets stuck in a city because it is prevented from traveling to a city it has already been to and all possible connections it has have already been visited.
        else:
            print(f'\n||||||||||||||||||||||stuck in {current}|||||||||||||||||||||||||||\n')
            print(f'Removing {route[-1]} from recommended route')
            eliminatedCity = current
            # removing the current city from the route list since visiting it results in getting stuck.
            route.pop()     
            # reverting to the city that the user was in before going to the city the algorithm got stuck in.
            current = route[-1]
            print(f'Reverting to {current} with {eliminatedCity} no longer an available option\n')            
            # time.sleep(2)
    
    # Rounding the total cost
    total = round(total, 0)
    
    # Obtaining the minimum cost of the offshoot routes
    minSkipRouteCost = min(skipToEndRoutesCost)  
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    print(skipToEndRoutesCost)
    print(skipToEndRoutesList)
    print(f'Min skip route cost = {minSkipRouteCost}')
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    
    # checking whether the best offshoot route is better than the Djikstra's Algorithm route.
    if minSkipRouteCost < total:
        print('\nBetter route available by skipping to end')
        # overwriting the route list and the total cost with the best offshoot option.
        route = skipToEndRoutesList[skipToEndRoutesCost.index(minSkipRouteCost)]
        total = minSkipRouteCost       
    
    print('\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!') 
    print(f'You have arrived at your destination.  Total distance traveled: {total}\n')

    return total, route


def optRoute(coordsDF, dcMatrix, current, destination):
    """
    This function calls the minPath function and passes a direct connections dataframe, origin city, and destination city to it.  It evaluates the optimal route in the forward (origin to destination) and reverse (destination to origin) directions.  It compares these 2 options and returns data for the  lowest travel cost option.
    :param p1: coordsDF.
    :type p1: dataframe.
    :param p2: dcMatrix.
    :type p2: dataframe.
    :param p3: current city.
    :type p3: string.
    :param p4: destination city.
    :type p4: string.
    :return: tuple of total cost and route as a list.
    """
    # checking cost of route in the forward direction (i.e., origin to destination)
    totalDistF, routeF = minPath(coordsDF, dcMatrix, current, destination)
    # checking cost of route in the backwards direction (i.e., destination to origin)
    totalDistR, routeR = minPath(coordsDF, dcMatrix, destination, current)
    # reversing list of cities encountered along route for backwards trip
    routeR.reverse()

    # if/else statements to return the lowest cost route since Djikstra's algorith can potentially miss better routes by blindly choosing the lowest cost option at each turn.
    if totalDistF < totalDistR:
        return totalDistF, routeF

    else:
        return totalDistR, routeR


def weatherSensitivity():
    """
    This function prompts the users to provide an input from 1 to 5 corresponding to their willingness to drive through bad weather.  The lower the number, the less willing.
    :return: integer of weather sensitivity
    """
    # setting lower and upper bounds of weather scale and then generating a range of integers between those bounds
    scaleMin = 1
    scaleMax = 5
    scale = range(scaleMin, scaleMax + 1)

    # Prompting the user to provide a willingness value corresponding to how willing they are to driving in bad weather.
    weatherSensitivity = int(input(f'On a scale of {scaleMin} to {scaleMax}, how willing are you to drive in bad weather?\n{scaleMin} is least willing and {scaleMax} is most willing.\nSelection: '))

    # checking to make sure that the willingness score in the allowable range of values.
    while weatherSensitivity not in scale:
        print(f'{weatherSensitivity} is not a valid selection.  Please try again')
        weatherSensitivity = int(input(
            f'On a scale of {scaleMin} to {scaleMax}, how willing are you to drive in bad weather?\n{scaleMin} is least willing and {scaleMax} is most willing.\nSelection: '))

    return weatherSensitivity


def routeWeather(sliderValue):
    """
    This function takes in the user's slider value for willingness to drive through bad weather.  Then it randomly generates a number corresponding to weather severity.  The slider value and the weather severity are used in a mathematical function to calculate the weather penalty factor of a given route.
    :param p1: sliderValue.
    :type p1: integer (1-5).
    :return: float of weather penalty factor.
    """
    # initializing lower and upper bounds of weather event severity
    scaleMin = 1
    scaleMax = 5

    # calculating the number of increments between the upper and lower bounds
    increments = (scaleMax + 1) - scaleMin
    # randomly generating the severity of weather in the range of the lower and upper bounds inclusively.
    forecast = random.randrange(1, increments + 1)

    # list comprehension to create list of coefficient starting from the min and increasing by the step size for the number of increments
    minCoeff = 1.25
    stepSize = 0.05
    coeff = [minCoeff + (stepSize * x) for x in range(increments)]
    # reversing list since 1 corresponds to least willing to drive in bad weather and thus requiring the largest coefficient
    coeff.reverse()
    # mathematical function to calculate the weather penalty.  It is exponential in nature to increasingly penalize weather as it gets worse.  Designed to never go below 1 since this will eventually be multiplied by the routes distance.  Always produces 1, regardless of user's willingness to drive in bad weather if the randomly generated weather is lowest value (1) since that corresponds to perfect weather.
    weatherPenalty = (1 / coeff[sliderValue - 1]) * (coeff[sliderValue - 1] ** forecast)

    return weatherPenalty


def weatherMatrix(dcDict, sliderValue):
    """
    This function takes in a dictionary of direct connection data and the user's slider value for willingness to drive through bad weather.  Then it calculates the weather penalty factor for each direct connection route and updates the dataframe to store the value for each direct connection.
    :param p1: dcDict.
    :type p1: dictionary.
    :param p2: sliderValue.
    :type p2: integer (1-5).
    :return: dataframe of weather penalty factors.
    """
    # calling function to create dataframe of direct connections using direct connections dataframe
    weatherMatrix = fillDCMatrix(dcDict)

    # nested for loop to replace distance values with randomly generated weather penalty for each route.
    for i in range(len(weatherMatrix.columns)):
        for j in range(len(weatherMatrix.index)):

            # Only selecting one have of the matrix since it will eventually be mirrored across the diagonal.  This must be done to prevent the weather penalty from A to B being randomly generated to be different from that of B to A.
            if i >= j:
                distance = weatherMatrix.at[weatherMatrix.index[j], weatherMatrix.columns[i]]
                severity = routeWeather(sliderValue)

                if pd.isna(distance):
                    continue

                weatherMatrix.at[weatherMatrix.index[j], weatherMatrix.columns[i]] = severity
                weatherMatrix.at[weatherMatrix.index[i], weatherMatrix.columns[j]] = severity

    return weatherMatrix


def totalRouteCost(distanceMatrix, weatherPenaltyMatrix):
    """
    This function takes in a direct connections distance dataframe and direct connections weather penalty dataframe. Then it outputs a total route cost dataframe that stores the cost of each individual direct connection.
    :param p1: distanceMatrix.
    :type p1: dataframe.
    :param p2: weatherPenaltyMatrix.
    :type p2: dataframe.
    :return: dataframe of direct connection costs.
    """
    # Checking to make sure that the cities along the header and indices is the same for both the weather and the distance matrix
    if distanceMatrix.columns.tolist() != weatherPenaltyMatrix.columns.tolist() and distanceMatrix.index.tolist() != weatherPenaltyMatrix.index.tolist():
        print('distance matrix is incompatible with weather matrix')
        sys.exit(-1)

    # Storing headers
    cols = distanceMatrix.columns
    # Storing indices
    rows = distanceMatrix.index
    # Creating copy of distanceMatrix to overwrite with total costs
    routeCostMatrix = distanceMatrix

    # Nested for loops to replace value in dataframe with the route cost (distance * weather penalty)
    for i in range(len(cols)):
        for j in range(len(rows)):
            distance = distanceMatrix.at[distanceMatrix.index[j], distanceMatrix.columns[i]]
            if pd.isna(distance):
                continue

            penalty = weatherPenaltyMatrix.at[weatherPenaltyMatrix.index[j], weatherPenaltyMatrix.columns[i]]
            routeCost = distance * penalty
            routeCostMatrix.at[routeCostMatrix.index[j], routeCostMatrix.columns[i]] = routeCost

    return routeCostMatrix

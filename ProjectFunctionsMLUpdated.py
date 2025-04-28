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

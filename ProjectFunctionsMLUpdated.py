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

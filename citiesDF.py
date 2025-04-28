import pandas as pd
import numpy as np

# City list for row index
cities = np.array(["Seattle", "Portland", "Oakland", "Los Angeles", "Helena", "Boise",
          "Salt Lake City", "Las Vegas", "Santa Fe", "Colorado Springs"])

# Creating DataFrame
cityInfoDF = pd.DataFrame(index = cities)
cityInfoDF["State"] = ["Washington", "Oregon", "California", "California", "Montana", "Idaho", "Utah", "Nevada", "New Mexico", "Colorado"]
cityInfoDF['X Coordinate'] = [185, 101, 95, 212, 468, 279, 341, 241, 524, 539]
cityInfoDF['Y Coordinate'] = [95, 181, 435, 621, 176, 279, 431, 564, 595, 486]

# Cities connecting via one interstate and their distance in miles
connections = {"Seattle" : {"Portland" : 175, "Boise" : 494, "Helena" : 588},
               "Portland" : {"Seattle" : 175, "Boise" : 430, "Oakland" : 629},
               "Oakland" : {"Portland" : 629, "Salt Lake City" : 730, "Los Angeles" : 371},
               "Los Angeles": {"Oakland" : 371, "Las Vegas" : 270, "Santa Fe" : 848},
               "Helena" : {"Seattle" : 588, "Salt Lake City" : 484, "Colorado Springs" : 860},
               "Boise" : {"Portland" : 430, "Seattle" : 494, "Salt Lake City" : 339},
               "Salt Lake City" : {"Boise" : 339, "Helena" : 484, "Colorado Springs" : 589, "Las Vegas" : 421, "Oakland" : 730},
               "Las Vegas" : {"Los Angeles" : 270, "Salt Lake City" : 421},
               "Santa Fe" : {"Los Angeles" : 848, "Colorado Springs" : 323},
               "Colorado Springs" : {"Santa Fe" : 323, "Salt Lake City" : 589, "Helena" : 860}}

cityInfoDF["Connections"] = [value for value in connections.values()]


print(cityInfoDF)


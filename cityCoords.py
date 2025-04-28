import math

class cityCoords:
    
    def __init__(self, cityName, lat, long):
        self.__cityName = cityName
        self.__lat = lat
        self.__long = long
        
    def getName(self):
        return self.__cityName
    
    def setName(self, cityName):
        self.__cityName = cityName
        
    def getLat(self):
        return self.__lat
    
    def setLat(self, lat):
        self.__lat = lat
        
    def getLong(self):
        return self.__long
    
    def setLong(self, long):
        self.__long = long
        
    def latRad(self):
        latRad = math.radians(self.getLat())
        return latRad
    
    def longRad(self):
        longRad = math.radians(self.getLong())
        return longRad
        
 #--------------------------------------------------------------------------

# cityName = 'Boise'
# lat = 95.1234
# long = 45.5678

# asdf = cityCoords(cityName, lat, long)

# print(asdf.getName())
# print(asdf.getLat())
# print(asdf.getLong())
# print(asdf.longRad())

       
    
    
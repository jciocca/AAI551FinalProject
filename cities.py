import tkinter as tk
#Author: Shasha Alvares
#Date: 4/2/2025
#Description: This function contains the city coordinates on the static map image used in our GUI so that the city
#             buttons can be created in the correct locations on the GUI.

#coordinate locations on map to place city labels.
cities = {
    "Seattle": (144, 72),
    "Portland": (54, 183),
    "Oakland": (35, 466),
    "Los Angeles": (94,660),
    "Helena": (347, 200),
    "Boise": (279, 279),
    "Salt Lake City": (341, 431),
    "Las Vegas": (226, 576), #217, 607
    "Santa Fe": (464, 639),
    "Colorado Springs": (524, 533),
}

# iterates through the dictionary creating buttons for each city name at the map coordinates specified
def create_cities(frame, city_clicked):
    for city_name, coordinates in cities.items():
        x, y = coordinates
        #the command = lambda makes sure every time city_clicked(name) is called, the name value
        #is the current city name from when the button was clicked. Otherwise the output would be the last city
        #from the loop
        button = tk.Button(frame, text=city_name, command=lambda name=city_name: city_clicked(name))
        button.place(x=x, y=y)


""" Tried to make a class but it broke the code too much 
import tkinter as tk

class CityManager:
    def __init__(self):
        # coordinate locations on map to place city labels
        self.cities = {
            "Seattle": (144, 72),
            "Portland": (54, 183),
            "Oakland": (35, 466),
            "Los Angeles": (94, 660),
            "Helena": (347, 200),
            "Boise": (279, 279),
            "Salt Lake City": (341, 431),
            "Las Vegas": (226, 576),
            "Santa Fe": (464, 639),
            "Colorado Springs": (524, 533),
        }

    def create_city_buttons(self, frame, city_clicked_function):
        for city_name, coordinates in self.cities.items():
            x, y = coordinates
            button = tk.Button(frame, text=city_name, command=lambda name=city_name: city_clicked_function(name))
            button.place(x=x, y=y)
"""


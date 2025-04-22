import tkinter as tk
#Author: Shasha Alvares
#Date: 4/2/2025
#Description: This function contains the city coordinates on the static map image used in our GUI so that the city
#             buttons can be created in the correct locations on the GUI.

#coordinate locations on map to place city labels.
cities = {
    "Seattle": (185, 95),
    "Portland": (101, 181),
    "Oakland": (95, 435),
    "Los Angeles": (212, 621),
    "Helena": (468, 176),
    "Boise": (279, 279),
    "Salt Lake City": (341, 431),
    "Las Vegas": (241, 564),
    "Santa Fe": (524, 595),
    "Colorado Springs": (539, 486),
}

# iterates through the dictionary creating buttons for each city name at the map coordinates specified
def create_cities(frame, city_clicked):
    for city_name, coordinates in cities.items():
        x, y = coordinates
        """ the command = lambda makes sure every time city_clicked(name) is called, the name value 
        is the current city name from when the button was clicked. Otherwise the output would be the last city
        from the loop"""
        button = tk.Button(frame, text=city_name, command=lambda name=city_name: city_clicked(name))
        button.place(x=x, y=y)

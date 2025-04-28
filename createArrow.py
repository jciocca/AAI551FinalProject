""" NOT USEING THIS TOP FILE
# createArrow.py
import math
from PIL import Image, ImageTk
import cities  # assumes you have a cities.cities dictionary

class ArrowDrawer:
    def __init__(self, canvas, arrow_path="arrow_red.png", size=(40, 20)):
        self.canvas = canvas
        self.arrow_img = Image.open(arrow_path).resize(size).convert("RGBA")
        self.image_refs = []  # to store PhotoImage objects to prevent garbage collection

    def draw_arrow(self, from_city, to_city):
        x1, y1 = cities.cities[from_city]
        x2, y2 = cities.cities[to_city]

        # Compute midpoint on the map and angle of the arrow
        mid_x = (x1 + x2) // 2
        mid_y = (y1 + y2) // 2
        dx = x2 - x1
        dy = y2 - y1
        angle = math.degrees(math.atan2(dy, dx))

        # Rotate and draw
        rotated = self.arrow_img.rotate(-angle, resample=Image.BICUBIC, expand=True)
        arrow_photo = ImageTk.PhotoImage(rotated)
        self.canvas.create_image(mid_x, mid_y, image=arrow_photo)
        self.image_refs.append(arrow_photo)  # Save reference to prevent garbage collection

    def clear_arrows(self):
        # Optionally clears and redraws the canvas map image if needed
        self.canvas.delete("all") """

""" WORKS BUT ONLY FOR ARROWS NO WEATHER
import math
from PIL import Image, ImageTk
import cities  # this accesses the city map coordinates stored in the dictionary

class ArrowDrawer:
    def __init__(self, canvas):
        self.canvas = canvas

    def draw_arrow(self, from_city, to_city, arrow_img):
        x1, y1 = cities.cities[from_city]
        x2, y2 = cities.cities[to_city]

        mid_x = (x1 + x2) // 2
        mid_y = (y1 + y2) // 2

        # Calculate angle between the two points
        dx = x2 - x1
        dy = y2 - y1
        angle = math.degrees(math.atan2(dy, dx))

        # Rotate with transparency preserved
        rotated_arrow = arrow_img.rotate(-angle, resample=Image.BICUBIC, expand=True)
        transparent_arrow = ImageTk.PhotoImage(rotated_arrow)

        self.canvas.create_image(mid_x, mid_y, image=transparent_arrow)
        self.canvas.image_refs.append(transparent_arrow)  # save reference to prevent garbage collection
"""

import math
from PIL import Image, ImageTk
import cities  # access city coordinates

#arrow class will draw the arrow on the canvas which contains the map
class ArrowDrawer:
    def __init__(self, canvas):
        self.canvas = canvas

    def draw_arrow(self, from_city, to_city, arrow_img, weather_img):

        #coordinates of stop and end city to figure out where to place each arrow
        x1, y1 = cities.cities[from_city]
        x2, y2 = cities.cities[to_city]

        #calculate mid x,y coordinate so we can generate arrow there
        mid_x = (x1 + x2) // 2
        mid_y = (y1 + y2) // 2

        # Calculate angle to rotate arrow so it is facing the next city button
        dx = x2 - x1
        dy = y2 - y1
        angle = math.degrees(math.atan2(dy, dx))

        # Rotate arrow and make transparent
        rotated_arrow = arrow_img.rotate(-angle, resample=Image.BICUBIC, expand=True)
        transparent_arrow = ImageTk.PhotoImage(rotated_arrow)
        self.canvas.create_image(mid_x, mid_y, image=transparent_arrow)
        self.canvas.image_refs.append(transparent_arrow)

        # Add weather icon near the arrow in the same y coordinate but shifted to the right in the x coordinate
        transparent_weather = ImageTk.PhotoImage(weather_img)
        self.canvas.create_image(mid_x + 35, mid_y, image=transparent_weather)
        self.canvas.image_refs.append(transparent_weather)

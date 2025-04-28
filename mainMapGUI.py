import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk
import slider  #gives access to slider.py
import cities #gives access to cities.py which stores city coordinates on the map
import ProjectFunctionsMLUpdated as ml #gives access to ProjectFunctionsML.py
import citiesDF as ccd #gives access to pandas dataframe used to store cities and interstates
import createArrow
import random
import cityCoords as cc
import pandas as pd
import math

#Author: Shasha Alvares
#Date: 4/2/2025
#Description: This is the main function for our map GUI

# Unpickling city coordinates dataframe
westCoastDF = pd.read_pickle('westCoastCities.pkl')

""" ------------------------------- Create main GUI window and sub-windows ------------------------------------"""
#creates, names, and sizes window for the app. Currently resizing the app messes with the city labels
#which will need to be fixed in the future.
window = tk.Tk()
window.title("Breeze Route")
window.geometry("1000x800")
window.resizable(False, False) #Disable resizing for now bc then the map coordinates need to be change

# Create left frame that will display map image
left_frame = tk.Frame(window, width=800, height=800)  # Make the left frame bigger
left_frame.pack(side="left", fill="both", expand=True)

#Create right frame that will display user buttons/sliders
right_frame = tk.Frame(window, width=200, height=800)  # Make the right frame smaller
right_frame.pack(side="right", fill="y")

""" ------------------------------- Load Map to left frame -----------------------------------------"""
# Load and crop map image
image_path = "InterstateHwyMap.png"
image = Image.open(image_path)
crop_area = (0, 0, 750, 800)
image = image.crop(crop_area)
#image = image.resize((600, 795)) #if the image needs to be blown up we will use this
photo = ImageTk.PhotoImage(image)

#assigns map as left background on a canvas so the arrows can also be generated
canvas = tk.Canvas(left_frame, width=photo.width(), height=photo.height())
canvas.pack()
canvas.create_image(0, 0, anchor="nw", image=photo)

#opens arrow image and is supposed to convert it so background is clear, however it does not do that
arrow_img = Image.open("arrow_red.png").convert("RGBA").resize((40, 20))
canvas.image_refs = []  # to store arrow images and prevent GC
arrow_drawer = createArrow.ArrowDrawer(canvas)  # pass in the map canvas to the arrowdrawer

""" ------------------------------- City Object --------------------------------------------------"""
# display map coordinates in console when clicked - helpful for moving city name buttons
def print_mouse_coordinates(event):
    print(f"Clicked at: ({event.x}, {event.y})")
canvas.bind("<Button-1>", print_mouse_coordinates)

#print a city name when clicked - helpful to verify the button works
def city_clicked_for_coords(city_name):
    print(f"{city_name} clicked!")

"""
#Instruciotn above the city boxes that tell user the boxes will autofill when user clicks a city
autoFillBoxLabel = tk.Label(
        right_frame,
        text="The first city you click\n"
             "will autofill in the start box.\n"
             "The second city you click will\n"
             "autofill in the destination box.\n"
             "If you type the name, be sure to type "
             "it exactly as spelled.",
        wraplength=200,
        justify="left", #Text in label is left aligned
        anchor = "w" #Anchor the entire label to the left
    )
autoFillBoxLabel.place(relx=0.0, rely=0.075, anchor="w") """

titleLabel = tk.Label(
    right_frame,
    text="Route Selection",
    font=("Helvetica", 14, "bold"),
)
titleLabel.place(relx=0.0, rely=0.01, anchor="nw")

autoFillBoxLabel = tk.Label(
    right_frame,
    text="Click a city to autofill:\n"
         "• 1st click → Start\n"
         "• 2nd click → Destination\n"
         "Or type the names exactly as shown.",
    wraplength=200,
    justify="left",
    bg="#ebddc5"
)
autoFillBoxLabel.place(relx=0.0, rely=0.035, anchor="nw")

#variables to store which city was clicked
first_city_clicked = None
second_city_clicked = None

#function to store which city is clicked first and second.
#vars are global so they can be accessed outside the function
def city_clicked(city_name):
    global first_city_clicked, second_city_clicked

    if first_city_clicked is None:
        first_city_clicked = city_name #variable storing first city name so we can autofill it in the start entry box
        start_entry.delete(0, tk.END) #clear existing text
        start_entry.insert(0, first_city_clicked) #insert new text
    elif second_city_clicked is None:
        second_city_clicked = city_name #variable storing second city name so we can autofill it in the end entry box
        destination_entry.delete(0, tk.END) #clear existing text
        destination_entry.insert(0, second_city_clicked) #insert new text

    print(f"First city: {first_city_clicked}")
    print(f"Second city: {second_city_clicked}")

#Create city buttons from cities.py file
cities.create_cities(left_frame, city_clicked)

""" using city class"""
#city_manager.create_city_buttons(left_frame, city_clicked)

"""create autofill boxes start_entry and destination_entry in the right frame that user clicks are store in"""
start_label = tk.Label(right_frame, text="Start City:", font=("Helvetica", 14, "bold"))
start_label.place(relx=0.00, rely=0.15)

start_entry = tk.Entry(right_frame, width=20) #we can access the current start city name using star_entry.get()
start_entry.place(relx=0.00, rely=0.2)

destination_label = tk.Label(right_frame, text="Destination City:", font=("Helvetica", 14, "bold"))
destination_label.place(relx=0.00, rely=0.25)

destination_entry = tk.Entry(right_frame, width=20) #we can access the current end city name using destination_entry.get()
destination_entry.place(relx=0.00, rely=0.3)


""" ------------------------------- Slider Object --------------------------------------------------"""
# Add the slider into the right frame and save the object to my_slider variable
my_slider = slider.add_slider_to_window(right_frame)

#create label widget to show value
def confirm_slider_value():
    slider_value = my_slider.get()
    print(f"This current slider value is {slider_value}")  # prints value to console

    dcDict = ccd.connections  #allows access to the pandas dataframe in the citiesDF.py file that hold the dictionary
    current = start_entry.get() #stores first city user clicked on
    destination = destination_entry.get() #stores second city user clicked on
    
    # reset()
    #reset arrows
    canvas.delete("all")
    canvas.create_image(0, 0, anchor="nw", image=photo)
    canvas.image_refs.clear()
    
    """print statements are for debugging. Sometimes program gets stuck on optimal route search, 
    which Mike has created a temporary solution for, but we will need to fully fix this issue later"""
    print("Starting weather matrix...")
    weatherPenaltyMatrix = ml.weatherMatrix(dcDict, slider_value)
    print("Weather matrix done.")
    print("Starting distance matrix...")
    distanceMatrix = ml.fillDCMatrix(dcDict)
    print("Distance matrix done.")
    print("Starting total cost matrix...")
    costMatrix = ml.totalRouteCost(distanceMatrix, weatherPenaltyMatrix)
    print("Cost matrix done.")
    print("Starting optimal route search...")
    #bestRoute[0] is the cost and bestRoute[1] is the list of optimal cities
    bestRoute = ml.optRoute(westCoastDF, costMatrix, current, destination)
    print("Optimal route found.")

    #makes a comma separated string out of the list of optimal route cities that is returned
    #by the optRoute() function in ProjectFunctionsML.py
    optimalRouteString = " to ".join(bestRoute[1])

    """ output text updates to the empty label that was created every time the confirm button is 
    clicked and outputs the optimal route and inconvenience factor. """
    outputText.config(
        text=f"Your optimal route is from\n"
             f"{optimalRouteString}\n"
             f"Take note of the arrow\n"
             f"color showing the weather!"
    )

    """ OG working red arrow
    #draw arrow path
    for i in range(len(bestRoute[1]) - 1):
        arrow_drawer.draw_arrow(bestRoute[1][i], bestRoute[1][i + 1]) 
        """
    # # draw arrows based on route
    # for i in range(len(bestRoute[1]) - 1):
    #     from_city = bestRoute[1][i]
    #     to_city = bestRoute[1][i + 1]   
    
    # draw arrows based on route    
    scaleMin = 1
    scaleMax = 5     
    increments = (scaleMax + 1) - scaleMin
    minCoeff = 1.25
    stepSize = 0.05    
    coeffList = [minCoeff + (stepSize * x) for x in range(increments)]
    coeffList.reverse()   
    coeff = coeffList[slider_value - 1]
    
    for i in range(1, len(bestRoute[1])):
        from_city = bestRoute[1][i - 1]
        to_city = bestRoute[1][i]
        wp = weatherPenaltyMatrix.loc[from_city, to_city]
        weather_event = (math.log10(wp) / math.log10(coeff)) + 1
        weather_event = int(round(weather_event, 0))
        print(f'Forecast from {from_city} to {to_city} = {weather_event}')      

        # weather_event = random.randint(1, 5)

        # Pick the correct arrow and weather image based on weather
        if weather_event == 1:  # sunny
            arrow_path = "arrow_orange.png"
            weather_icon_path = "sun.png"
        elif weather_event == 2:  # light rain
            arrow_path = "arrow_green.png"
            weather_icon_path = "rain2.png"
        elif weather_event == 3:  # heavy rain
            arrow_path = "arrow_blue.png"
            weather_icon_path = "thunder.png"
        elif weather_event == 4:  # snow
            arrow_path = "arrow_purple.png"
            weather_icon_path = "snow.png"
        elif weather_event == 5:  # fire
            arrow_path = "arrow_red.png"
            weather_icon_path = "fire.png"
        else:
            arrow_path = "arrow_orange.png"  # fallback safety
            weather_icon_path = "sun.png"

        # Load both the arrow and weather images
        arrow_img = Image.open(arrow_path).convert("RGBA").resize((50,50))
        weather_img = Image.open(weather_icon_path).convert("RGBA").resize((40, 40))

        # Draw them both
        arrow_drawer.draw_arrow(from_city, to_city, arrow_img, weather_img)

""" Works for all colored arrows but no weather included
    # draw arrows based on route
    for i in range(len(bestRoute[1]) - 1):
        from_city = bestRoute[1][i]
        to_city = bestRoute[1][i + 1]

        # Simulate new weather severity for each leg (1 to 5)
        weather_event = random.randint(1, 5)

        # Pick the correct arrow color based on weather
        if weather_event == 1: #sunny weather
            arrow_path = "arrow_orange.png"
        elif weather_event == 2: #light rain
            arrow_path = "arrow_green.png"
        elif weather_event == 3: # heavy rain
            arrow_path = "arrow_blue.png"
        elif weather_event == 4: #snow
            arrow_path = "arrow_purple.png"
        elif weather_event == 5: #fire
            arrow_path = "arrow_red.png"
        else:
            arrow_path = "arrow_orange.png"  # fallback safety

        # Load the arrow and draw it
        arrow_img = Image.open(arrow_path).convert("RGBA").resize((40, 20))
        arrow_drawer.draw_arrow(from_city, to_city, arrow_img) 
        
        """


#create button to confirm slider choice and do actions in the function confirm_slider_value above
confirmSliderButton = (tk.Button
    (
    right_frame,
    text="Confirm Choice",
    command=confirm_slider_value)
)
confirmSliderButton.place(relx=0.3, rely=0.63, anchor="center")

""" ------------------------------- Run program -----------------------------------------------------"""
window.mainloop()

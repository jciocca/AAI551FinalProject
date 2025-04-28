import tkinter as tk
from tkinter import *

#Author: Shasha Alvares
#Date: 4/2/2025
"""
Description: This function/file creates the slider user in the GUI, as well as the text description above of 
what the slider values mean above it. 
"""
#later we can create a controlsFrame so physically updating all these related features
# on the GUI display will be easier

#function to create slider in the main file
def add_slider_to_window(window):
    #create slider widget. slider.get() has the value stored
    slider = Scale(window, from_=1, to=5, orient=HORIZONTAL)

    #specify the location in the frame that the slider will appear
    slider.place(relx=0.3, rely=0.59, anchor="center")  # relx=0.5 centers horizontally and rely 0.3 down vertically

    #create bold text labeling the
    titleLabel = tk.Label(
        window,
        text="Inconvenience Selection",
        font=("Helvetica", 14, "bold"),
    )
    titleLabel.place(relx=0.0, rely=0.37, anchor="w")
    #create a label above the slider to prompt user
    inconvenienceLabel = tk.Label(
        window,
        text="From 1-5, 1 being least\n"
             "inconvenienced and\n"
             "5 being most, how much\n"
             "traffic/bad weather\n"
             "would you be okay with\n"
             "for a faster route? "
             "Make sure to confirm after you also choose cities.",
        wraplength=200,
        justify="left", #Text in label is left aligned
        anchor = "w", #Anchor the entire label to the left
        bg = "#ebddc5"
    )
    #w for west so text is left aligned
    #relx 0 makes the text start at the left of the textbox
    inconvenienceLabel.place(relx=0.0, rely=0.48, anchor="w")

    return slider  # return the slider to use slider.get() later

# Imports
from collections import deque
from datetime import datetime
from faicons import icon_svg
from shiny import reactive, render
from shiny.express import ui
import pandas as pd
import random

# Define the page layout
ui.page_opts(title = 'Antarctic Temperature (F) and Timestamp', fillable=True)

# === Sidebar ==============================================================================
with ui.sidebar(title = 'Antarctic Temperature (F)', class_ = 'text-center', open='open'):

    # Add a description
    ui.p('Frequently "measuring" the farenheit temperature in Antarctica')

    # Include link to GitHub repo
    ui.a('GitHub Repository for Code', href='https://github.com/Stone-Snevets/cintel-05-cintel')


# === Main =================================================================================

with ui.layout_columns():
# (
    # --- Create a value box showing the current temperature -------------------------------
    
    with ui.value_box(value = 'Warmer than usual.', showcase = icon_svg('sun'), theme = 'bg-gradient-blue-green'):
    # (
        # Grab the current temp
        @render.text
        def get_current_temp():
        # (
            # Call "get_timestamp_and_temp" function
            now_dict, now_deque, now_df = get_timestamp_and_temp()

            # Grab and return the temp from the dictionary
            return now_dict['temp']            
        # )
    # )

    # --- Create a card holding the current timestamp --------------------------------------

    with ui.card(full_screen=True):
    # (
        # Add a header
        ui.h2('Current Date and Time:')

        # Grab the current timestamp
        @render.text
        def get_current_timestamp():
        # (
            # Call "get_timestamp_and_temp" function
            now_dict, now_deque, now_df = get_timestamp_and_temp()

            # Grab and return the timestamp from the dictionary
            return now_dict['timestamp']
        # )
    # )        
# )
# --- Generate reactive calc function ------------------------------------------------------

# Create constant for number of seconds
NUM_SECONDS:int = 1

# Create constant for number of elements our deque can hold
DEQUE_ELEMENTS:int = 5

# Generate our deque
time_temp_deque = reactive.value(deque(maxlen = DEQUE_ELEMENTS))

# Define the reactive.calc function
@reactive.calc()
def get_timestamp_and_temp():
# (
    # Invalidate the reactive calc to update every "NUM_SECONDS" seconds
    reactive.invalidate_later(NUM_SECONDS)

    # Retrieve the current timestamp
    #-> Format with strftime()
    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Generate a random temperature
    #-> Round the temperature to 2 decimal places
    current_temp_f = round(random.uniform(-18, -16), 2)

    # Create a dictionary of the latest timestamp and temperature
    current_dict = {'timestamp': current_timestamp, 'temp': current_temp_f}

    # Append the latest timestamp and temperature to our deque
    time_temp_deque.get().append(current_dict)

    # Grab the current deque
    current_deque = time_temp_deque.get()

    # Convert the currcnt deque to a dataframe
    current_df = pd.DataFrame(current_deque)

    # Return the dictionary, deque, and dataframe
    return current_dict, current_deque, current_df
# )

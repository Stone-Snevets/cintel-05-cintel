# Imports
from collections import deque
from datetime import datetime
from shiny import reactive, render
from shiny.express import ui
import random

# ----- Title ----------------------------------------------------------------------
ui.page_opts(title='Live Antarctic Temperatures', fillable=True)

# ----- Sidebar --------------------------------------------------------------------
with ui.sidebar(title='Antarctica Temperature',
                class_='text-center',
                open='open'):

    # Provide a description
    ui.p('Perodically measuring the farenheit temperature in Antarctica')

    # Provide a link to GitHub Repository
    ui.a('GitHub Repository of Code',
         href = 'https://github.com/Stone-Snevets/cintel-05-cintel',
        target = '_blank')


# ----- Main ----------------------------------------------------------------------
# Add title of the timestamp
ui.h2('Current Time:')

# Render the timestamp
@render.text
def display_timestamp():

    # Call 'create_timestamp_and_temp' function
    # Grab only the timestamp
    current_timestamp = create_timestamp_and_temp()['time']

    # Return the timestamp
    return current_timestamp

# Add title of the temperature
ui.h2('Current Temperature(F):')

# Render the temperature
@render.text
def display_temp():

    # Call 'create_timestamp_and_temp' function
    # Grab only the temperature
    current_temp_f = create_timestamp_and_temp()['temperature(F)']

    # Return the temperature
    return current_temp_f


# ----- Generate and store 'random' temperature intervals --------------------------
# Assign our time interval to a constant
INTERVAL_SEC:int = 1;

# Assign the number of bins we can hold
NUM_DEQUE_BINS = 5

# Create the deque
temperature_deque = reactive.value(deque(maxlen=NUM_DEQUE_BINS))

# Create a reactive calc function to create a temperature and timestamp
@reactive.calc()
def create_timestamp_and_temp():
    
    # Generate a interval every 'INTERVAL_SEC' seconds
    reactive.invalidate_later(INTERVAL_SEC)

    # Create a timestamp that changes every 'INTERVAL_SEC' seconds
    #-> Format the output with strftime()
    time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Randomly generate a temperature
    #-> Round it to 2 decimal places
    temperature_F = round(random.uniform(-18, -16),2)

    # Append the new timestamp and temperature into our deque
    temperature_deque.get().append({'time': time_stamp, 'temperature(F)': temperature_F})

    # Return the new timestamp and temperature
    return {'time': time_stamp, 'temperature(F)': temperature_F}

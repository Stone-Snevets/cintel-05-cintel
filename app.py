# Imports
from collections import deque
from datetime import datetime
from faicons import icon_svg
from scipy import stats
from shiny import reactive, render
from shiny.express import ui
from shinywidgets import render_plotly
import pandas as pd
import plotly.express as px
import random

# Define the page layout
ui.page_opts(title = 'Antarctic Temperature and Timestamp', fillable=True)

# === Sidebar ==============================================================================
with ui.sidebar(title = 'Antarctic Temperature', class_ = 'text-center', open='open'):

    # Add a description
    ui.p('Frequently "measuring" the temperature in Antarctica')

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
        def get_current_temp_c():
        # (
            # Call "get_timestamp_and_temp" function
            now_dict, now_deque, now_df = get_timestamp_and_temp()

            # Grab the temperature from the dictionary
            now_temp_c = now_dict['temp']

            # Convert Celsius to Fahrenheit
            #-> Round to 2 decimal places
            now_temp_f = round(((9/5)*now_temp_c)+32, 2)

            # Return both temperatures
            return f"{now_temp_c} C <-> {now_temp_f} F"
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

    # --- Create a card holding the latest elements of the deque ---------------------------
    with ui.card(full_screen=True):
    # (
        # Create a dategrid of latest deque elements
        @render.data_frame
        def deque_data_grid():
        # (
            # Call "get_timestamp_and_temp" function
            now_dict, now_deque, now_df = get_timestamp_and_temp()

            # Grab and return a datagrid of the dataframe
            return render.DataGrid(now_df, width='100%')
        # )
    # )

    # --- Create a card with a plot of the elements ----------------------------------------
    with ui.card(full_screen=True):
    # (
        # Draw a plot of the elements
        @render_plotly
        def draw_timestamp_and_temp():
        # (
            # Call "get_timestamp_and_temp" function
            now_dict, now_deque, now_df = get_timestamp_and_temp()

            # Make sure "now_df" is not empty
            if not now_df.empty:
            # (
                # Convert "timestamp" to a dataframe timestamp
                #-> this is for cleaner graphing
                now_df['timestamp'] = pd.to_datetime(now_df['timestamp'])
                
                # Graph a scatterplot of our findings
                graph_timestamp_and_temp = px.scatter(now_df,
                                                      x = 'timestamp',
                                                      y = 'temp',
                                                      title = 'Measured Temperature (F) in Antarctica',
                                                      labels = {'temp':'Temperature (F)', 'timestamp': 'Date and Time'},
                                                      color_discrete_sequence = ['blue'])

                # Add a Regression Line
                #-> Set the x values to be a sequence list
                reg_x = list(range(len(now_df)))

                #-> Set the y values to the temperatures
                reg_y = now_df['temp']

                #-> Call stats.linregress() to obtain the regression
                slope, intercept, r_value, p_value, std_err = stats.linregress(reg_x, reg_y)

                #-> Calculate the slope of the line-best-fit
                now_df['best_fit_line'] = [((slope*x) + intercept) for x in reg_x]

                #-> Add regression line to our scatterplot
                graph_timestamp_and_temp.add_scatter(x = now_df['timestamp'],
                                                     y = now_df['best_fit_line'],
                                                     mode = 'lines',
                                                     name = 'Regression Line')

                # Return our plot
                return graph_timestamp_and_temp
            # )
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
    current_temp_c = round(random.uniform(-18, -16), 2)

    # Create a dictionary of the latest timestamp and temperature
    current_dict = {'timestamp': current_timestamp, 'temp': current_temp_c}

    # Append the latest timestamp and temperature to our deque
    time_temp_deque.get().append(current_dict)

    # Grab the current deque
    current_deque = time_temp_deque.get()

    # Convert the currcnt deque to a dataframe
    current_df = pd.DataFrame(current_deque)

    # Return the dictionary, deque, and dataframe
    return current_dict, current_deque, current_df
# )

# cintel-05-cintel
Begin working with live data

### NOTE
app.py was created in the Shiny live platform.  All libraries listed in requirements.txt are already in Shiny.
So if you are running app.py in shiny, you don't need to include anything in requirements.txt

### Create "live" data to work with
* Use a reactive calculation to simulate periodic temperature readings in Antarctica.
* Create a timestamp to associate with each temperature reading

### Develop a Deque
* A deque stores only the past N inputs which makes working with live data more efficient
* This program uses a deque to store the past N timestamps and temperatures

### Display Temperature and Timestamp
* Use a value box to display the temperature readings next to a sun icon
* Use a card to display the current timestamp

### Plot Temperature and Timestamp
* Create a scatterplot of the temperature(y) and timestamp(x)
* Generate a regression line of the past N inputs in our deque

# tims-picker
About this program:

This program provides a variety of functions that together provide a way to reliably pick winning hockey challenge picks for Tim Hortons Hockey Pick Challenge. Note that as this program does not enter the picks for you, it is not against Tim Hortons TOS. The three functions and their uses are described below.


Function 1 (Make a guess using a predefined formula):

This function takes a formula I created after testing many, and automatically pulls data from the NHL api to compare the stats of each possible pick, before returning the best players. Additionally, it checks all rounds (new players become available at different times throughout the day), and compares each group to find the best overall time of pick. At the time of writing this, the pick percentage of this program is 34%, while the best percentage globally on the leaderboard is 33%.


Function 2 (Make a guess using an AI formulated calculation):

This function makes use of Python's Tensorflow library to use a machine learning method to make the pick. It does this by looking at years of data of each possible pick per day, and who scored versus who didn't. Using this data, the program makes a linear estimator, and then runs the possible picks of the day through this estimator. This returns a possibility of each player scoring, and takes the highest probability as the best possible pick from each group for the day. These names are then outputted for the user to easily see and make note of. Currently, this method has an average of 39%, however more testing is needed to verify if this is a consistent average.


Function 3 (Add more data to the csv data files):

In order to continually update the accuracy of the machine learning AI, it is important to provide it with new, up-to-date information. This function allows the user to add data to the csv files, by adding days of stats from to either the back or the start of the file. It automatically stops when reaching yesterday, as filling out today's data can be detrimental as it provides false scoring records. Note that this data can only go back so far, as tims picks is a relatively new challenge.


Running this program:

First install all packages within requirements.txt, and then simply run main.py and follow the terminal instructions.
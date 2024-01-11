# Tims-Picker
## About this Program

This program offers a set of functions that provide a reliable method for selecting winning picks for the Tim Hortons Hockey Pick Challenge. As this program only suggests picks and does not enter them, it does not violate Tim Hortons' Terms of Service. The program includes three main functions, described below.

## Function 1: Make a Guess Using a Predefined Formula

This function uses a formula created through extensive testing. It automatically pulls data from the NHL API to compare the stats of each possible pick, then returns the best players. As of the time of writing, this program's correct pick percentage is 34%, while the highest percentage on the global leaderboard is 33%.

## Function 2: Make a Guess Using an AI Formulated Calculation

This function utilizes Python's TensorFlow library to employ a machine learning method for making picks. It analyzes years of data for each possible pick per day, determining who scored versus who didn't. The program creates a linear estimator using this data, then runs the possible picks of the day through this estimator. This process yields a scoring probability for each player, and the program selects the players with the highest probabilities as the best possible picks. These names are then output for the user's convenience. Currently, this method has an average success rate of 39%, but more testing is needed to verify if this is a consistent average.

## Function 3: Add More Data to the CSV Data Files

To continually improve the accuracy of the machine learning AI, it's important to feed it new, up-to-date information. This function allows the user to add data to the CSV files, appending days of stats to either the end or the beginning of the file. The function automatically stops when it reaches yesterday's data, as including today's data can be detrimental by providing false scoring records. Please note that this data can only go back so far, as the Tim Hortons Hockey Pick Challenge is a relatively new event.

**Note:** The source of the possible player picks has been discontinued. At the time of writing, there are no additions to be appended to the CSV file.

## Running this Program

First install all packages within requirements.txt:
```pip install -r requirements.txt```
Start the main script:
```python src/main.py```

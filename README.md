# Tims-Picker
## About this Program

UPDATE : As of Feb. 2, 2024, this program has been reworked to rank all players playing today. This is because it is no longer possible to access Tim Horton's possible player picks, instead the user must now look through the sorted list and compare with possible Tim's picks. 

This program offers a set of functions that provide a reliable method for selecting winning picks for the Tim Hortons Hockey Pick Challenge. As this program only suggests picks and does not enter them, it does not violate Tim Hortons' Terms of Service. The program includes three main functions, described below.

## Function 1: Create Rankings Using a Predefined Formula

This function uses a formula created through extensive testing. It pulls data from the NHL API to create probabilities for each possible player, and then outputs the players in order of most likely to score.

## Function 2: Make a Guess Using an AI Formulated Calculation

This function utilizes Python's TensorFlow library to employ a machine learning method for making picks. It analyzes years of data for each possible pick per day, determining who scored versus who didn't. The program creates a linear estimator using this data, then runs the possible picks of the day through this estimator. This process yields a scoring probability for each player, and the program orders the players with the highest probabilities as the best possible picks. These names are then outputed for the user's convenience.

## Running this Program

First install all packages within requirements.txt:<br/>
```pip install -r requirements.txt```<br/><br/>
Start the main script:<br/>
```python src/main.py```

## Images
Predefined Formula:        |  Linear Estimator
:-------------------------:|:-------------------------:
![image](https://github.com/proby-8/tims-picker/assets/109328434/7d7d8ace-0a5d-4f16-887b-9086ea36baea)  |  ![image](https://github.com/proby-8/tims-picker/assets/109328434/7064cf24-dc40-4979-a3cb-09f935f36d25)




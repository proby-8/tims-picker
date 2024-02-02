from formulaGuess import makeGuess
from empiricalTesting import runTest
from aiMain import aiGuess

if __name__ == "__main__":
    print("\nPlease select a function:")
    print("1: Make a guess using a predefined formula")
    print("2: Make a guess using an AI formulated calculation")
    print("3: Update the csv data files")
    print("4: Test formulas")
    print("5: Rank all players playing today")
    choice = int(input("Choice: "))

    if (choice == 1):
        # predefined formula
        print("Loading data...")
        makeGuess()
    elif (choice == 2):
        # AI formula
        print("Having the AI run estimates...")
    elif (choice == 3):
        # csv
        print("Taking you to update the csv data...")
    elif (choice == 4):
        print("Time to do some empirical testing...")
        runTest()
    elif (choice == 5): 
        print("Loading data...")
        allPlayers()
    else:
        print("Invalid input")
        exit(1)
            
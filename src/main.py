from formulaGuess import makeGuess
from empiricalTesting import runTest
from aiMain import aiGuess

if __name__ == "__main__":
    repeat = True
    while (repeat):
        repeat = False
        print("\nPlease select a function:")
        print("1: Make a guess using a predefined formula")
        print("2: Make a guess using an AI formulated calculation")
        print("3: Update the csv data files")
        print("4: Test formulas")
        choice = input("Choice: ")
        if (choice.isnumeric()):
            choice = int(choice)

        if (choice == 1):
            # predefined formula
            print("Loading data...")
            makeGuess()
        elif (choice == 2):
            # AI formula
            print("Having the AI run estimates...")
            aiGuess()
        elif (choice == 3):
            # csv
            print("Taking you to update the csv data...")
        elif (choice == 4):
            print("Time to do some empirical testing...")
            runTest()
        else:
            print("Invalid input")
            repeat = True
            
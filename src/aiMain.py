from linearRegression import test2

# stats
# - goals per game
# - other teams goals against
# - minutes played
# - possible stuff
#   - powerplay minutes
#   - (could look at other teams penalty minutes)


def aiGuess():
    numEpoch = int(input("Please enter the number of epochs you would like to use: "))
    totalCorrect = 0
    totalCorrect += test2(1, numEpoch)
    totalCorrect += test2(2, numEpoch)
    totalCorrect += test2(3, numEpoch)


    print(f"Total correct: {totalCorrect}")
    # 33 dates in test data currently
    print(f"Final pick rate: {totalCorrect / (33*3)}")

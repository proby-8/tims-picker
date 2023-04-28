import time
from datetime import datetime
import scrapingFunctions
import os
import guessMaker
import aiPrediction


path = "lib\\"
try:
    os.mkdir(path)
except:
    pass

print("\nPlease select a function:")
print("1: Make a guess using a predefined formula")
print("2: Make a guess using an AI formulated calculation")
print("3: Add more data to the csv data files")
choice = int(input())

start_time = time.time()
if (choice == 1):
    guessMaker.main()
elif(choice == 2):
    df = []
    name = []
    for i in range (0, 3):
        df.append(scrapingFunctions.getStatsTemp(i+1))
        index = aiPrediction.main(df[i], 1)
        name.append(df[i].loc[index]['Name'])
    print("\n")
    for i in range (1,4):
        print(f"Pick from group {i}: {name[i-1]}")

elif (choice == 3):
    daysGoingUp=True
    print("Would you like to add recent games, or continue adding old games (o/n)? ", end="")
    if (input() == 'o'):
        daysGoingUp = False

    print("How many days would you like to add? ", end="")
    daysToLookAt = input()

    try:
        if (daysGoingUp):
            inputFile = (path + 'train_test1.csv')
            f1 = open(inputFile, "r")
            first_line = f1.readlines()[1]
            f1.close()
            date = first_line[:10]
            date = scrapingFunctions.addDays(date)
        else:
            inputFile = (path + 'train_test1.csv')
            f1 = open(inputFile, "r")
            last_line = f1.readlines()[-1]
            f1.close()
            date = last_line[:10]
            date = scrapingFunctions.subtractDays(date)
    except:
        # file DNE
        date = datetime.today().strftime('%Y-%m-%d')
        if (daysGoingUp == False):
            date = scrapingFunctions.subtractDays(date)

    print(f"Beginning at {date}")
    start_time = time.time()

    # path is path to file location
    # date is date to start at
    scrapingFunctions.getStats(path, date, daysToLookAt, daysGoingUp)

scrapingFunctions.printTime(time.time() - start_time)
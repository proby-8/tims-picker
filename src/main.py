if __name__ == "__main__":
    print("Please select a function:")
    print("1: Rank all players playing today based off of a predefined formula")
    print("2: Make a guess using an AI formulated calculation")
    print("3: Get betting odds from DraftKings")
    print("4: Save today's data")
    choice = int(input("Choice: "))
    print("")

    if (choice == 1):
        # rank all players today
        print("Loading data...\n")
        from allPlayers import rank
        rank()
    elif (choice == 2):
        # AI formula
        print("Having the AI run estimates...\n")
        from aiMain import aiGuess
        aiGuess()
    elif (choice == 3):
        # odds scraper
        print("Gathering odds...")
        from oddsScraper import main
        main()
    elif (choice == 4):
        # saving data
        print("Loading player data...")
        from saveData import main
        main()
    else:
        print("Invalid input")
        exit(1)
            
if __name__ == "__main__":
    print("Please select a function:")
    print("1: Rank all players playing today based off of a predefined formula")
    print("2: Make a guess using an AI formulated calculation")
    print("3: Save today's data - Depreciated, use daily run instead.")
    print("4: Empirical Testing")
    print("5: Daily run (saves data and updates api)")
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
        print("Running daily upkeep...")
        from api import main
        main()
    elif (choice == 4):
        print("Running empirical calculations...")
        from empCalc import main
        main()
    elif (choice == 5):
        print("Running daily upkeep...")
        from api import main
        main()
    else:
        print("Invalid input")
        exit(1)
            
            
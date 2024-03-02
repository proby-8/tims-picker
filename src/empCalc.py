import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def main():
    print("Please select a function:")
    print("1: Find best weight combination based on historical data.")
    print("2: Find best threshold based on weight.")
    print("3: Find weights without combining penalty minutes and powerplay goals.")
    print("4: Test current weight.")
    choice = int(input("Choice: "))
    print("")

    if (choice == 1):
        empiricalTest()
    elif (choice == 2):
        thresholdTest()
    elif (choice == 3):
        forPMandPPG()
    elif (choice == 4):
        testCurWeight()
    

def calculateStat(row, weights):
    
    # Incorporate the relationship between OTPM and PPG
    ratio = 0.18  # from empirical testing
    composite_feature = ratio * row['OTPM'] + (1 - ratio) * row['PPG']

    # Replace OTPM and PPG with the composite feature in the row
    row_without_otpm_ppg = row.drop(['OTPM', 'PPG'])
    row_with_composite = row_without_otpm_ppg._append(pd.Series([composite_feature], index=['Composite_OTPM_PPG']))

    if len(weights) != len(row_with_composite):
        raise ValueError("Number of weights must match the number of features.")
    
    if round(sum(weights), 2) != 1:
        print(sum(weights))
        raise ValueError("Weights must add up to 1.")

    # Calculate the overallStat using the modified row
    overallStat = 0
    for w, stat in zip(weights, row_with_composite):
        result = w * stat
        overallStat += result

    return overallStat


def calculateStatNoComp(row, weights):
    
    if len(weights) != len(row):
        raise ValueError("Number of weights must match the number of features.")
    
    if round(sum(weights), 2) != 1:
        print(sum(weights))
        raise ValueError("Weights must add up to 1.")

    # Calculate the overallStat using the modified row
    overallStat = sum(w * stat for w, stat in zip(weights, row))
    return overallStat


def test():
    # Load the data
    try:
        data = pd.read_csv('lib/data.csv')
    except UnicodeDecodeError:
        print("Manually save the csv file and try again.\n")
        exit(1)


    # Drop the rows where 'Scored' is empty
    data = data[data['Scored'] != ' ']

    features = data[['GPG', 'Last 5 GPG', 'HGPG', 'PPG', 'OTPM', 'TGPG', 'OTGA', 'Home (1)']]
    labels = data['Scored']
    names = data['Name']

    # Normalize the data
    scaler = MinMaxScaler()
    normalized_features = scaler.fit_transform(features)

    # The normalized_features is now a numpy array, you can convert it back to a DataFrame if needed
    normalized_features_df = pd.DataFrame(normalized_features, columns=features.columns)

    # Normalized weights
    weights = [
        0.0,
        0.4,
        0.3,
        0.0,
        0.0,
        0.1,
        0.2
    ]

    # weights = empiricalTest()

    counter = 0
    totalCount = 0

    for index, normalized_row in normalized_features_df.iterrows():
        # Access label for the current row
        label = labels.loc[index]

        # Your further logic with the normalized features and label
        probability = calculateStat(normalized_row, weights)

        # Print or use the calculated values
        # print(f"Name: {names.loc[index]}, Probability: {probability}, Label: {label}")
        threshold = 0.5
        if probability >= threshold:
            totalCount += 1
            if int(label) == 1:
                counter += 1

    ratio = counter / totalCount
    print(f"Weights: {weights}, Ratio: {counter}/{totalCount}, {ratio}")


def thresholdTest():
    # Load the data
    data = pd.read_csv('lib/data.csv')

    # Drop the rows where 'Scored' is empty
    data = data[data['Scored'] != ' ']

    features = data[['GPG', 'Last 5 GPG', 'HGPG', 'PPG', 'OTPM', 'TGPG', 'OTGA', 'Home (1)']]
    labels = data['Scored']
    names = data['Name']

    # Normalize the data
    scaler = MinMaxScaler()
    normalized_features = scaler.fit_transform(features)

    # The normalized_features is now a numpy array, you can convert it back to a DataFrame if needed
    normalized_features_df = pd.DataFrame(normalized_features, columns=features.columns)

    # Normalized weights
    weights = [0.2, 0.3, 0.1, 0.1, 0.2, 0.0, 0.1, 0.0]

    # weights = empiricalTest()

    i = 0
    highestStat = 0
    highestI = i
    while i < 1:
        i = round(i, 2)
        counter = 0
        totalCount = 0

        for index, normalized_row in normalized_features_df.iterrows():
            # Access label for the current row
            label = labels.loc[index]

            # Your further logic with the normalized features and label
            probability = calculateStatNoComp(normalized_row, weights)

            # Print or use the calculated values
            # print(f"Name: {names.loc[index]}, Probability: {probability}, Label: {label}")
            threshold = i
            if probability >= threshold:
                totalCount += 1
                if int(label) == 1:
                    counter += 1

        if totalCount != 0:
            
            ratio = counter / totalCount

            if ratio > highestStat:
                highestStat = ratio
                highestI = i
        
        else:
            break

        print(f"i: {i}, Ratio: {counter}/{totalCount}, {ratio}")


        i += 0.01

    print(f"Best i: {highestI}, {highestStat}")


def empiricalTest():
    # Load the data
    data = pd.read_csv('lib/data.csv')

    # Drop the rows where 'Scored' is empty
    data = data[data['Scored'] != ' ']

    features = data[['GPG', 'Last 5 GPG', 'HGPG', 'PPG', 'OTPM', 'TGPG', 'OTGA', 'Home (1)']]
    labels = data['Scored']
    names = data['Name']

    # Normalize the data
    scaler = MinMaxScaler()
    normalized_features = scaler.fit_transform(features)

    # The normalized_features is now a numpy array, you can convert it back to a DataFrame if needed
    normalized_features_df = pd.DataFrame(normalized_features, columns=features.columns)

    highestStat = 0
    bestWeights = []

    for gpg_weight in range(0, 11, 1):
        for last_5_gpg_weight in range(0, 11 - gpg_weight, 1):
            for hgpg_weight in range(0, 11 - gpg_weight - last_5_gpg_weight, 1):
                for tgpg_weight in range(0, 11 - gpg_weight - last_5_gpg_weight - hgpg_weight, 1):
                    for otga_weight in range(0, 11 - gpg_weight - last_5_gpg_weight - hgpg_weight - tgpg_weight, 1):
                        for comp_weight in range(0, 11 - gpg_weight - last_5_gpg_weight - hgpg_weight - tgpg_weight - otga_weight, 1):
                            home_weight = 10 - gpg_weight - last_5_gpg_weight - hgpg_weight - tgpg_weight - otga_weight - comp_weight

                            # Normalized weights
                            weights = [
                                round(gpg_weight / 10, 2),
                                round(last_5_gpg_weight / 10, 2),
                                round(hgpg_weight / 10, 2),
                                round(tgpg_weight / 10, 2),
                                round(otga_weight / 10, 2),
                                round(home_weight / 10, 2),
                                round(comp_weight / 10, 2)
                            ]

                            counter = 0
                            totalCount = 0

                            for index, normalized_row in normalized_features_df.iterrows():
                                # Access label for the current row
                                label = labels.loc[index]

                                # Your further logic with the normalized features and label
                                probability = calculateStat(normalized_row, weights)

                                # Print or use the calculated values
                                # print(f"Name: {names.loc[index]}, Probability: {probability}, Label: {label}")
                                if probability >= 0.5:
                                    totalCount += 1
                                    if int(label) == 1:
                                        counter += 1

                            ratio = counter / totalCount
                            # print(f"Weights: {weights}, Ratio: {counter}/{totalCount}, {ratio}")

                            if ratio > highestStat:
                                highestStat = ratio
                                bestWeights = weights


    print(f"Highest weights: {bestWeights}, with {highestStat}")

    return bestWeights


def forPMandPPG():
    # Load the data
    data = pd.read_csv('lib/data.csv')

    # Drop the rows where 'Scored' is empty
    data = data[data['Scored'] != ' ']

    features = data[['GPG', 'Last 5 GPG', 'HGPG', 'PPG', 'OTPM', 'TGPG', 'OTGA', 'Home (1)']]
    labels = data['Scored']
    names = data['Name']

    # Normalize the data
    scaler = MinMaxScaler()
    normalized_features = scaler.fit_transform(features)

    # The normalized_features is now a numpy array, you can convert it back to a DataFrame if needed
    normalized_features_df = pd.DataFrame(normalized_features, columns=features.columns)

    highestStat = 0
    bestWeights = []

    for gpg_weight in range(0, 11, 1):
        for last_5_gpg_weight in range(0, 11 - gpg_weight, 1):
            for hgpg_weight in range(0, 11 - gpg_weight - last_5_gpg_weight, 1):
                for otpm_weight in range(0, 11 - gpg_weight - last_5_gpg_weight - hgpg_weight, 1):
                    for ppg_weight in range(0, 11 - gpg_weight - last_5_gpg_weight - hgpg_weight - otpm_weight, 1):
                        for tgpg_weight in range(0, 11 - gpg_weight - last_5_gpg_weight - hgpg_weight - otpm_weight - ppg_weight, 1):
                            for otga_weight in range(0, 11 - gpg_weight - last_5_gpg_weight - hgpg_weight - otpm_weight - ppg_weight - tgpg_weight, 1):

                                home_weight = 10 - gpg_weight - last_5_gpg_weight - hgpg_weight - tgpg_weight - otga_weight - otpm_weight - ppg_weight

                                # Normalized weights
                                weights = [
                                    round(gpg_weight / 10, 2),
                                    round(last_5_gpg_weight / 10, 2),
                                    round(hgpg_weight / 10, 2),
                                    round(otpm_weight / 10, 2),
                                    round(ppg_weight / 10, 2),
                                    round(tgpg_weight / 10, 2),
                                    round(otga_weight / 10, 2),
                                    round(home_weight / 10, 2),
                                ]

                                counter = 0
                                totalCount = 0

                                for index, normalized_row in normalized_features_df.iterrows():
                                    # Access label for the current row
                                    label = labels.loc[index]

                                    # Your further logic with the normalized features and label
                                    probability = calculateStatNoComp(normalized_row, weights)

                                    # Print or use the calculated values
                                    # print(f"Name: {names.loc[index]}, Probability: {probability}, Label: {label}")
                                    if probability >= 0.5:
                                        totalCount += 1
                                        if int(label) == 1:
                                            counter += 1

                                ratio = counter / totalCount
                                # print(f"Weights: {weights}, Ratio: {counter}/{totalCount}, {ratio}")

                                if ratio > highestStat:
                                    highestStat = ratio
                                    bestWeights = weights

            print(weights)

    print(f"Highest weights: {bestWeights}, with {highestStat}")

    return bestWeights

def testCurWeight():
    # Load the data
    data = pd.read_csv('lib/data.csv')

    # Drop the rows where 'Scored' is empty
    data = data[data['Scored'] != ' ']

    features = data[['GPG', 'Last 5 GPG', 'HGPG', 'PPG', 'OTPM', 'TGPG', 'OTGA', 'Home (1)']]
    labels = data['Scored']
    names = data['Name']

    # Normalize the data
    scaler = MinMaxScaler()
    normalized_features = scaler.fit_transform(features)

    # The normalized_features is now a numpy array, you can convert it back to a DataFrame if needed
    normalized_features_df = pd.DataFrame(normalized_features, columns=features.columns)

    # Normalized weights
    weights = [0.2, 0.3, 0.1, 0.1, 0.2, 0.0, 0.1, 0.0]

    # weights = empiricalTest()

    counter = 0
    totalCount = 0

    for index, normalized_row in normalized_features_df.iterrows():
        # Access label for the current row
        label = labels.loc[index]

        # Your further logic with the normalized features and label
        probability = calculateStat(normalized_row, weights)

        # Print or use the calculated values
        # print(f"Name: {names.loc[index]}, Probability: {probability}, Label: {label}")
        threshold = 0.48
        if probability >= threshold:
            totalCount += 1
            if int(label) == 1:
                counter += 1

    
    print(f"Ratio: {counter}/{totalCount}, {counter/totalCount}")


if __name__ == "__main__":
    main()


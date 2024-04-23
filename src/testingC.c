#include "testingC.h"

void empiricalTest() {
    // Load the data
    // TODO: Load the data from 'lib/data.csv' and store it in the 'data' variable
    FILE *file = fopen("../lib/data.csv", "r");
    if (file == NULL) {
        printf("Error opening file\n");
        return;
    }

    // Count the number of rows in the file where 'Scored' is not empty
    int numRows = 0;
    char line[4096];
    fgets(line, sizeof(line), file); // Skip the header line
    while (fgets(line, sizeof(line), file) != NULL) {
        char *token = strtok(line, ",");
        token = strtok(NULL, ","); // Get the 'Scored' column
        if (token != NULL && (token[0] == '0' || token[0] == '1')) {
            numRows++;
        }
    }
    printf("Number of rows: %d\n", numRows);
    rewind(file);

    // Allocate memory for the data array

    // Allocate memory for the data array dynamically
    Stats **stats = (Stats **)malloc(numRows * sizeof(Stats *));
    if (stats == NULL) {
        printf("Memory allocation failed\n");
        return;
    }
    for (int i = 0; i < numRows; i++) {
        stats[i] = (Stats *)malloc(9 * sizeof(Stats));
        if (stats[i] == NULL) {
            printf("Memory allocation failed\n");
            // Free previously allocated memory before returning
            for (int j = 0; j < i; j++) {
                free(stats[j]);
            }
            free(stats);
            return;
        }
    }

    // Read the data from the file into the data array
    fgets(line, sizeof(line), file);
    for (int i = 0; i < numRows; i++) {
        fgets(line, sizeof(line), file);
        char *token = strtok(line, ",");

        // skip date
        token = strtok(NULL, ",");
        
        // get scored
        stats[i]->scored = atoi(token);

        // skip name id team and bet
        for (int j=0; j<4; j++) {
            token = strtok(NULL, ",");
        }

        // get gpg
        token = strtok(NULL, ",");
        stats[i]->gpg = atof(token);

        // get last 5 gpg
        token = strtok(NULL, ",");
        stats[i]->last_5_gpg = atof(token);

        // get hgpg
        token = strtok(NULL, ",");
        stats[i]->hgpg = atof(token);
        
        // get ppg
        token = strtok(NULL, ",");
        stats[i]->ppg = atoi(token);

        // get otpm
        token = strtok(NULL, ",");
        stats[i]->otpm = atoi(token);

        // get tgpg
        token = strtok(NULL, ",");
        stats[i]->tgpg = atof(token);

        // get otga
        token = strtok(NULL, ",");
        stats[i]->otga = atof(token);

        // get home
        token = strtok(NULL, ",");
        stats[i]->home = atof(token);
    }

    // Normalize the data array
    // Scale the data using Min-Max scaling
    for (int j = 1; j < 8; j++) {
        float min = getStat(stats[0], j);
        float max = getStat(stats[0], j);
        
        // Find the minimum and maximum values in the column
        for (int i = 0; i < numRows; i++) {
            if (getStat(stats[i], j) < min) {
                min = getStat(stats[i], j);
            }
            if (getStat(stats[i], j) > max) {
                max = getStat(stats[i], j);
            }
        }
        
        // Normalize the values in the column
        for (int i = 0; i < numRows; i++) {
            setStat(stats[i], j, (getStat(stats[i], j) - min) / (max - min));
        }
    }

    // Close the file
    fclose(file);

    float highestStat = 0;
    int bestCount = 0;
    int bestTotalCount = 0;
    Weights bestWeights;

    // USE DATA PARALLELISM TO OPTIMIZE SPEED

    // could i just calculate probability for those who actually score, check those stats, and then base it off that? Will be like 10 times faster, could then run the top 10 or so weights against all data

    for (int gpg_weight = 0; gpg_weight <= 10; gpg_weight++) {
        for (int last_5_gpg_weight = 0; last_5_gpg_weight <= 10 - gpg_weight; last_5_gpg_weight++) {
            for (int hgpg_weight = 0; hgpg_weight <= 10 - gpg_weight - last_5_gpg_weight; hgpg_weight++) {
                for (int tgpg_weight = 0; tgpg_weight <= 10 - gpg_weight - last_5_gpg_weight - hgpg_weight; tgpg_weight++) {
                    for (int otga_weight = 0; otga_weight <= 10 - gpg_weight - last_5_gpg_weight - hgpg_weight - tgpg_weight; otga_weight++) {
                        for (int home_weight = 0; home_weight <= 10 - gpg_weight - last_5_gpg_weight - hgpg_weight - tgpg_weight - otga_weight; home_weight++) {
                            int comp_weight = 10 - gpg_weight - last_5_gpg_weight - hgpg_weight - tgpg_weight - otga_weight - home_weight;

                            // Normalized weights
                            Weights weights = {
                                (float)gpg_weight / 10,
                                (float)last_5_gpg_weight / 10,
                                (float)hgpg_weight / 10,
                                (float)tgpg_weight / 10,
                                (float)otga_weight / 10,
                                (float)comp_weight / 10,
                                (float)home_weight / 10,
                            };

                            int counter = 0;
                            int totalCount = 0;

                            for (int i = 0; i < numRows; i++) {
                                // Calculate the probability of scoring
                                float probability = calculateStat(stats[i], weights);
                                // printf("%f\n", probability);

                                // Check if the prediction is correct
                                if (probability >= 0.50) {
                                    totalCount++;
                                    if (getStat(stats[i], 0) == 1) {
                                        counter++;
                                    }
                                }
                                exit(0);
                            }

                            // Calculate the ratio
                            float ratio = (float)counter / totalCount;

                            // display the ratio
                            // printf("%d \\ %d : %f - ", counter, totalCount, ratio);
                            // for (int i = 0; i < 7; i++) {
                            //     printf("%f, ", weights[i]);
                            // }
                            // printf("\n");

                            // Update the highestStat and bestWeights if necessary
                            if (ratio > highestStat) {
                                highestStat = ratio;
                                for (int i = 0; i < 7; i++) {
                                    bestWeights = weights;
                                    bestCount = counter;
                                    bestTotalCount = totalCount;
                                }
                            }
                            // exit(0);
                        }
                    }
                }
            }
        }
    }

    printf("Highest weights: [");
    for (int i = 0; i < 7; i++) {
        printf("%f", bestWeights);
        if (i < 6) {
            printf(", ");
        }
    }
    printf("], with %d \\ %d = %f\n", bestCount, bestTotalCount, highestStat);

    // TODO: Return the 'bestWeights' array
}

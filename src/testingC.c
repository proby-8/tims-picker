#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

float calculateStat(float data[], float weights[]) {

    float probability = 0;

    float ratio = 0.18;
    float composite = ratio*data[5] + (1-ratio)*data[4];

    // replace the composite with the composite stat
    float newData[7] = {data[1], data[2], data[3], composite, data[6], data[7], data[8]};

    for (int i = 0; i < 7; i++) {
        probability += newData[i] * weights[i];
    }

    // Apply the sigmoid function?
    // probability = 1 / (1 + exp(-probability));

    return probability;
}

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
    float data[numRows][9];

    // Read the data from the file into the data array
    fgets(line, sizeof(line), file);
    for (int i = 0; i < numRows; i++) {
        fgets(line, sizeof(line), file);
        char *token = strtok(line, ",");

        // skip date
        token = strtok(NULL, ",");
        
        // get scored
        data[i][0] = atoi(token);

        // skip name id team and bet
        for (int j=0; j<4; j++) {
            token = strtok(NULL, ",");
        }

        // get gpg
        token = strtok(NULL, ",");
        data[i][1] = atof(token);

        // get last 5 gpg
        token = strtok(NULL, ",");
        data[i][2] = atof(token);

        // get hgpg
        token = strtok(NULL, ",");
        data[i][3] = atof(token);

        // get ppg
        token = strtok(NULL, ",");
        data[i][4] = atoi(token);

        // get otpm
        token = strtok(NULL, ",");
        data[i][5] = atoi(token);

        // get tgpg
        token = strtok(NULL, ",");
        data[i][6] = atof(token);

        // get otga
        token = strtok(NULL, ",");
        data[i][7] = atof(token);

        // get home
        token = strtok(NULL, ",");
        data[i][8] = atof(token);
    }

    // Normalize the data array
    // Scale the data using Min-Max scaling
    float min = data[0][0];
    float max = data[0][0];
    for (int j = 1; j < 9; j++) {
        for (int i = 0; i < numRows; i++) {
            if (data[i][j] < min) {
                min = data[i][j];
            }
            if (data[i][j] > max) {
                max = data[i][j];
            }
        }

        for (int i = 0; i < numRows; i++) {
            data[i][j] = (data[i][j] - min) / (max - min);
        }
    }

    // Close the file
    fclose(file);

    float highestStat = 0;
    float bestWeights[7];

    // USE DATA PARALLELISM TO OPTIMIZE SPEED

    // could i just calculate probability for those who actually score, check those stats, and then base it off that? Will be like 10 times faster, could then run the top 10 or so weights against all data

    for (int gpg_weight = 0; gpg_weight <= 10; gpg_weight++) {
        for (int last_5_gpg_weight = 0; last_5_gpg_weight <= 10 - gpg_weight; last_5_gpg_weight++) {
            for (int hgpg_weight = 0; hgpg_weight <= 10 - gpg_weight - last_5_gpg_weight; hgpg_weight++) {
                for (int tgpg_weight = 0; tgpg_weight <= 10 - gpg_weight - last_5_gpg_weight - hgpg_weight; tgpg_weight++) {
                    for (int otga_weight = 0; otga_weight <= 10 - gpg_weight - last_5_gpg_weight - hgpg_weight - tgpg_weight; otga_weight++) {
                        for (int comp_weight = 0; comp_weight <= 10 - gpg_weight - last_5_gpg_weight - hgpg_weight - tgpg_weight - otga_weight; comp_weight++) {
                            int home_weight = 10 - gpg_weight - last_5_gpg_weight - hgpg_weight - tgpg_weight - otga_weight - comp_weight;

                            // Normalized weights
                            float weights[7] = {
                                (float)gpg_weight / 10,
                                (float)last_5_gpg_weight / 10,
                                (float)hgpg_weight / 10,
                                (float)tgpg_weight / 10,
                                (float)otga_weight / 10,
                                (float)home_weight / 10,
                                (float)comp_weight / 10
                            };

                            int counter = 0;
                            int totalCount = 0;

                            for (int i = 0; i < numRows; i++) {
                                // Calculate the probability of scoring
                                float probability = calculateStat(data[i], weights);
                                // printf("%f\n", probability);

                                // Check if the prediction is correct
                                if (probability >= 0.48) {
                                    totalCount++;
                                    if (data[i][0] == 1) {
                                        counter++;
                                    }
                                }
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
                                    bestWeights[i] = weights[i];
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
        printf("%f", bestWeights[i]);
        if (i < 6) {
            printf(", ");
        }
    }
    printf("], with %f\n", highestStat);

    // TODO: Return the 'bestWeights' array
}
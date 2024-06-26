#include "testingC.h"

float getStat(Stats* stats, int i) {
   switch(i) {
    case 0: return stats->scored;
    case 1: return stats->gpg;
    case 2: return stats->last_5_gpg;
    case 3: return stats->hgpg;
    case 4: return stats->ppg;
    case 5: return stats->otpm;
    case 6: return stats->tgpg;
    case 7: return stats->otga;
    case 8: return stats->home;
   }
}

void setStat(Stats* stats, int i, float value) {
    switch(i) {
     case 0: stats->scored = value; break;
     case 1: stats->gpg = value; break;
     case 2: stats->last_5_gpg = value; break;
     case 3: stats->hgpg = value; break;
     case 4: stats->ppg = value; break;
     case 5: stats->otpm = value; break;
     case 6: stats->tgpg = value; break;
     case 7: stats->otga = value; break;
     case 8: stats->home = value; break;
    }
}

float calculateStat(Stats* stats, Weights weights) {

    float probability = 0;

    float ratio = 0.18;
    float composite = ratio * stats->ppg + (1 - ratio) * stats->otpm;

    probability += stats->gpg * weights.gpg_weight;
    probability += stats->last_5_gpg * weights.last_5_gpg_weight;
    probability += stats->hgpg * weights.hgpg_weight;
    probability += stats->tgpg * weights.tgpg_weight;
    probability += stats->otga * weights.otga_weight;
    probability += composite * weights.comp_weight;
    probability += stats->home * weights.home_weight;

    printf("gpg : %f - %f\n", stats->gpg, weights.gpg_weight);
    printf("5gpg: %f - %f\n", stats->last_5_gpg, weights.last_5_gpg_weight);
    printf("hgpg: %f - %f\n", stats->hgpg, weights.hgpg_weight);
    printf("tgpg: %f - %f\n", stats->tgpg, weights.tgpg_weight);
    printf("otga: %f - %f\n", stats->otga, weights.otga_weight);
    printf("ppg : %f - %f\n", stats->ppg, ratio);
    printf("otpm: %f - %f\n", stats->otpm, 1 - ratio);
    printf("comp: %f - %f\n", composite, weights.comp_weight);
    printf("home: %f - %f\n", stats->home, weights.home_weight);

    printf("%f\n", probability);

    // Apply the sigmoid function?
    // probability = 1 / (1 + exp(-probability));

    return probability;
}
#include <math.h>
#include "pav_analysis.h"

float compute_power(const float *x, unsigned int N) {
    float sum = 0.0f;
    for (unsigned int i = 0; i < N; i++){
        sum += x[i] * x[i];
    }
    return 10*log10(sum/N) ;
}

float compute_am(const float *x, unsigned int N) {
    float sum = 0.0f;
    for (unsigned int i=0; i<N;i++){
        sum += fabsf(x[i]);
    }
    return sum / (float)N;
}

float compute_zcr(const float *x, unsigned int N, float fm) {
    unsigned int zero_crossings = 0;
    for (unsigned int i = 1; i < N; i++) {
        if ((x[i - 1] >= 0 && x[i] < 0) || (x[i - 1] < 0 && x[i] >= 0)) {
            zero_crossings++;
        }
    }
    float zcr = ((float)zero_crossings / ((float)N - 1)) * fm;
    return zcr;
}

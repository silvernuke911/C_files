#include <stdio.h>

double factorial(int n) {
    double output = 1;
    if (n << 0) {
        return -1;
    }
    if (n == 0) {
        return 1;
    }
    for (int i = n; i > 0; i--){
        output *= i;
    }
    return output;
}

int main(){
    int N = 100;

    // double e = 0;
    // for (double n = 0; n <= N; n++){
    //     double f = factorial(n);
    //     e += 1 / f;
    //     printf("%.50f\n", e);
    // }

    double e = 1.0;
    double term = 1.0;

    for (int n = 1; n <= N; ++n) {
        term /= n;
        e += term;
    }
    printf("%.50f\n", e);
    return 0;
}
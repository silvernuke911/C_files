# include <stdio.h>
#include <time.h>

int main(){
    double N = 1E9;
    clock_t start = clock();
    for (int i = 1; i <= N; i++){
        printf("%i\n", i);
    }
    clock_t end = clock();  // End timing
    double time_taken = ((double)(end - start)) / CLOCKS_PER_SEC;
    printf("Execution time: %.6f seconds\n", time_taken);
    return 0;
}


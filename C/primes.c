#include <stdio.h>
#include <stdbool.h>
#include <time.h>  // For measuring execution time

void sieve_of_eratosthenes(int N) {
    if (N < 2) {
        printf("No prime numbers up to %d.\n", N);
        return;
    }

    bool primes[N + 1];
    for (int i = 0; i <= N; i++) {
        primes[i] = true;
    }
    primes[0] = primes[1] = false; // 0 and 1 are not prime

    for (int p = 2; p * p <= N; p++) {
        if (primes[p]) {
            for (int i = p * p; i <= N; i += p) {
                primes[i] = false;
            }
        }
    }

    printf("Prime numbers up to %d:\n", N);
    for (int i = 2; i <= N; i++) {
        if (primes[i]) {
            printf("%d ", i);
        }
    }
    printf("\n");
}

int main() {
    int N = 1000000;
    // printf("Enter the value of N: ");
    // scanf("%d", &N);

    clock_t start = clock();  // Start timing

    sieve_of_eratosthenes(N);

    clock_t end = clock();  // End timing
    double time_taken = ((double)(end - start)) / CLOCKS_PER_SEC;

    printf("Execution time: %.6f seconds\n", time_taken);

    return 0;
}

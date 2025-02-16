import time

def sieve_of_eratosthenes(N):
    if N < 2:
        print(f"No prime numbers up to {N}.")
        return

    primes = [True] * (N + 1)
    primes[0] = primes[1] = False  # 0 and 1 are not prime

    for p in range(2, int(N**0.5) + 1):
        if primes[p]:
            for i in range(p * p, N + 1, p):
                primes[i] = False

    print(f"Prime numbers up to {N}:")
    print([i for i in range(2, N + 1) if primes[i]])

if __name__ == "__main__":
    N = 1000000

    start_time = time.time()  # Start timing

    sieve_of_eratosthenes(N)

    end_time = time.time()  # End timing
    time_taken = end_time - start_time

    print(f"Execution time: {time_taken:.6f} seconds")

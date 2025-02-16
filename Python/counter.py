import time
N = int(1e5)
s = time.time()
print(N)
for i in range(N):
    print(i)
e = time.time()
print(f'Execution time: {e-s}')
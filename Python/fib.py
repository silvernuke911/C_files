import numpy as np
import matplotlib.pyplot as plt

def fibonnaci(N):
    fib_nums = np.zeros(N)
    fib_nums[0] = 1
    fib_nums[1] = 1
    for i in range(2,N):
        fib_nums[i] = fib_nums[i-1] + fib_nums[i-2]
    return fib_nums

N = 100
phi = (1+np.sqrt(5))/2
print(phi)
x = np.arange(N)
y = fibonnaci(N)
print(y)
y2 = phi**x
plt.plot(x,y)
plt.plot(x,y2)
plt.show()
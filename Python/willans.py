# Willans prime generating formula

import numpy as np 

def willans_pgf(n):
    def fact(n):
        if n==0:
            result = 1
        else:
            prods = np.arange(1,n+1, dtype = int)
            result = np.prod(prods)
        return int(result)
    def prime_detector(j):
        res0 = (fact(j-1)+1)/j
        res1 = np.pi * res0
        res2 = np.cos(res1)**2
        res3 = np.floor(res2)
        return int(res3)
    def prime_detector_sum(i):
        s = 0
        for j in range(1,i+1):
            s += prime_detector(j)
        return int(s)
    def prime_greater_detector(n, i):
        res1 = n / prime_detector_sum(i)
        res2 = res1 ** (1/n)
        print(res2)
        res3 = np.floor(res2)
        return int(res3)
    def prime_greater_sum(n):
        s = 0
        for i in range(1, 2**n + 1):
            s += prime_greater_detector(n, i)
        return int(s)
    result = 1 + prime_greater_sum(n)
    return result

print(willans_pgf(4))
        












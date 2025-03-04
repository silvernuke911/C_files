import numpy as np
import matplotlib.pyplot as plt
import math  # Import math for factorial

# Define x with proper spacing
x = np.arange(-2*np.pi, 2*np.pi, 0.01)
y = np.sin(x)

plt.figure(figsize=(12, 6)) 
plt.plot(
    x,
    y,
    color='k',
    linewidth=4,
    label=r'$\sin(x)$'
)

n = 20
for i in range(n+1):
    s = np.zeros_like(x) 
    for j in range(i):
        s += ((-1)**j / math.factorial(2*j + 1)) * (x ** (2*j + 1))
    
    plt.plot(
        x,
        s,
        label=f'$n = {i}$'
    )

plt.xlabel(r'$x$')
plt.ylabel(r'$y$')
plt.xlim(-2*np.pi, 2*np.pi)
plt.ylim(-2,2)
# plt.legend()
plt.grid(True)  # Optional: adds a grid for better visualization

print('Plotting ...')
plt.show()

import numpy as np
import matplotlib.pyplot as plt
import math  # Import math for factorial

# Define x with proper spacing
x = np.arange(-2*np.pi, 2*np.pi, 0.01)
y = np.cos(x)  # True cosine function

plt.figure(figsize=(12, 6))  # Set figure size (width, height)
plt.plot(
    x,
    y,
    color='k',
    linewidth=3,
    label=r'$\cos(x)$'  # Use raw string for LaTeX formatting
)

n = 10  # Maximum degree of Taylor series
for i in range(n+1):
    s = np.zeros_like(x)  # Initialize s as an array
    for j in range(i):
        s += ((-1)**j / math.factorial(2*j)) * (x ** (2*j))  # Taylor series for cos(x)
    
    plt.plot(
        x,
        s,
        label=f'$n = {i}$'
    )

plt.xlabel(r'$x$')
plt.ylabel(r'$y$')
plt.grid(True)  # Optional: adds a grid for better visualization
plt.xlim(-2*np.pi, 2*np.pi)
plt.ylim(-2,2)
print('Plotting ...')
plt.show()

import numpy as np
import matplotlib.pyplot as plt
import math  # Import math for factorial

# Define x with proper spacing
x = np.arange(-2, 2, 0.01)
y = np.exp(x)  # True exponential function

plt.figure(figsize=(6, 12))  # Set figure size (width, height)
plt.plot(
    x,
    y,
    color='k',
    linewidth=3,
    label=r'$e^x$'  # Use raw string for LaTeX formatting
)

n = 10  # Maximum degree of Taylor series
for i in range(n+1):
    s = np.zeros_like(x)  # Initialize s as an array
    for j in range(i):
        s += (x ** j) / math.factorial(j)  # Taylor series for e^x
    
    plt.plot(
        x,
        s,
        label=f'$n = {i}$'
    )

plt.xlabel(r'$x$')
plt.ylabel(r'$y$')
plt.grid(True)  # Optional: adds a grid for better visualization
plt.xlim(-2,2)
plt.ylim(-1,10)
print('Plotting ...')
plt.show()

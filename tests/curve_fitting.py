import numpy as np
import matplotlib.pyplot as plt

# Data points
n_e = np.array([30, 150, 300, 750, 1250, 3750, 10500, 18750, 45000, 93750, 112500])
bfs_runtimes = np.array([0.099, 0.114, 0.213, 0.804, 2.157, 16.968, 134.979, 424.735, 2859.067, 9926.912, 12217.326])
dfs_runtimes = np.array([0.109, 0.1102, 0.1625, 0.5352, 1.4908, 11.2988, 110.229, 334.997, 1963.761, 8875.124, 11895.126])
# Linear fit
coefficients = np.polyfit(n_e, dfs_runtimes, 1)  # Linear fit on the original scale
linear_polynomial = np.poly1d(coefficients)

# Linear equation: y = mx + c
m = linear_polynomial.coefficients[0]  # Slope from linear fit
c = linear_polynomial.coefficients[1]  # Intercept from linear fit
equation_str = f'dfs_runtimes = {m:.4f} * n_e + {c:.4f}'

# Visualization
plt.scatter(n_e, dfs_runtimes, color='red', label='Data points')
plt.plot(n_e, linear_polynomial(n_e), label='Fitted Line')
plt.legend()
plt.xlabel('Vertices + Aristas')
plt.ylabel('Tiempo de ejecución (s)')
plt.title('Linear Fitting')
plt.grid(True, which="both", ls="--")
plt.text(n_e[0], dfs_runtimes[-1]/3, equation_str, verticalalignment='bottom', horizontalalignment='left', color='blue', fontsize=12)  # Display the equation on the graph
plt.show()

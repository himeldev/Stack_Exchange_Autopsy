import numpy as np
import matplotlib.pyplot as plt

x = np.arange(-1.2, 1.2, .025)
y = np.arange(-1.2, 1.2, .025)
X, Y = np.meshgrid(x, y)
Z = np.cos(X)*np.cos(Y)
print Z
Z = Z*Z
print Z

plt.subplot(1,2,1)
CS = plt.contour(X, Y, Z)   # set levels automatically
plt.clabel(CS, inline=1, fontsize=10)
plt.subplot(1,2,2)
CS = plt.contour(X, Y, Z-.1, CS.levels)  # set levels as previous levels
plt.clabel(CS, inline=1, fontsize=10)
plt.show()

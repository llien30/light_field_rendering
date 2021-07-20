import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import LinearNDInterpolator

rng = np.random.default_rng()
x = rng.random(10) - 0.5
y = rng.random(10) - 0.5
z = np.hypot(x, y)
X = np.linspace(min(x), max(x))
Y = np.linspace(min(y), max(y))
X, Y = np.meshgrid(X, Y)  # 2D grid for interpolation
interp = LinearNDInterpolator(list(zip(x, y)), z)
print(list(zip(x, y)))
Z = interp(X, Y)
print(interp(0, 0))
plt.pcolormesh(X, Y, Z, shading="auto")
plt.plot(x, y, "ok", label="input point")
plt.legend()
plt.colorbar()
plt.axis("equal")
plt.show()

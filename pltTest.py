import time

import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
np.set_printoptions(precision=2)

# Make the X, Y meshgrid.
xs = np.linspace(1, 12, 12)
ys = np.linspace(1, 12, 12)
X, Y = np.meshgrid(xs, ys)

# Set the z axis limits, so they aren't recalculated each frame.
ax.set_zlim(-2, 0)

# Begin plotting.
wframe = None
tstart = time.time()
for phi in np.linspace(0, 10/np.pi, 100):   
    # Generate data.
    Z = np.cos(0.2 * np.pi * X + phi)*0.5-1
    # Plot the new wireframe and pause briefly before continuing.
    wframe = ax.plot_wireframe(X, Y, Z, rstride=1, cstride=1)
    plt.pause(.001)
    wframe.remove()

for i in range(len(X)):
    print(Z[i])

print('Average FPS: %f' % (100 / (time.time() - tstart)))
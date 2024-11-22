import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
nGrid = [3, 5]
ax = []

depth = np.linspace(-100, 0, 100)
x = np.random.rand(100)
y = (x - 0.5) / 1

ax1 = fig.add_axes((0.1, 0.1, 0.3, 0.8))
ax2 = fig.add_axes((0.4, 0.1, 0.4, 0.8))

yticks = ax1.get_yticks()

for idx, ax in enumerate([ax1, ax2]):
    ax.xaxis.set_tick_params(labelbottom=False)
    ax.yaxis.set_tick_params(labelsize=8)
    xTicks = np.linspace(-1, 1, nGrid[idx] + 1)
    ax.grid(axis="both")
    ax.set_xticks(xTicks)
    ax.tick_params(direction="in")


ax2.plot(x, depth, "r")
ax2.set_xlim(0, 1)
ax2.tick_params(labelleft=False)

ax_temp = ax2.twiny()
ax_temp.plot(y, depth, "b")
ax_temp.set_xlim(-0.5, 1)


plt.show()

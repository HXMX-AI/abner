import matplotlib.pyplot    as      plt
import numpy                as      np

fig = plt.figure()
ax  = [None, None]
nGrid = [3, 5]

depth = np.linspace(-100,0, 100)
x     = np.random.rand(100)
y     = (x-0.5)/1

ax[0] = fig.add_axes([0.1, 0.1, 0.3, 0.8])
ax[1] = fig.add_axes([0.4, 0.1, 0.4, 0.8])

yticks = ax[0].get_yticks()

for n in [0,1]:
    ax[n].xaxis.set_tick_params(labelbottom = False)
    ax[n].yaxis.set_tick_params(labelsize=8)
    xTicks = np.linspace(-1,1, nGrid[n]+1)
    ax[n].grid(axis='both')
    ax[n].set_xticks(xTicks)
    ax[n].tick_params(direction = 'in')
    if n != 0:
        ax[n].tick_params(labelleft=False)


ax[1].plot(x, depth, 'r')
ax[1].set_xlim(0, 1)

ax_temp = ax[1].twiny()
ax_temp.plot(y, depth, 'b')
ax_temp.set_xlim(-0.5,1)


plt.show()
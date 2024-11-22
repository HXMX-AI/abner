import matplotlib.pyplot as plt


coordbot = (0.05, 0.05, 0.3, 0.5)
coords = (0.05, 0.75, 0.9, 0.2)

fig = plt.figure()


ax0 = fig.add_axes(coordbot)
ax = fig.add_axes(coords)
ax.set_xticks([])
ax.set_yticks([])

ax.text(0.05, 0.05, "Curve")

plt.show()

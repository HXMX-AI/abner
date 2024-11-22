import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector
import numpy as np


# Function to be triggered when a span is selected
def onselect(xmin, xmax):
    print(f"Selected Span: xmin={xmin}, xmax={xmax}")


# Generate example data
x_data = np.linspace(0, 10, 100)
y_data = np.sin(x_data)
# Create a figure and axes
fig, ax = plt.subplots()
# Plot the data
ax.plot(x_data, y_data)
# Create a SpanSelector
span_selector = SpanSelector(
    ax,
    onselect,
    direction="horizontal",
    useblit=True,
    props=dict(alpha=0.5, facecolor="red"),
)
plt.show()


import  matplotlib.pyplot           as      plt
from    matplotlib.widgets          import  RangeSlider

# SLIDER CREATE ....................................
def Add_Slider(fig, slider_coord, zRange):
    slider_ax = fig.add_axes(slider_coord)
    slider    = RangeSlider(slider_ax, 'DEPTH', zRange[0],  zRange[1],
                     valinit = zRange, orientation = 'vertical',
                     closedmin = True, closedmax = True)

    slider.valtext.set_visible(False)
    slider.label.set_size(7)
    return slider
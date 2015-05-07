#!/Users/leclercq/miniconda/bin/python

import aplpy
import matplotlib.pyplot as mpl

fig = mpl.figure(figsize=(15, 7))

f1 = aplpy.FITSFigure('N4Qsmooth.fits', figure=fig, subplot=[0.1,0.1,0.35,0.8])
f1.set_tick_labels_font(size='x-small')
f1.set_axis_labels_font(size='small')
f1.show_grayscale()

f2 = aplpy.FITSFigure('wolQN4.fits', figure=fig, subplot=[0.5,0.1,0.35,0.8])
f2.set_tick_labels_font(size='x-small')
f2.set_axis_labels_font(size='small')
f2.show_grayscale()

f2.hide_yaxis_label()
f2.hide_ytick_labels()

fig.canvas.draw()

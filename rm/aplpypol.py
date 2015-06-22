#/Users/leclercq/miniconda/bin/python

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as mpl

import aplpy

fig = mpl.figure(figsize=(14,7))

f1 = aplpy.FITSFigure('N4_polarised_intensity.fits', figure=fig)

f1.tick_labels.set_font(size='x-small')
f1.axis_labels.set_font(size='small')
f1.show_colorscale(cmap='afmhot')
f1.add_colorbar()
f1.colorbar.set_axis_label_text('brightness [K]')
f1.show_rectangles(0,32,1000,1000)
f1.show_rectangles(1000,32,1000,1000)
f1.show_rectangles(2000,32,1000,1000)
f1.show_rectangles(3000,32,1000,1000)
f1.show_rectangles(4000,32,1000,1000)

## f2 = aplpy.FITSFigure('S2rm0.fits', figure=fig,
##                       subplot=[0.1, 0.4, 0.9, 0.3])

## f2.tick_labels.set_font(size='x-small')
## f2.axis_labels.set_font(size='small')
## f2.show_colorscale(cmap='seismic',vmin=-150,vmax=150)
## f2.add_colorbar()
## f2.colorbar.set_axis_label_text('RM [rad/m^2]')

## f3 = aplpy.FITSFigure('N4rm0.fits', figure=fig,
##                       subplot=[0.1, 0.1, 0.9, 0.3])

## f3.tick_labels.set_font(size='x-small')
## f3.axis_labels.set_font(size='small')
## f3.show_colorscale(cmap='seismic',vmin=-150,vmax=150)
## f3.add_colorbar()
## f3.colorbar.set_axis_label_text('RM [rad/m^2]')

## f1.axis_labels.hide_x()
## f1.tick_labels.hide_x()

## f2.axis_labels.hide_x()
## f2.tick_labels.hide_x()

fig.savefig('n4pol_withchunks.pdf', bbox_inches='tight')

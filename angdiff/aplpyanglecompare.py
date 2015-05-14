#/Users/leclercq/miniconda/bin/python

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as mpl
import sys
import aplpy

galq=sys.argv[1]
galu=sys.argv[2]
wolq=sys.argv[3]
wolu=sys.argv[4]
field=sys.argv[5]

fig = mpl.figure(figsize=(25.3, 10))

f1 = aplpy.FITSFigure(galq, figure=fig,
                      subplot=[0.1, 0.4, 0.38, 0.2])

f1.tick_labels.set_font(size='x-small')
f1.axis_labels.set_font(size='small')
f1.add_label(0.15,0.85,'GALFACTS Q ('+field+')',relative=True,size='large',layer='title')
f1.show_colorscale(cmap='afmhot',vmin=-0.32,vmax=0.12)
f1.add_colorbar()
f1.colorbar.set_axis_label_text('K')
f1.colorbar.set_location('bottom')
f1.colorbar.set_pad(0.4)
f1.colorbar.set_axis_label_font(size='x-small')
f1.ticks.set_color('black')

f2 = aplpy.FITSFigure(wolq, figure=fig,
                      subplot=[0.1, 0.1, 0.38, 0.2])

f2.tick_labels.set_font(size='x-small')
f2.axis_labels.set_font(size='small')
f2.add_label(0.12,0.85,'DRAO Q ('+field+')',relative=True,size='large',layer='title')
f2.show_colorscale(cmap='afmhot',vmin=-0.32,vmax=0.12)
f2.add_colorbar()
f2.colorbar.set_axis_label_text('K')
f2.colorbar.set_location('bottom')
f2.colorbar.set_pad(0.4)
f2.colorbar.set_axis_label_font(size='x-small')
f2.ticks.set_color('black')

f3 = aplpy.FITSFigure(galu, figure=fig,
                      subplot=[0.45, 0.4, 0.38, 0.2])

f3.tick_labels.set_font(size='x-small')
f3.axis_labels.set_font(size='small')
f3.add_label(0.15,0.85,'GALFACTS U ('+field+')',relative=True,size='large',layer='title')
f3.show_colorscale(cmap='afmhot',vmin=-0.32,vmax=0.12)
f3.add_colorbar()
f3.colorbar.set_axis_label_text('K')
f3.colorbar.set_location('bottom')
f3.colorbar.set_pad(0.4)
f3.colorbar.set_axis_label_font(size='x-small')
f3.ticks.set_color('black')

f4 = aplpy.FITSFigure(wolu, figure=fig,
                      subplot=[0.45, 0.1, 0.38, 0.2])

f4.tick_labels.set_font(size='x-small')
f4.axis_labels.set_font(size='small')
f4.add_label(0.12,0.85,'DRAO U ('+field+')',relative=True,size='large',layer='title')
f4.show_colorscale(cmap='afmhot',vmin=-0.32,vmax=0.12)
f4.add_colorbar()
f4.colorbar.set_axis_label_text('K')
f4.colorbar.set_location('bottom')
f4.colorbar.set_pad(0.4)
f4.colorbar.set_axis_label_font(size='x-small')
f4.ticks.set_color('black')

## f1.axis_labels.hide_x()
## f1.tick_labels.hide_x()
## f3.axis_labels.hide_x()
## f3.tick_labels.hide_x()
## f3.axis_labels.hide_y()
## f3.tick_labels.hide_y()
## f4.axis_labels.hide_y()
## f4.tick_labels.hide_y()
print 'saving output to '+ field+'viscompare.pdf'
fig.savefig(field+'viscompare.pdf', bbox_inches='tight')

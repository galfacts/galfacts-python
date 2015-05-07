#!/Users/leclercq/miniconda/bin/python

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as mpl

import aplpy

fig = mpl.figure(figsize=(14, 7))

f1 = aplpy.FITSFigure('S1_diff_map.fits', figure=fig,
                      subplot=[0.1, 0.5, 0.9, 0.38])

f1.tick_labels.set_font(size='x-small')
f1.axis_labels.set_font(size='small')
f1.show_colorscale(cmap='gist_rainbow',vmin=-20,vmax=20)
f1.add_colorbar()
f1.colorbar.set_axis_label_text('deg')

f2 = aplpy.FITSFigure('S1_diff_err_map.fits', figure=fig,
                      subplot=[0.1, 0.1, 0.9, 0.38])

f2.tick_labels.set_font(size='x-small')
f2.axis_labels.set_font(size='small')
f2.show_colorscale(cmap='gist_rainbow',vmin=0,vmax=2)
f2.add_colorbar()
f2.colorbar.set_axis_label_text('deg')

f1.axis_labels.hide_x()
f1.tick_labels.hide_x()

fig.savefig('S1angdiff.pdf', bbox_inches='tight')

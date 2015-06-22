#!/Users/leclercq/miniconda/bin/python

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as mpl
import sys
import aplpy

diff=sys.argv[1]
err=sys.argv[2]
field=sys.argv[3]

fig = mpl.figure(figsize=(14, 7))

f1 = aplpy.FITSFigure(diff, figure=fig,
                      subplot=[0.1, 0.5, 0.9, 0.38])

f1.tick_labels.set_font(size='x-small')
f1.axis_labels.set_font(size='small')
f1.show_colorscale(cmap='gist_rainbow',vmin=-20,vmax=20)
f1.add_colorbar()
f1.colorbar.set_axis_label_text('deg')

f2 = aplpy.FITSFigure(err, figure=fig,
                      subplot=[0.1, 0.1, 0.9, 0.38])

f2.tick_labels.set_font(size='x-small')
f2.axis_labels.set_font(size='small')
f2.show_colorscale(cmap='gist_rainbow',vmin=-20,vmax=20)
f2.add_colorbar()
f2.colorbar.set_axis_label_text('deg')

f1.axis_labels.hide_x()
f1.tick_labels.hide_x()

print 'Saving output to '+field+'angdiff.pdf'

fig.savefig(field+'angdiff.pdf', bbox_inches='tight')

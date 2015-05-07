#!/Users/leclercq/miniconda/bin/python

import numpy as np
from numpy import pi
from astropy.io import fits
from astropy import constants as const
import sys
import matplotlib
matplotlib.use('MacOSX')
import matplotlib.pylab as plt

#Plot the angle versus lambda squared for a given pixel


anglein=sys.argv[1]
xpix=sys.argv[2]
ypix=sys.argv[3]

ang_hdu=fits.open(anglein)

angcube=ang_hdu[0].data
lamsq=ang_hdu[1].data.field(1)

#plot plot plot
fig,ax=plt.subplots()
title='Angle profile for pixel {0},{1}'.format(xpix,ypix)
ax.set_title(title)
ax.set_xlabel('$\lambda^2[m^2]$',fontsize=16 )
ax.set_ylabel('Polarisation angle (rad)')

ax.plot(lamsq,angcube[:,ypix,xpix],'r+-')

plt.show()

#!/Users/leclercq/miniconda/bin/python

import numpy as np
import theil_sen as ts
import matplotlib
matplotlib.use('MacOSX')
import matplotlib.pylab as plt
from astropy.io import fits
import sys
from numpy import pi

infile=sys.argv[1]
field=infile[6:8]

angin=fits.open(sys.argv[1])

angfile=field+'_rmfit_angles_for_aplpy.fits'

ang_header=angin[0].header

ang_header['OBJECT']='GALFACTS_{0} pol. angles from RM fit(degrees)'.format(field)

angles=angin[0].data

for idx, pixang in np.ndenumerate(angles):
    if pixang == np.nan:
        angles[idx[0],idx[1]]=np.nan
    elif pixang > pi/2.:
        while pixang >= pi/2.:
            pixang -= pi
        angles[idx[0],idx[1]]=pixang
    elif pixang < pi/2.:
        while pixang <= -pi/2.:
            pixang += pi
        angles[idx[0],idx[1]]=pixang

angles*=180./pi

print 'New maximum: '+str(np.nanmax(angles))
print 'New minimun: '+str(np.nanmin(angles))

fits.writeto(angfile,angles,header=ang_header)




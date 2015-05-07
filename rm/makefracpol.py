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
field=infile[9:11]

qin=fits.open(sys.argv[1])
uin=fits.open(sys.argv[2])
iin=fits.open(sys.argv[3])

polfile=field+'_fracpolarised_intensity_pos.fits'
angfile=field+'_raw_angles_for_aplpy.fits'

header_cube=qin[0].header

map_header=header_cube.copy()
map_header.remove('ctype3')
map_header.remove('crval3')
map_header.remove('crpix3')
map_header.remove('cdelt3')
map_header.remove('crota3')
map_header['OBJECT']='GALFACTS_{0} Fractional polarization values'.format(field)

qdata=qin[0].data[0,:,:]
udata=uin[0].data[0,:,:]
idata=iin[0].data[0,:,:]

polint=np.sqrt(qdata**2+udata**2)
fracpol=polint/idata

fits.writeto(polfile,fracpol,header=map_header)

## polang=0.5*np.arctan2(udata,qdata)

## for idx, pixang in np.ndenumerate(polang):
##     if pixang == np.nan:
##         polang[idx[0],idx[1]]=np.nan
##     elif pixang > pi/2.:
##         pixang -= pi
##         polang[idx[0],idx[1]]=pixang
##     elif pixang < -pi/2.:
##         pixang += pi
##         polang[idx[0],idx[1]]=pixang

## print 'New maximum: '+str(np.nanmax(polang))
## print 'New minimun: '+str(np.nanmin(polang))

## polang*=180./pi

## ang_header=map_header.copy()
## ang_header['OBJECT']='GALFACTS_{0} pol. angles from band0 avg (degrees)'.format(field)

## fits.writeto(angfile,polang,header=ang_header)






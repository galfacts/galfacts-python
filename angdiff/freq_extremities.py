#Extracts the first and last channels of a binned galfacts cube, so we can smooth them.

import numpy as np
from astropy.io import fits
import sys

hdu1=fits.open(sys.argv[1])
cube=hdu1[0].data
head=hdu1[0].header
mfrs=hdu1[2].data.field(3)

field=infile[0:2]
stokes=infile[10]

first_plane=cube[0,:,:]
print first_plane.shape

last_plane=cube[-1,:,:]
print last_plane.shape

mfr_first=mfrs[0]
mfr_last=mfrs[-1]

first_head=head.copy()
last_head=head.copy()

first_head.remove('ctype3')
first_head.remove('crval3')
first_head.remove('crpix3')
first_head.remove('cdelt3')
first_head.remove('crota3')
first_head['BUNIT']='K'
first_head['COMMENT']='Frequency:{0:E}'.format(mfr_first)


last_head.remove('ctype3')
last_head.remove('crval3')
last_head.remove('crpix3')
last_head.remove('cdelt3')
last_head.remove('crota3')
last_head['BUNIT']='K'
last_head['COMMENT']='Frequency:{0:E}'.format(mfr_last)

first_hdu=fits.PrimaryHDU(first_plane,header=first_head)
last_hdu=fits.PrimaryHDU(last_plane,header=last_head)

outfile_first=field+'_binned_'+stokes+'_first.fits'
outfile_last=field+'_binned_'+stokes+'_last.fits'

first_hdu.writeto(outfile_first)
last_hdu.writeto(outfile_last)

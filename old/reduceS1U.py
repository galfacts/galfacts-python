#!/usr/local/bin/python

import sys
import numpy as np
from astropy.io import fits


infile=sys.argv[1]
start=np.int(sys.argv[2])
end=np.int(sys.argv[3])

#print start
#print end

hdu=fits.open(infile)

cube=hdu[0].data
#print np.shape(cube)
header_cube=hdu[0].header
err=hdu[1].data

new_cube_header=header_cube.copy()


mfr=hdu[2].data.field(3)
#print np.shape(mfr)
mean_mfr=np.nanmean(mfr[start:end])


cube_reduced=np.nanmean(cube[start:end,:,:],axis=0)
err_reduced=np.nanmean(err[start:end,:,:],axis=0)

new_cube_header.remove('ctype3')
new_cube_header.remove('crval3')
new_cube_header.remove('crpix3')
new_cube_header.remove('cdelt3')
new_cube_header.remove('crota3')
new_cube_header['BUNIT']='K'
new_cube_header['COMMENT']='Frequency:{0:E}'.format(mean_mfr)

new_err_header=new_cube_header.copy()

new_cube_header['OBJECT']='GALFACTS S1 U reduced 1.4GHz'
new_err_header['OBJECT']='GALFACTS S1 U reduc-err 1.4GHz'

new_hdu=fits.PrimaryHDU(cube_reduced,header=new_cube_header)
new_err_hdu=fits.PrimaryHDU(err_reduced,header=new_err_header)

outfile_image='S1_binned_U_red.fits'
outfile_err='S1_binned_U_erred.fits'

new_hdu.writeto(outfile_image)
new_err_hdu.writeto(outfile_err)


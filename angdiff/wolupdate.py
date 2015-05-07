#!/usr/local/bin/python

import numpy as np
from astropy.io import fits
import sys

wol_hdu=fits.open(sys.argv[1])
wol_head=wol_hdu[0].header
wol_data=wol_hdu[0].data
wol_data=wol_data[0,:,:]
wol_data=wol_data*0.001
wol_head['NAXIS']=2
wol_head['BUNIT']='K'
wol_head.remove('NAXIS3')

outfile='updated'+sys.argv[1]
fits.writeto(outfile,wol_data,header=wol_head)



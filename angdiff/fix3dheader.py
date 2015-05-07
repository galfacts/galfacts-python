#!/Users/leclercq/miniconda/bin/python

import numpy as np
from astropy.io import fits
import sys
from numpy import pi


infile=sys.argv[1]
field=infile[9:11]

hdu_in=fits.open(infile,mode='update')

map_header=hdu_in[0].header

map_header['EQUINOX']=2000.00
#machinery for new header#

map_header.remove('ctype3')
map_header.remove('crval3')
map_header.remove('crpix3')
map_header.remove('cdelt3')
map_header.remove('crota3')
map_header.remove('date-obs')
####

hdu_in.close()



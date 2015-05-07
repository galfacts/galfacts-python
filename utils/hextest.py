#!/opt/exp_soft/python-2.7.3/bin/python

import numpy as np
from astropy.io import fits


print 'Hex test script'

rand=np.random.random_sample((10,10,10))

fits.writeto('hextest.fits',rand)

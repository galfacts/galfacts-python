#!/Users/leclercq/miniconda/bin/python

import numpy as np
import theil_sen as ts
import matplotlib
matplotlib.use('MacOSX')
import matplotlib.pylab as plt
from astropy.io import fits
import sys
from numpy import pi

diffile=sys.argv[1]
errfile=sys.argv[2]
angdiffhdu=fits.open(diffile)
angerrhdu=fits.open(errfile)

angle_diff=angdiffhdu[0].data*pi/180.
angle_err=angerrhdu[0].data

angle_diff=angle_diff[:,0:4030]
angle_err=angle_err[:,0:4030]


angweight=1/angle_err**2

angle_diff_flat=np.ravel(angle_diff)
angweight_flat=np.ravel(angweight)

good2=np.arange(np.shape(angle_diff_flat)[0])

angle_diff_good=good2[~np.isnan(angle_diff_flat)]
angweight_good=good2[~np.isnan(angweight_flat)]

good_both_2=np.intersect1d(angle_diff_good,angweight_good)

angle_diff_flat=angle_diff_flat[good_both_2]
angweight_flat=angweight_flat[good_both_2]


weighted_diff_average=np.average(angle_diff_flat,weights=angweight_flat)
weighted_diff_average_deg=weighted_diff_average*180./pi

print "The weighted angle difference between the two maps is {0} rad or {1} degrees".format(weighted_diff_average,weighted_diff_average_deg)

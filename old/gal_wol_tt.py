#!/usr/local/bin/python

import numpy as np
import theil_sen as ts
import matplotlib
matplotlib.use('MacOSX')
import matplotlib.pylab as plt
from astropy.io import fits
import sys

###Open Q and U maps from both GALFACTS and DRAO
galqhdu=fits.open(sys.argv[1])
wolqhdu=fits.open(sys.argv[2])
galuhdu=fits.open(sys.argv[3])
woluhdu=fits.open(sys.argv[4])

galq=galqhdu[0].data
wolq=wolqhdu[0].data
galu=galuhdu[0].data
wolu=woluhdu[0].data

####Set up data for TT plots (flatten, remove nans)

galq_flat=np.ravel(galq)
wolq_flat=np.ravel(wolq)
galu_flat=np.ravel(galu)
wolu_flat=np.ravel(wolu)

good=np.arange(np.shape(gal_flat)[0])

#print np.shape(good)
good_galq=good[~np.isnan(galq_flat)]
good_wolq=good[~np.isnan(wolq_flat)]

good_galu=good[~np.isnan(galu_flat)]
good_wolu=good[~np.isnan(wolu_flat)]

#print np.shape(good_wol)
#print np.shape(good_gal)

good_bothq=np.intersect1d(good_galq,good_wolq)
good_bothu=np.intersect1d(good_galu,good_wolu)

#print np.shape(good_both)

gal_flatq=gal_flatq[good_bothq]
wol_flatq=wol_flatq[good_bothq]
gal_flatu=gal_flatu[good_bothu]
wol_flatu=wol_flatu[good_bothu]

###Make TTplots and get offsets

galq_min=np.nanmin(gal_flatq)
galq_max=np.nanmax(gal_flatq)
galu_min=np.nanmin(gal_flatu)
galu_max=np.nanmax(gal_flatu)

xu=np.arange(galu_min,galu_max,0.01)
xq=np.arange(galq_min,galq_max,0.01)

qparams=ts.theil_sen(gal_flatq,wol_flatq)
uparams=ts.theil_sen(gal_flatu,wol_flatu)
coeffq=paramsq[0]
interceptq=paramsq[1]
coeffu=paramsu[0]
interceptu=paramsu[1]

offsetq=-interceptq/coeffq
offsetu=-interceptu/coeffu



print 'The GALFACTS Q data contains a spurious offset of {0} K'.format(offsetq)
print 'The GALFACTS U data contains a spurious offset of {0} K'.format(offsetu)


## matplotlib.rcParams.update({'font.size':14})

## fig,ax=plt.subplots()

## ax.plot(gal_flat,wol_flat)
## ax.plot(x,coeff*x+intercept)
## ax.set_ylabel("DRAO Q (K)")
## ax.set_xlabel("GALFACTS Q (K)")
## ax.set_title('T-T plot for S1 field Q maps')

## fig.savefig("S1_Q_TTplot.pdf",dpi=300)

## plt.show()


galqerrhdu=fits.open(sys.argv[5])
galuerrhdu=fits.open(sys.argv[6])
galqerr=galqerrhdu[0].data
galuerr=galuerrhdu[0].data

##Remove offset:

galq=galq-offsetq
galu=galu-offsetu

###Make galfacts angle map and associated errormaps and chisq etc.

galfacts_angle=0.5*np.arctan2(galu,galq)

wolleben_angle=0.5*np.arctan2(wolu,wolq)

galfacts_angle_error=sqrt(0.25*(1/(galq**2+galu**2))*((galq*galuerr)**2+(galu*galqerr)**2))

wol_angle_error=sqrt(0.25*0.03**2/(wolq**2+galq**2))

angle_diff=galfacts_angle-wolleben_angle

angle_err=sqrt(galfacts_angle_error**2+wol_angle_error**2)


angweight=1/angle_err**2

weighted_diff_average=np.average(angle_diff,weights=angweight)
weighted_diff_average_deg=weighted_diff_average*180./np.pi


#chi_sq=(-angle_diff+weighted_diff_average)**2*angweight


fits.writeto('S1_diff_map.fits',angle_diff)
fits.writeto('S1_diff_err_map.fits',angle_err)

print "The weighted angle difference between the two maps is {0} rad or {1} degrees".format(weighted_diff_average,weighted_diff_average_deg)


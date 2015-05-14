#/Users/leclercq/miniconda/bin/python

import numpy as np
import theil_sen as ts
#import matplotlib
#matplotlib.use('MacOSX')
import matplotlib.pylab as plt
from astropy.io import fits
import sys
from numpy import pi

print 'Reading in data...'

###Open Q and U maps from both GALFACTS and DRAO - input is galfacts q, wolleben q, galfacts u, wolleben u
galqhdu=fits.open(sys.argv[1])
wolqhdu=fits.open(sys.argv[2])
galuhdu=fits.open(sys.argv[3])
woluhdu=fits.open(sys.argv[4])

header_template=galqhdu[0].header

field=sys.argv[1][0:2]

galq=galqhdu[0].data
wolq=wolqhdu[0].data
galu=galuhdu[0].data
wolu=woluhdu[0].data

if field =='S1':
    galq=galq[

print '...done.'
print 'Preparing data for TT plots...'

####Set up data for TT plots (flatten, remove nans)

galq_flat=np.ravel(galq)
wolq_flat=np.ravel(wolq)
galu_flat=np.ravel(galu)
wolu_flat=np.ravel(wolu)

good=np.arange(np.shape(galq_flat)[0])

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

galq_flat=galq_flat[good_bothq]
wolq_flat=wolq_flat[good_bothq]
galu_flat=galu_flat[good_bothu]
wolu_flat=wolu_flat[good_bothu]

###Make TTplots and get offsets

galq_min=np.nanmin(galq_flat)
galq_max=np.nanmax(galq_flat)
galu_min=np.nanmin(galu_flat)
galu_max=np.nanmax(galu_flat)

xu=np.arange(galu_min,galu_max,0.01)
xq=np.arange(galq_min,galq_max,0.01)

print 'Beginning TT plots'

qparams=ts.theil_sen(galq_flat,wolq_flat)
uparams=ts.theil_sen(galu_flat,wolu_flat)
coeffq=qparams[0]
interceptq=qparams[1]
coeffu=uparams[0]
interceptu=uparams[1]

offsetq=-interceptq/coeffq
offsetu=-interceptu/coeffu



print 'The GALFACTS ',field,' Q data contains a spurious offset of {0} K'.format(offsetq)
print 'The GALFACTS ',field,' U data contains a spurious offset of {0} K'.format(offsetu)


##Remove offset:

#galq=galq-offsetq
#galu=galu-offsetu


#write FITS files

#galq_head=header_template.copy()
#galu_head=header_template.copy()


#galq_head['OBJECT']=('GALFACTS '+field+' TTcorrected')
#galu_head['OBJECT']=('GALFACTS '+field+' TTcorrected')

#galq_head['COMMENT']='The GALFACTS Q data contains a spurious offset of {0} K'.format(offsetq)
#galu_head['COMMENT']='The GALFACTS U data contains a spurious offset of {0} K'.format(offsetu)

#galqfileout=field+'_galfacts_q_corrected.fits'
#galufileout=field+'_galfacts_u_corrected.fits'

#fits.writeto(galqfileout,galq,header=galq_head)
#fits.writeto(galufileout,galu,header=galu_head)




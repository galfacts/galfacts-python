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

###Open Q and U maps from both GALFACTS and DRAO - input is galfacts q, wolleben q, galfacts u, wolleben u, galfacts error q, galfacts error u
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



print 'The GALFACTS Q data contains a spurious offset of {0} K'.format(offsetq)
print 'The GALFACTS U data contains a spurious offset of {0} K'.format(offsetu)

galq_head=header_template.copy()
galu_head=header_template.copy()


galq_head['OBJECT']=('GALFACTS '+field+' TTcorrected')
galu_head['OBJECT']=('GALFACTS '+field+' TTcorrected')

galq_head['COMMENT']='The GALFACTS Q data contains a spurious offset of {0} K'.format(offsetq)
galu_head['COMMENT']='The GALFACTS U data contains a spurious offset of {0} K'.format(offsetu)

galqfileout=field+'_galfacts_q_corrected.fits'
galufileout=field+'_galfacts_u_corrected.fits'

print 'Writing out corrected Q & U maps'

fits.writeto(galqfileout,galq,header=galq_head)
fits.writeto(galufileout,galu,header=galu_head)

## matplotlib.rcParams.update({'font.size':14})
## fig,axes=plt.subplots(1,2,figsize=(10,5),squeeze=True)
## fig.subplots_adjust(left= 0.05,right=0.98)
## axes[0].plot(galq_flat,wolq_flat)
## axes[0].plot(xq,coeffq*xq+interceptq)
## axes[0].set_ylabel("DRAO Q (K)")
## axes[0].set_xlabel("GALFACTS Q (K)")
## title0='T-T plot for '+field+' field Q maps.'
## axes[0].set_title(title0)

## axes[1].plot(galu_flat,wolu_flat)
## axes[1].plot(xu,coeffu*xu+interceptu)
## axes[1].set_ylabel("DRAO U (K)")
## axes[1].set_xlabel("GALFACTS U (K)")
## title1='T-T plot for '+field+' field U maps.'
## axes[1].set_title(title1)

## savetitle=field+'_TTplots.pdf'

## fig.savefig(savetitle,dpi=100)




galqerrhdu=fits.open(sys.argv[5])
galuerrhdu=fits.open(sys.argv[6])
galqerr=galqerrhdu[0].data
galuerr=galuerrhdu[0].data

##Remove offset:

galq=galq-offsetq
galu=galu-offsetu

print 'Now making angle maps'

###Make galfacts angle map and associated errormaps etc.

galfacts_angle=0.5*np.arctan2(galu,galq)
galfacts_angle_deg=galfacts_angle*180./pi

wolleben_angle=0.5*np.arctan2(wolu,wolq)
wolleben_angle_deg=wolleben_angle*180./pi

galfacts_angle_error=np.sqrt(0.25*(1/(galq**2+galu**2))*((galq*galuerr)**2+(galu*galqerr)**2))

wol_angle_error=np.sqrt(0.25*0.03**2/(wolq**2+galq**2))

#Take differences, folding the angles into plus or minus 90 degrees

print 'Calculating angle differences and averages'
angle_diff=galfacts_angle-wolleben_angle

angle_diff[angle_diff>pi/2.]-=pi
angle_diff[angle_diff<-pi/2.]+=pi

angle_diff_deg=angle_diff*180./pi

#Compute total combined error on the difference, related weight
angle_err=np.sqrt(galfacts_angle_error**2+wol_angle_error**2)
angle_err_deg=angle_err*180./pi
mean_err_deg=np.nanmean(angle_err_deg)
angweight=1/angle_err**2

#print np.shape(angweight)
#print np.shape(angle_diff)

###Remove nans from the data to do average difference (with inverse error weighting)

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

#Now construct fits headers and write everything to files

print 'Now writing to file'

header_template['BTYPE']='Pol. angle'
header_template['BUNIT']='deg'

galang_head=header_template.copy()
wolang_head=header_template.copy()
diffmap_head=header_template.copy()
differr_head=header_template.copy()

galang_head['OBJECT']=('GALFACTS '+field+' angle map')
wolang_head['OBJECT']=('Wolleben '+field+' angle map')
diffmap_head['OBJECT']=('GALFACTS-Wolleben '+field+' angle difference map')
differr_head['OBJECT']=('GALFACTS-Wolleben '+field+' angle difference error map')

diffmap_head['COMMENT']='Weighted average difference:{0} degrees'.format(weighted_diff_average_deg)
diffmap_head['COMMENT']='Mean error:{0} degrees'.format(mean_err_deg)
diffmap_head['COMMENT']='The GALFACTS Q data contains a spurious offset of {0} K'.format(offsetq)
diffmap_head['COMMENT']='The GALFACTS U data contains a spurious offset of {0} K'.format(offsetu)

difffileout=field+'_diff_map.fits'
errfileout=field+'_diff_err_map.fits'
galangfileout=field+'_galfacts_angles.fits'
wolangfileout=field+'_wolleben_angles.fits'

fits.writeto(difffileout,angle_diff_deg,header=diffmap_head)
fits.writeto(errfileout,angle_err_deg,header=differr_head) #this used to not be in degrees, be careful!
fits.writeto(galangfileout,galfacts_angle_deg,header=galang_head)
fits.writeto(wolangfileout,wolleben_angle_deg,header=wolang_head)


print "The weighted angle difference between the two maps is {0} rad or {1} degrees".format(weighted_diff_average,weighted_diff_average_deg)


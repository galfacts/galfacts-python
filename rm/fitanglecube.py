#!/Users/leclercq/miniconda/bin/python

import numpy as np
from numpy import pi
from astropy.io import fits
from astropy import constants as const
import sys
import linfit

infile=sys.argv[1]
field=infile[0:2]

qin=fits.open(sys.argv[1])
uin=fits.open(sys.argv[2])

angfile='../rmsyn/'+field+'angle.fits'
angle=fits.getdata(angfile)

header_cube=qin[0].header

new_cube_header=header_cube.copy()

#machinery for new header#
map_header=new_cube_header.copy()
map_header.remove('ctype3')
map_header.remove('crval3')
map_header.remove('crpix3')
map_header.remove('cdelt3')
map_header.remove('crota3')
####

qcube=qin[0].data
ucube=uin[0].data

mfr=qin[2].data.field(3)
lamsq=(const.c.value/mfr)**2

s=np.shape(qcube)
sz,sy,sx=s[0],s[1],s[2]

#Fit it, yo (iterate over each pixel of the unfolded angle cube)

print 'Now going to fit for RM and zero angle'
print 'Making angle errors'
qerr=qin[1].data
uerr=uin[1].data
angerr=np.sqrt(0.25*(1/(qcube**2+ucube**2))*((qcube*uerr)**2+(ucube*qerr)**2))

coeffs=np.empty((5,sy,sx))
coeffs_temp=np.empty(5)
print'Fitting...'
for ind in np.ndindex(sy,sx):
    ytemp=angle[:,ind[0],ind[1]]
    errtemp=angerr[:,ind[0],ind[1]]
    coeffs_temp[0],coeffs_temp[1],coeffs_temp[2],coeffs_temp[3],coeffs_temp[4]=linfit.linfit(ytemp,lamsq,errtemp)
    coeffs[:,ind[0],ind[1]]=coeffs_temp
print '...done!'

#output output

angmap=coeffs[0,:,:]
rmmap=coeffs[1,:,:]
angerr=coeffs[2,:,:]
rmerr=coeffs[3,:,:]
chisq=coeffs[4,:,:]


#WRITE IT ALL OUT
print 'Writing output'
angmapout='../rmsyn/'+field+'angmap.fits'
angmap_header=map_header.copy()
angmap_header['BUNIT']='rad'
angmap_header['OBJECT']='galfacts3.1.1 RMsyn angle map (rad) {0}'.format(field)
angmap_header['COMMENT']='2-d angle map made from linear RM fit (offset)'
fits.writeto(angmapout,angmap,angmap_header)
rmmapout='../rmsyn/'+field+'rmmap.fits'
rmmap_header=map_header.copy()
rmmap_header['BUNIT']='rad'
rmmap_header['OBJECT']='galfacts3.1.1 RMsyn RM map (rad/m^2) {0}'.format(field)
rmmap_header['COMMENT']='2-d RM map made from linear RM fit (slope)'
fits.writeto(rmmapout,rmmap,rmmap_header)
angerrout='../rmsyn/'+field+'angerr.fits'
angerr_header=map_header.copy()
angerr_header['BUNIT']='rad'
angerr_header['OBJECT']='galfacts3.1.1 RMsyn angle error map (rad) {0}'.format(field)
angerr_header['COMMENT']='2-d error map made from offset fit error'
fits.writeto(angerrout,angerr,angerr_header)
rmerrout='../rmsyn/'+field+'rmerr.fits'
rmerr_header=map_header.copy()
rmerr_header['BUNIT']='rad'
rmerr_header['OBJECT']='galfacts3.1.1 RMsyn rm error map (rad) {0}'.format(field)
rmerr_header['COMMENT']='2-d error map made from slope fit error'
fits.writeto(rmerrout,rmerr,rmerr_header)
chisqout='../rmsyn/'+field+'chisq.fits'
chisq_header=map_header.copy()
chisq_header['BUNIT']='rad'
chisq_header['OBJECT']='galfacts3.1.1 RMsyn chisq map (rad) {0}'.format(field)
chisq_header['COMMENT']='2-d chi-sq map made from linear RM fit (measures GOF)'
fits.writeto(chisqout,chisq,chisq_header)

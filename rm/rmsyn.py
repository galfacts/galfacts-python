#!/opt/exp_soft/python-2.7.3/bin/python

import numpy as np
from numpy import pi
from astropy.io import fits
from astropy import constants as const
import sys
import linfit
#import bottleneck as bn

#input input
infile=sys.argv[1]
field=infile[0:2]

qin=fits.open(sys.argv[1])
uin=fits.open(sys.argv[2])



qcube=qin[0].data
ucube=uin[0].data

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


mfr=qin[2].data.field(3)
lamsq=(const.c.value/mfr)**2


s=np.shape(qcube)
sz,sy,sx=s[0],s[1],s[2]


#set up RM synthesis cube with hard-coded number of bins & delrm

nbin=100
drm=10

rmmax=nbin*drm/2

rm=np.arange(-rmmax,rmmax,drm)

rm -= np.amin(np.abs(rm))#make sure that 0 RM is in the array

pp=qcube+1j*ucube #slow but does the job - creates polarized intensity cube

pout=np.empty((nbin,sy,sx),dtype=complex)

lamsqb=lamsq.reshape(sz,1,1)


#SYNTHESIZE

for irm in range(nbin):
    print 'Making RM = {0}'.format(rm[irm])
    rot= -2.*rm[irm]*lamsqb
    rr=np.cos(rot)
    ri=np.sin(rot)
    rot=np.tile(rr,(sy,sx))+1j*np.tile(ri,(sy,sx))
    pout[irm,:,:] = np.nansum(rot*pp,axis=0)


#find the max in the cube (single value)
print 'Now finding peak RMs'
pmax=np.nanmax(np.abs(pout),axis=0)
index=np.nanargmax(np.abs(pout),axis=0)

rmp=rm[index] #this makes a sx by sy map of the peak RMs corresponding to the peak pout

#fit 3-point parabola to peak
print 'Fitting 3-point parabola to peak'
first = np.where(index == 0)
last = np.where(index == (nbin-1))

ind1=index-1
ind1[np.where(ind1<0)]=0
rm1=rm[ind1]

ind2=index+1
ind2[np.where(ind2>nbin-1)]=nbin-1
rm2=rm[ind2]

pp1=np.empty((sy,sx))
for idx,z in np.ndenumerate(ind1):
    pp1[idx[0],idx[1]]=abs(pout[z,idx[0],idx[1]])

pp2=np.empty((sy,sx))
for idx,z in np.ndenumerate(ind2):
    pp1[idx[0],idx[1]]=abs(pout[z,idx[0],idx[1]])


#now have array of y1, y2, y3 (pp1,pmax,pp2)
#and x1,x2,x3 (rm1,rmp,rm2)
#want to fit parabola through each triplet of x,y pairs - construct temp arrays and iterate
xtemp=np.empty(3)
ytemp=np.empty(3)

coeffs=np.empty((3,sy,sx))

print 'Fitting...'
for idx in np.ndindex(sy,sx):
    xtemp[0],xtemp[1],xtemp[2]=rm1[idx],rmp[idx],rm2[idx]
    ytemp[0],ytemp[1],ytemp[2]=pp1[idx],pmax[idx],pp2[idx]
    if (xtemp[0] != xtemp[1] and xtemp[1] != xtemp[2]):
        coeffs_temp=np.polyfit(xtemp,ytemp,2)
    else:
        coeffs_temp=np.zeros(3)
    coeffs[:,idx[0],idx[1]]=coeffs_temp
print'...done!'
a=coeffs[0,:,:]
b=coeffs[1,:,:]

rm0=-b/(2.*a)
rm0[first]=rm[0]
rm0[last]=rm[nbin-1]

rm0[np.where(np.isnan(rm0))]=0.0

#Write out rm0 properly
rm0_header=map_header.copy()
rm0_header['BUNIT']='rad/m^2'
rm0_header['OBJECT']='galfacts3.1.1 RMsyn rm0 {0}'.format(field)
rm0_header['COMMENT']='rm0 are the RM derived from basic RM synthesis'
rm0out='../rmsyn/'+field+'rm0.fits'
fits.writeto(rm0out,rm0,rm0_header)

#Now unfold PA:
print 'Now unfolding PA'
#make angle cube (this restricts angle values to within 0,+pi)

angle=0.5*np.arctan2(ucube,qcube)

cchan=sz/2

rm0=np.repeat(rm0.reshape(1,sy,sx),sz,axis=0)
target=rm0*np.reshape(lamsq-lamsq[cchan],(sz,1,1))

target += angle[cchan].reshape(1,sy,sx)

npi=np.around(((target-angle)/pi))
npi[np.where(np.isnan(npi))]=0

angle += pi * npi



#Write it out properly#
angleout='../rmsyn/'+field+'angle.fits'
angle_header=new_cube_header.copy()
angle_header['BUNIT']='rad'
angle_header['OBJECT']='galfacts3.1.1 RMsyn angle cube (rad) {0}'.format(field)
angle_header['COMMENT']='list of lambda^2 values present in extension'
anglehdu=fits.PrimaryHDU(angle,header=angle_header)
anglehdulist=fits.HDUList([anglehdu])
col1=fits.Column(name='channel',format='d',array=np.arange(sz)+1)
col2=fits.Column(name='lambda_square',format='f8',array=lamsq)
cols=fits.ColDefs([col1,col2])
bintablehdu=fits.BinTableHDU.from_columns(cols)
anglehdulist.append(bintablehdu)
anglehdulist.writeto(angleout)


#fit for RM and zero angle! get angle errors
print 'Now going to fit for RM and zero angle'
print 'Making angle errors'
qerr=qin[1].data
uerr=uin[1].data
angerr=np.sqrt(0.25*(1/(qcube**2+ucube**2))*((qcube*uerr)**2+(ucube*qerr)**2))

coeffs=np.empty((6,sy,sx))
coeffs_temp=np.empty(6)
print'Fitting...'
for ind in np.ndindex(sy,sx):
    ytemp=angle[:,ind[0],ind[1]]
    errtemp=angerr[:,ind[0],ind[1]]
    coeffs_temp[0],coeffs_temp[1],coeffs_temp[2],coeffs_temp[3],coeffs_temp[4],coeffs_temp[5]=linfit.linfit(ytemp,lamsq,errtemp)
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








    

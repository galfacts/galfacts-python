#!/Users/leclercq/miniconda/bin/python

import numpy as np
from numpy import pi
from astropy.io import fits
from astropy import constants as const
import sys

#make unfolded angle cubes from an RM-synthesis map and the binned q and u cubes

infile=sys.argv[1]
field=infile[0:2]

qin=fits.open(sys.argv[1])
uin=fits.open(sys.argv[2])

header_cube=qin[0].header

new_cube_header=header_cube.copy()

qcube=qin[0].data
ucube=uin[0].data

mfr=qin[2].data.field(3)
lamsq=(const.c.value/mfr)**2

s=np.shape(qcube)
sz,sy,sx=s[0],s[1],s[2]

#read in rm map

rm0in='../rmsyn/'+field+'rm0.fits'

rm0=fits.getdata(rm0in)

angle=0.5*np.arctan2(ucube,qcube)

#fits.writeto('../rmsyn/quickangleout.fits',angle)

cchan=sz/2

#unfold cube
rm0=np.repeat(rm0.reshape(1,sy,sx),sz,axis=0)
target=rm0*np.reshape(lamsq-lamsq[cchan],(sz,1,1))


target += angle[cchan].reshape(1,sy,sx)

#fits.writeto('../rmsyn/quicktargetout.fits',target)

npi=np.around(((target-angle)/pi))
npi[np.where(np.isnan(npi))]=0

#fits.writeto('../rmsyn/quicknpi.fits',npi)

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



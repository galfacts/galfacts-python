#!/opt/exp_soft/python-2.7.3/bin/python

import sys
import numpy as np 
from astropy.io import fits

#Computes the noise ratio as a function of RA for the binned cubes - syntax ra.py channel (where channel is the 0-indexing chnnel numberx)

#Read in binned cubes - I,Q,U,V and the weight cube W
i_in=sys.argv[1]
q_in=sys.argv[2]
u_in=sys.argv[3]
v_in=sys.argv[4]
w_in=sys.argv[5]
channel=sys.argv[6]

hdu_i=fits.open(i_in)
hdu_q=fits.open(q_in)
hdu_u=fits.open(u_in)
hdu_v=fits.open(v_in)
hdu_w=fits.open(w_in)

i_err=hdu_i[1].data
q_err=hdu_q[1].data
u_err=hdu_u[1].data
v_err=hdu_v[1].data
weights=hdu_w[0].data

header=hdu_i[0].header
refpix=header['CRPIX1']
spacing=header['CDELT1']
refval=header['CRVAL1']

s=np.shape(i_err)

ra=spacing*(np.arange(s[2])-refpix)+refval



w=np.nanmean(weights[channel,:,:],axis=0)


scale_factor= 26.5/np.sqrt(0.4*4.2E5*2.) #this is given by the radiometer thermal noise equation for a given system temperature, bandwidth and integration time (26.5K, 420 kHz and 0.4s), with a 1/sqrt(2) factor reduction in the noise due to gaussian interpolation in the gridding.

w_scaled=scale_factor*(1./np.sqrt(w))

i_ra=np.nanmean(i_err[channel,:,:],axis=0)
q_ra=np.nanmean(q_err[channel,:,:],axis=0)
u_ra=np.nanmean(u_err[channel,:,:],axis=0)
v_ra=np.nanmean(v_err[channel,:,:],axis=0)

i_ra_ratio=i_ra/w_scaled
q_ra_ratio=q_ra/w_scaled
u_ra_ratio=u_ra/w_scaled
v_ra_ratio=v_ra/w_scaled


channel_number=np.ones(s[2])*float(channel)



np.savetxt('../txt/'+i_in[0:2]+'_ra_noise_'+str(channel)+'.txt',(i_ra_ratio,q_ra_ratio,u_ra_ratio,v_ra_ratio,ra,channel_number))

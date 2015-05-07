#!/usr/local/bin/python

import sys
import numpy as np 
from astropy.io import fits



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
refpix=header['CRPIX2']
spacing=header['CDELT2']
refval=header['CRVAL2']

s=np.shape(i_err)

dec=spacing*(np.arange(s[1])-refpix)+refval



w=np.nanmean(weights[channel,:,:],axis=1)


scale_factor= 26.5/np.sqrt(0.4*4.2E5*2.) #this is given by the radiometer thermal noise equation for a given system temperature, bandwidth and integration time (26.5K, 420 kHz and 0.4s), with a 1/sqrt(2) factor reduction in the noise due to gaussian interpolation in the gridding.

w_scaled=scale_factor*(1./np.sqrt(w))

i_dec=np.nanmean(i_err[channel,:,:],axis=1)
q_dec=np.nanmean(q_err[channel,:,:],axis=1)
u_dec=np.nanmean(u_err[channel,:,:],axis=1)
v_dec=np.nanmean(v_err[channel,:,:],axis=1)

i_dec_ratio=i_dec/w_scaled
q_dec_ratio=q_dec/w_scaled
u_dec_ratio=u_dec/w_scaled
v_dec_ratio=v_dec/w_scaled

channel_number=np.ones(s[1])*float(channel)



np.savetxt('S1_dec_noise_'+str(channel)+'.txt',(i_dec_ratio,q_dec_ratio,u_dec_ratio,v_dec_ratio,dec,channel_number))

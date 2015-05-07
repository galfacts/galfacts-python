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


x1=100
x2=5055
y1=100
y2=970

i_crop=i_err[:,y1:y2,x1:x2]
q_crop=q_err[:,y1:y2,x1:x2]
u_crop=u_err[:,y1:y2,x1:x2]
v_crop=v_err[:,y1:y2,x1:x2]
weights_crop=weights[:,y1:y2,x1:x2]

s=np.shape(i_crop)
i_reduced=np.reshape(i_crop,(s[0],s[1]*s[2]))
q_reduced=np.reshape(q_crop,(s[0],s[1]*s[2]))
u_reduced=np.reshape(u_crop,(s[0],s[1]*s[2]))
v_reduced=np.reshape(v_crop,(s[0],s[1]*s[2]))
w_reduced=np.reshape(weights_crop,(s[0],s[1]*s[2]))

i_noise=np.nanmean(i_reduced,axis=1)
q_noise=np.nanmean(q_reduced,axis=1)
u_noise=np.nanmean(u_reduced,axis=1)
v_noise=np.nanmean(v_reduced,axis=1)
w=np.nanmean(w_reduced,axis=1)

scale_factor= 26.5/np.sqrt(0.4*4.2E5*2.) #this is given by the radiometer thermal noise equation for a given system temperature, bandwidth and integration time (26.5K, 420 kHz and 0.4s), with a 1/sqrt(2) factor reduction in the noise due to gaussian interpolation in the gridding.

w_scaled=scale_factor*(1./np.sqrt(w))

i_noise_ratio=i_noise/w_scaled
q_noise_ratio=q_noise/w_scaled
u_noise_ratio=u_noise/w_scaled
v_noise_ratio=v_noise/w_scaled

mfr=hdu_i[2].data.field(3)

np.savetxt('S1_binned_noise.txt', (i_noise_ratio,q_noise_ratio,u_noise_ratio,v_noise_ratio,mfr))


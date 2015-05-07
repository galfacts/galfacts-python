#!/usr/local/bin/python

import numpy as np
from numpy import pi
import matplotlib
matplotlib.use('MacOSX')
import matplotlib.pylab as plt
import gaussbeam
import sys
from astropy.io import fits

######################################################
#General utilities; consider writing separate function

#define pixel step and pixel area in rad
pixstep=pi/(60.*180.)
pixarea=pixstep**2

#Generate white noise as reference scaling factor
wnoise=np.random.randn(1024,1024)
wnoiseft=np.fft.fftshift(np.fft.fft2(wnoise))
wnoiseft2=(wnoiseft*np.conj(wnoiseft)).real
noisepwr_rms=np.sqrt(np.mean(wnoiseft2**2))
scaling=noisepwr_rms/pixarea
#######################################################


# first step is to get images and import header and data into numpy arrays

i_in=sys.argv[1]
q_in=sys.argv[2]
u_in=sys.argv[3]

gal_hdu=fits.open(i_in) 
gal_im=gal_hdu[0].data
sgal=np.shape(gal_im)
cchan=sgal[0]/2
gal_im_bottom=np.nanmean(gal_im[:cchan,20:1044,0:5120],axis=0)
gal_im_top=np.nanmean(gal_im[cchan:,20:1044,0:5120],axis=0)
gal_head=gal_hdu[0].header

q_hdu=fits.open(q_in) 
q_im=q_hdu[0].data
sq=np.shape(q_im)
cchan=sq[0]/2
q_im_bottom=np.nanmean(q_im[:cchan,20:1044,0:5120],axis=0)
q_im_top=np.nanmean(q_im[cchan:,20:1044,0:5120],axis=0)
q_head=q_hdu[0].header

u_hdu=fits.open(u_in) 
u_im=u_hdu[0].data
su=np.shape(u_im)
cchan=su[0]/2
u_im_bottom=np.nanmean(u_im[:cchan,20:1044,0:5120],axis=0)
u_im_top=np.nanmean(u_im[cchan:,20:1044,0:5120],axis=0)
u_head=u_hdu[0].header

#Asisgn zero to blanks

q_im_bottom[np.where(np.isnan(q_im_bottom))]=0.
q_im_top[np.where(np.isnan(q_im_top))]=0.

u_im_bottom[np.where(np.isnan(u_im_bottom))]=0.
u_im_top[np.where(np.isnan(u_im_top))]=0.

gal_im_bottom[np.where(np.isnan(gal_im_bottom))]=0.
gal_im_top[np.where(np.isnan(gal_im_top))]=0.

#Divide images into 5 1024x1024 chunks

gal_im_bottom_0=np.asarray(gal_im_bottom[:,0:1024])
gal_im_bottom_1=np.asarray(gal_im_bottom[:,1024:2048])
gal_im_bottom_2=np.asarray(gal_im_bottom[:,2048:3072])
gal_im_bottom_3=np.asarray(gal_im_bottom[:,3072:4096])
gal_im_bottom_4=np.asarray(gal_im_bottom[:,4096:5120])

gal_im_top_0=np.asarray(gal_im_top[:,0:1024])
gal_im_top_1=np.asarray(gal_im_top[:,1024:2048])
gal_im_top_2=np.asarray(gal_im_top[:,2048:3072])
gal_im_top_3=np.asarray(gal_im_top[:,3072:4096])
gal_im_top_4=np.asarray(gal_im_top[:,4096:5120])

q_im_bottom_0=np.asarray(q_im_bottom[:,0:1024])
q_im_bottom_1=np.asarray(q_im_bottom[:,1024:2048])
q_im_bottom_2=np.asarray(q_im_bottom[:,2048:3072])
q_im_bottom_3=np.asarray(q_im_bottom[:,3072:4096])
q_im_bottom_4=np.asarray(q_im_bottom[:,4096:5120])

q_im_top_0=np.asarray(q_im_top[:,0:1024])
q_im_top_1=np.asarray(q_im_top[:,1024:2048])
q_im_top_2=np.asarray(q_im_top[:,2048:3072])
q_im_top_3=np.asarray(q_im_top[:,3072:4096])
q_im_top_4=np.asarray(q_im_top[:,4096:5120])

u_im_bottom_0=np.asarray(u_im_bottom[:,0:1024])
u_im_bottom_1=np.asarray(u_im_bottom[:,1024:2048])
u_im_bottom_2=np.asarray(u_im_bottom[:,2048:3072])
u_im_bottom_3=np.asarray(u_im_bottom[:,3072:4096])
u_im_bottom_4=np.asarray(u_im_bottom[:,4096:5120])

u_im_top_0=np.asarray(u_im_top[:,0:1024])
u_im_top_1=np.asarray(u_im_top[:,1024:2048])
u_im_top_2=np.asarray(u_im_top[:,2048:3072])
u_im_top_3=np.asarray(u_im_top[:,3072:4096])
u_im_top_4=np.asarray(u_im_top[:,4096:5120])

#Do FTs
ftb0=np.fft.fftshift(np.fft.fft2(gal_im_bottom_0))
ftb1=np.fft.fftshift(np.fft.fft2(gal_im_bottom_1))
ftb2=np.fft.fftshift(np.fft.fft2(gal_im_bottom_2))
ftb3=np.fft.fftshift(np.fft.fft2(gal_im_bottom_3))
ftb4=np.fft.fftshift(np.fft.fft2(gal_im_bottom_4))

ftt0=np.fft.fftshift(np.fft.fft2(gal_im_top_0))
ftt1=np.fft.fftshift(np.fft.fft2(gal_im_top_1))
ftt2=np.fft.fftshift(np.fft.fft2(gal_im_top_2))
ftt3=np.fft.fftshift(np.fft.fft2(gal_im_top_3))
ftt4=np.fft.fftshift(np.fft.fft2(gal_im_top_4))

qftb0=np.fft.fftshift(np.fft.fft2(q_im_bottom_0))
qftb1=np.fft.fftshift(np.fft.fft2(q_im_bottom_1))
qftb2=np.fft.fftshift(np.fft.fft2(q_im_bottom_2))
qftb3=np.fft.fftshift(np.fft.fft2(q_im_bottom_3))
qftb4=np.fft.fftshift(np.fft.fft2(q_im_bottom_4))

qftt0=np.fft.fftshift(np.fft.fft2(q_im_top_0))
qftt1=np.fft.fftshift(np.fft.fft2(q_im_top_1))
qftt2=np.fft.fftshift(np.fft.fft2(q_im_top_2))
qftt3=np.fft.fftshift(np.fft.fft2(q_im_top_3))
qftt4=np.fft.fftshift(np.fft.fft2(q_im_top_4))

uftb0=np.fft.fftshift(np.fft.fft2(u_im_bottom_0))
uftb1=np.fft.fftshift(np.fft.fft2(u_im_bottom_1))
uftb2=np.fft.fftshift(np.fft.fft2(u_im_bottom_2))
uftb3=np.fft.fftshift(np.fft.fft2(u_im_bottom_3))
uftb4=np.fft.fftshift(np.fft.fft2(u_im_bottom_4))

uftt0=np.fft.fftshift(np.fft.fft2(u_im_top_0))
uftt1=np.fft.fftshift(np.fft.fft2(u_im_top_1))
uftt2=np.fft.fftshift(np.fft.fft2(u_im_top_2))
uftt3=np.fft.fftshift(np.fft.fft2(u_im_top_3))
uftt4=np.fft.fftshift(np.fft.fft2(u_im_top_4))


#get fft spatial frequencies
freq_1d=np.fft.fftshift(np.fft.fftfreq(1024,pixstep))

ell_1d= 2*pi*freq_1d

ellx,elly=np.meshgrid(ell_1d,ell_1d)

#define radii of constant ell
ell_r=np.sqrt((ellx)**2+(elly)**2)

#set up grid of phis
phi_ell=np.arctan2(elly,ellx)

#Stack chunks and average

ftstack_b=np.dstack((ftb0,ftb1,ftb2,ftb3,ftb4))
ftstack_t=np.dstack((ftt0,ftt1,ftt2,ftt3,ftt4))

qftstack_b=np.dstack((qftb0,qftb1,qftb2,qftb3,qftb4))
qftstack_t=np.dstack((qftt0,qftt1,qftt2,qftt3,qftt4))

uftstack_b=np.dstack((uftb0,uftb1,uftb2,uftb3,uftb4))
uftstack_t=np.dstack((uftt0,uftt1,uftt2,uftt3,uftt4))

ft_avg_b=np.mean(ftstack_b,axis=2)
ft_avg_t=np.mean(ftstack_t,axis=2)

qft_avg_b=np.mean(qftstack_b,axis=2)
qft_avg_t=np.mean(qftstack_t,axis=2)

uft_avg_b=np.mean(uftstack_b,axis=2)
uft_avg_t=np.mean(uftstack_t,axis=2)

#divide out beam

ft_beam=gaussbeam.makeFTgaussian(1024,fwhm=3.55)

ft_avg_b=ft_avg_b/ft_beam
ft_avg_t=ft_avg_t/ft_beam

uft_avg_b=uft_avg_b/ft_beam
uft_avg_t=uft_avg_t/ft_beam

qft_avg_b=qft_avg_b/ft_beam
qft_avg_t=qft_avg_t/ft_beam


#Calculate E and B mode functions

emode_b=qft_avg_b*np.cos(2.*phi_ell)+uft_avg_b*np.sin(2.*phi_ell)
emode_t=qft_avg_t*np.cos(2.*phi_ell)+uft_avg_t*np.sin(2.*phi_ell)

bmode_b=-qft_avg_b*np.sin(2.*phi_ell)+uft_avg_b*np.cos(2.*phi_ell)
bmode_t=-qft_avg_t*np.sin(2.*phi_ell)+uft_avg_t*np.cos(2.*phi_ell)

#compute correlations (TT,EE,BB) and scale these
ft_pwr=(ft_avg_b*np.conj(ft_avg_t)).real
ee=(emode_b*np.conj(emode_t)).real
bb=(bmode_b*np.conj(bmode_t)).real

ft_scaled=ft_pwr/scaling
ee_scaled=ee/scaling
bb_scaled=bb/scaling

#create bins - single integer ell values for 2-52 and then logarithmically spaced for the rest.

ell_max=np.max(ell_r).astype(np.int)
bins_low=np.arange(2,53).astype(np.uint64)
bins_high=np.logspace(np.log10(53.0),np.log10(ell_max),30).astype(np.uint64)
bins=np.hstack((bins_low,bins_high))
ell_scale=bins*(bins+1)/2.*pi

#use histogram function to take average (using weights)

power_hist=np.histogram(ell_r,bins,weights=ft_scaled)[0]
ell_hist=np.histogram(ell_r,bins)[0]
power_average=np.zeros(power_hist.size)
nonzero=np.where(ell_hist!=0)
power_average[nonzero]=power_hist[nonzero]/ell_hist[nonzero]
d_ell=power_average*ell_scale[1:]

ee_hist=np.histogram(ell_r,bins,weights=ee_scaled)[0]

ee_average=np.zeros(ee_hist.size)
nonzero_ee=np.where(ee_hist!=0)
ee_average[nonzero_ee]=ee_hist[nonzero_ee]/ell_hist[nonzero_ee]
ee_dl=ee_average*ell_scale[1:]

bb_hist=np.histogram(ell_r,bins,weights=bb_scaled)[0]

bb_average=np.zeros(bb_hist.size)
nonzero_bb=np.where(bb_hist!=0)
bb_average[nonzero_bb]=bb_hist[nonzero_bb]/ell_hist[nonzero_bb]
bb_dl=bb_average*ell_scale[1:]

#plot plot plot

bins_center=np.zeros((bins_high.size)-1)

for i in range((bins_high.size)-1):
    bins_center[i]=bins_high[i]+(bins_high[i+1]-bins_high[i])/2.

bins_axis=np.hstack((bins_low,bins_center))

fig,ax=plt.subplots()

ax.set_title('TT,EE and BB power spectra of GALFACTS DR3.1 S1 map --cross-correlated')
ax.set_xlabel('$\ell$',fontsize=16 )
ax.set_ylabel('$D_{\ell}[K^2]$',fontsize=16)
ax.plot(bins_axis,ee_average,'+',label='EE')
ax.plot(bins_axis,bb_average,'x',label='BB')
ax.plot(bins_axis,power_average,'o',label='TT')
ax.legend(loc='upper left')
ax.set_xscale('log')
ax.set_yscale('log')
#plt.axes().set_aspect('equal')

fig.savefig("S1_aps_dqa3.1v2.pdf",dpi=300)
plt.show()



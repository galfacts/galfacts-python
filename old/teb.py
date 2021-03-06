#!/usr/local/bin/python

import numpy as np 
import matplotlib
matplotlib.use('MacOSX')
import matplotlib.pylab as plt
import gaussbeam
import sys

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

gal_hdu=fits.open("GALFACTS_S1_average_image_I.fits") 
gal_im=gal_hdu[0].data
gal_im=np.asarray(gal_im[0,20:1044,0:5120])
gal_head=gal_hdu[0].header

q_hdu=fits.open("GALFACTS_S1_average_image_Q.fits") 
q_im=q_hdu[0].data
q_im=np.asarray(q_im[0,20:1044,0:5120])
q_head=q_hdu[0].header

u_hdu=fits.open("GALFACTS_S1_average_image_U.fits") 
u_im=u_hdu[0].data
u_im=np.asarray(u_im[0,20:1044,0:5120])
u_head=u_hdu[0].header

#Asisgn zero to blanks

q_nan=np.where(np.isnan(q_im))
q_im[q_nan]=0.0

u_nan=np.where(np.isnan(u_im))
u_im[u_nan]=0.0

gal_nan=np.where(np.isnan(gal_im))
gal_im[gal_nan]=0.0

#Divide images into 5 1024x1024 chunks

gal_im_0=np.asarray(gal_im[:,0:1024])
gal_im_1=np.asarray(gal_im[:,1024:2048])
gal_im_2=np.asarray(gal_im[:,2048:3072])
gal_im_3=np.asarray(gal_im[:,3072:4096])
gal_im_4=np.asarray(gal_im[:,4096:5120])

u_im_0=np.asarray(u_im[:,0:1024])
u_im_1=np.asarray(u_im[:,1024:2048])
u_im_2=np.asarray(u_im[:,2048:3072])
u_im_3=np.asarray(u_im[:,3072:4096])
u_im_4=np.asarray(u_im[:,4096:5120])

q_im_0=np.asarray(q_im[:,0:1024])
q_im_1=np.asarray(q_im[:,1024:2048])
q_im_2=np.asarray(q_im[:,2048:3072])
q_im_3=np.asarray(q_im[:,3072:4096])
q_im_4=np.asarray(q_im[:,4096:5120])

#Do FTs
ft0=np.fft.fftshift(np.fft.fft2(gal_im_0))
ft1=np.fft.fftshift(np.fft.fft2(gal_im_1))
ft2=np.fft.fftshift(np.fft.fft2(gal_im_2))
ft3=np.fft.fftshift(np.fft.fft2(gal_im_3))
ft4=np.fft.fftshift(np.fft.fft2(gal_im_4))

qft0=np.fft.fftshift(np.fft.fft2(q_im_0))
qft1=np.fft.fftshift(np.fft.fft2(q_im_1))
qft2=np.fft.fftshift(np.fft.fft2(q_im_2))
qft3=np.fft.fftshift(np.fft.fft2(q_im_3))
qft4=np.fft.fftshift(np.fft.fft2(q_im_4))

uft0=np.fft.fftshift(np.fft.fft2(u_im_0))
uft1=np.fft.fftshift(np.fft.fft2(u_im_1))
uft2=np.fft.fftshift(np.fft.fft2(u_im_2))
uft3=np.fft.fftshift(np.fft.fft2(u_im_3))
uft4=np.fft.fftshift(np.fft.fft2(u_im_4))


#get fft spatial frequencies
freq_1d=np.fft.fftshift(np.fft.fftfreq(1024,pixstep))

ell_1d= 2*pi*freq_1d

ellx,elly=np.meshgrid(ell_1d,ell_1d)

#define radii of constant ell
ell_r=np.sqrt((ellx)**2+(elly)**2)

#set up grid of phis
phi_ell=np.arctan2(elly,ellx)

#Stack chunks and average

ftstack=np.dstack((ft0,ft1,ft2,ft3,ft4))
uftstack=np.dstack((uft0,uft1,uft2,uft3,uft4))
qftstack=np.dstack((qft0,qft1,qft2,qft3,qft4))

ft_avg=np.mean(ftstack,axis=2)
uft_avg=np.mean(uftstack,axis=2)
qft_avg=np.mean(qftstack,axis=2)

#divide out beam

ft_beam=gaussbeam.makeFTgaussian(1024,fwhm=3.5)

ft_avg=ft_avg/ft_beam
uft_avg=uft_avg/ft_beam
qft_avg=qft_avg/ft_beam

#Calculate E and B mode functions

emode=qft_avg*np.cos(2.*phi_ell)+uft_avg*np.sin(2.*phi_ell)
bmode=-qft_avg*np.sin(2.*phi_ell)+uft_avg*np.cos(2.*phi_ell)

#compute correlations (EE,BB) and scale these
ft_pwr=(ft_avg*np.conj(ft_avg)).real
ee=(emode*np.conj(emode)).real
bb=(bmode*np.conj(bmode)).real

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

ax.set_title('TT,EE and BB power spectra of GALFACTS DR3 S1 map')
ax.set_xlabel('$\ell$',fontsize=16 )
ax.set_ylabel('$D_{\ell}[K^2]$',fontsize=16)
ax.plot(bins_axis,ee_average,'+',label='EE')
ax.plot(bins_axis,bb_average,'x',label='BB')
ax.plot(bins_axis,power_average,'o',label='TT')
ax.legend(loc='upper left')
ax.xscale('log')
ax.yscale('log')
#plt.axes().set_aspect('equal')

plt.show()



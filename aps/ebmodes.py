import numpy as np 
import matplotlib.pyplot as plt
from astropy.io import fits
from numpy import pi

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

#get Q and U images (hard-coded destination for now) and import header and data into numpy arrays

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




#divide maps into chunks

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



#stack and average Q FTs and U FTs

uftstack=np.dstack((uft0,uft1,uft2,uft3,uft4))
qftstack=np.dstack((qft0,qft1,qft2,qft3,qft4))

uft_avg=np.mean(uftstack,axis=2)
qft_avg=np.mean(qftstack,axis=2)


#Calculate E and B mode functions

emode=qft_avg*np.cos(2.*phi_ell)+uft_avg*np.sin(2.*phi_ell)
bmode=-qft_avg*np.sin(2.*phi_ell)+uft_avg*np.cos(2.*phi_ell)

#compute correlations (EE,BB) and scale these

ee=(emode*np.conj(emode)).real
bb=(bmode*np.conj(bmode)).real

ee_scaled=ee/scaling
bb_scaled=bb/scaling


#create bins - single integer ell values for 0-50 and then logarithmically spaced for the rest.
ell_max=np.max(ell_r).astype(np.int)

bins_low=np.arange(2,53).astype(np.uint64)

bins_high=np.logspace(np.log10(53.0),np.log10(ell_max),30).astype(np.uint64)

bins=np.hstack((bins_low,bins_high))

ell_scale=bins*(bins+1)/2.*pi

#use histogram function to take average (using weights)

ee_hist=np.histogram(ell_r,bins,weights=ee_scaled)[0]
ell_hist=np.histogram(ell_r,bins)[0]
ee_average=np.zeros(ee_hist.size)
nonzero=np.where(ee_hist!=0)
ee_average[nonzero]=ee_hist[nonzero]/ell_hist[nonzero]

bb_hist=np.histogram(ell_r,bins,weights=bb_scaled)[0]
ell_hist=np.histogram(ell_r,bins
bb_average=np.zeros(bb_hist.size)
nonzero=np.where(bb_hist!=0)
bb_average[nonzero]=bb_hist[nonzero]/ell_hist[nonzero]

print ee_average
print bb_average

ee_dl=ee_average*ell_scale[1:]
bb_dl=bb_average*ell_scale[1:]
#construct power spectrum x-axis

bins_center=np.zeros((bins_high.size)-1)

for i in range((bins_high.size)-1):
    bins_center[i]=bins_high[i]+(bins_high[i+1]-bins_high[i])/2.

bins_axis=np.hstack((bins_low,bins_center))

print bins_axis.size

plt.plot(bins_axis,ee_dl,'+')
plt.plot(bins_axis,bb_dl,'x')
plt.xscale('log')
plt.yscale('log')

plt.show()





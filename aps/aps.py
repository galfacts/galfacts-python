import numpy as np 
import matplotlib.pyplot as plt
from astropy.io import fits
from numpy import pi

# first step is to get image (hard-coded destination for now) and import header and data into numpy arrays

gal_hdu=fits.open("GALFACTS_S1_average_image_I.fits") 
gal_im=gal_hdu[0].data
gal_im=np.asarray(gal_im[0,20:1044,0:5120])
gal_head=gal_hdu[0].header

#Asisgn zero to blanks
gal_nan=np.where(np.isnan(gal_im))
gal_im[gal_nan]=0.0

#define pixel step and pixel area in rad
pixstep=pi/(60.*180.)
pixarea=pixstep**2

#Divide image into 5 1024x1024 chunks

gal_im_0=np.asarray(gal_im[:,0:1024])
gal_im_1=np.asarray(gal_im[:,1024:2048])
gal_im_2=np.asarray(gal_im[:,2048:3072])
gal_im_3=np.asarray(gal_im[:,3072:4096])
gal_im_4=np.asarray(gal_im[:,4096:5120])

#plt.subplot(2,6,7)
#plt.imshow(np.log(gal_im_0))
#plt.subplot(2,6,8)
#plt.imshow(np.log(gal_im_1))
#plt.subplot(2,6,9)
#plt.imshow(np.log(gal_im_2))
#plt.subplot(2,6,10)
#plt.imshow(np.log(gal_im_3))
#plt.subplot(2,6,11)
#plt.imshow(np.log(gal_im_4))

#Do FFTs of 1024 chunks

ft0=np.fft.fftshift(np.fft.fft2(gal_im_0))
ft1=np.fft.fftshift(np.fft.fft2(gal_im_1))
ft2=np.fft.fftshift(np.fft.fft2(gal_im_2))
ft3=np.fft.fftshift(np.fft.fft2(gal_im_3))
ft4=np.fft.fftshift(np.fft.fft2(gal_im_4))

#Stack chunks and average

ftstack=np.dstack((ft0,ft1,ft2,ft3,ft4))
ft_pwr=(ftstack*np.conj(ftstack)).real
ft_avg=np.mean(ft_pwr,axis=2)

#plt.subplot(2,6,1)
#plt.imshow(np.log(ft_pwr[:,:,0]))
#plt.subplot(2,6,2)
#plt.imshow(np.log(ft_pwr[:,:,1]))
#plt.subplot(2,6,3)
#plt.imshow(np.log(ft_pwr[:,:,2]))
#plt.subplot(2,6,4)
#plt.imshow(np.log(ft_pwr[:,:,3]))
#plt.subplot(2,6,5)
#plt.imshow(np.log(ft_pwr[:,:,4]))
#plt.subplot(2,6,6)
#plt.imshow(np.log(ft_avg))
#plt.colorbar()
#plt.show()


#Generate white noise as reference scaling
wnoise=np.random.randn(1024,1024)
wnoiseft=np.fft.fftshift(np.fft.fft2(wnoise))
wnoiseft2=(wnoiseft*np.conj(wnoiseft)).real
noisepwr_rms=np.sqrt(np.mean(wnoiseft2**2))
scaling=noisepwr_rms/pixarea


#Scale fft
ft_scaled=ft_avg/scaling

#get fft spatial frequencies
freq_1d=np.fft.fftshift(np.fft.fftfreq(1024,pixstep))

#make grid of ells

ell_1d= 2*pi*freq_1d

ellx,elly=np.meshgrid(ell_1d,ell_1d)

#define radii of constant ell
ell_r=np.sqrt((ellx)**2+(elly)**2)


#create bins - single integer ell values for 0-50 and then logarithmically spaced for the rest.
ell_max=np.max(ell_r).astype(np.int)

bins_low=np.arange(0,51).astype(np.uint64)

bins_high=np.logspace(np.log10(51.0),np.log10(ell_max),30).astype(np.uint64)

bins=np.hstack((bins_low,bins_high))

ell_scale=bins*(bins+1)/2.*pi

#use histogram function to take average (using weights)

power_hist=np.histogram(ell_r,bins,weights=ft_scaled)[0]
ell_hist=np.histogram(ell_r,bins)[0]
power_average=np.zeros(power_hist.size)

nonzero=np.where(ell_hist!=0)
power_average[nonzero]=power_hist[nonzero]/ell_hist[nonzero]

d_ell=power_average*ell_scale[1:]

#print power_average

#construct power spectrum x-axis

bins_center=np.zeros((bins_high.size)-1)

for i in range((bins_high.size)-1):
    bins_center[i]=bins_high[i]+(bins_high[i+1]-bins_high[i])/2.

bins_axis=np.hstack((bins_low,bins_center))
#print bins_axis

#print bins_axis.size,power_average.size

#plt.subplot(2,6,12)
plt.plot(bins_axis,power_average,'x')
plt.xscale('log')
plt.yscale('log')
plt.show()









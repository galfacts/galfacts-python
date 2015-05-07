#!/Users/leclercq/miniconda/bin/python

import numpy as np 
import matplotlib
matplotlib.use('MacOSX')
import matplotlib.pylab as plt
import gaussbeam
import sys
from numpy import pi
from astropy.io import fits

#define pixel step and pixel area in rad
pixstep=pi/(60.*180.)
pixarea=pixstep**2
area1024=pixarea*(1024**2)


#Generate white noise as reference scaling factor
wnoise=np.random.randn(1024,1024)
wnoiseft=np.fft.fftshift(np.fft.fft2(wnoise))
wnoiseft2=(wnoiseft*np.conj(wnoiseft)).real
noisepwr_rms=np.sqrt(np.mean(wnoiseft2**2))
scaling=noisepwr_rms/pixarea


sourcesim=fits.getdata('/Users/leclercq/galfacts/source_sim.fits')

ftsources=np.fft.fftshift(np.fft.fft2(sourcesim))

source_pwr=(ft0*np.conj(ftsources)).real
source_scaled=source_pwr/scaling

#get fft spatial frequencies
freq_1d=np.fft.fftshift(np.fft.fftfreq(1024,pixstep))

ell_1d= 2*pi*freq_1d

ellx,elly=np.meshgrid(ell_1d,ell_1d)

#define radii of constant ell
ell_r=np.sqrt((ellx)**2+(elly)**2)


ft_beam=gaussbeam.makeFTgaussian(1024,fwhm=3.5)

ftunbeam=ft0/ft_beam

ell_max=np.max(ell_r).astype(np.int)
bins_low=np.arange(2,53).astype(np.uint64)
bins_high=np.logspace(np.log10(20.0),np.log10(ell_max),50).astype(np.uint64)
bins=bins_high
ell_scale=bins*(bins+1)/2.*pi



source_hist=np.histogram(ell_r,bins,weights=source_scaled)[0]
ell_hist=np.histogram(ell_r,bins)[0]
source_average=np.zeros(source_hist.size)
nonzero=np.where(ell_hist!=0)
source_average[nonzero]=area1024*source_hist[nonzero]/ell_hist[nonzero]


#plotplot

bins_center=np.zeros((bins_high.size)-1)

for i in range((bins_high.size)-1):
    bins_center[i]=bins_high[i]+(bins_high[i+1]-bins_high[i])/2.

bins_axis=bins_center

fig,ax=plt.subplots(figsize=(8,8))
ax.plot(bins_axis,power_average,'+',label='TT')
ax.set_xlabel('$\ell$',fontsize=16 )
ax.set_ylabel('$C_{\ell}[K^2]$',fontsize=16)


ax.set_xscale('log')
ax.set_yscale('log')

ax.set_aspect('equal')


plt.show()
